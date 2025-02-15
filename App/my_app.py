from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv  # For loading the .env file
import os
import redis
import json
from datetime import datetime
import logging
import hvac  # Library for communicating with Vault

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.secret_key = os.urandom(24)

vault_addr = os.getenv("VAULT_ADDR", "http://vault.vault.svc.cluster.local:8200")
vault_token = os.getenv("VAULT_TOKEN")


try:
    vault_client = hvac.Client(url=vault_addr, token=vault_token)
    secret_response = vault_client.secrets.kv.v2.read_secret_version(
        path="database/mysql",
        mount_point="secret"
    )
    secret_data = secret_response["data"]["data"]

    rds_username = secret_data["username"]
    rds_password = secret_data["password"]
    rds_host     = secret_data["host"]
    rds_port     = secret_data.get("port", 3306)
    rds_database = secret_data["dbname"]

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{rds_username}:{rds_password}@{rds_host}:{rds_port}/{rds_database}"
    logger.info("Database connection successfully configured from Vault")
except Exception as e:
    logger.error("Error retrieving secret from Vault: " + str(e))
    raise e

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

redis_client = redis.Redis(
    host="redis-service.redis.svc.cluster.local",
    port=6379,
    db=0
)

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis_client
Session(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

def get_cached_todos(user_id):
   cache_key = f'user:{user_id}:todos'
   cached_data = redis_client.get(cache_key)
   
   if cached_data:
       logger.info(f"\n🚀 Retrieving data from Redis cache for user {user_id}")
       return json.loads(cached_data)
   
   logger.info(f"\n📁 No data in cache! Retrieving data from the database for user {user_id}")
   todos = Todo.query.filter_by(user_id=user_id).order_by(Todo.created_at.desc()).all()
   todos_data = [{
       'id': todo.id,
       'title': todo.title,
       'description': todo.description,
       'completed': todo.completed,
       'created_at': todo.created_at.isoformat()
   } for todo in todos]
   
   redis_client.setex(cache_key, 3600, json.dumps(todos_data))
   return todos_data

def invalidate_cache(user_id):
   cache_key = f'user:{user_id}:todos'
   redis_client.delete(cache_key)
   logger.info(f"🗑️ Clearing cache for user {user_id}")

@app.route('/')
def index():
   if 'user_id' not in session:
       return redirect(url_for('login'))
   
   user_id = session['user_id']
   user = db.session.get(User, user_id)
   if not user:
       session.clear()
       return redirect(url_for('login'))
   
   todos = get_cached_todos(user_id)
   return render_template('index.html', todos=todos, username=user.username)

@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       
       if User.query.filter_by(username=username).first():
           flash('Username already exists, please choose another one.')
           return redirect(url_for('register'))
       
       new_user = User(username=username, password=generate_password_hash(password))
       db.session.add(new_user)
       db.session.commit()
       
       flash('Registration successful! Please log in.')
       return redirect(url_for('login'))
   
   return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       
       user = User.query.filter_by(username=username).first()
       if user and check_password_hash(user.password, password):
           session.clear()
           session['user_id'] = user.id
           flash('Login successful!')
           return redirect(url_for('index'))
       
       flash('Incorrect username or password.')
   
   return render_template('login.html')

@app.route('/logout')
def logout():
   session.clear()
   flash('You have logged out successfully!')
   return redirect(url_for('login'))

@app.route('/add_todo', methods=['POST'])
def add_todo():
   if 'user_id' not in session:
       return redirect(url_for('login'))
   
   user_id = session['user_id']
   title = request.form['title']
   description = request.form['description']
   
   todo = Todo(title=title, description=description, user_id=user_id)
   db.session.add(todo)
   db.session.commit()
   invalidate_cache(user_id)
   
   flash('Task added successfully!')
   return redirect(url_for('index'))

@app.route('/toggle_todo/<int:id>')
def toggle_todo(id):
   if 'user_id' not in session:
       return redirect(url_for('login'))
   
   user_id = session['user_id']
   todo = db.session.get(Todo, id)
   if not todo:
       flash('Task not found')
       return redirect(url_for('index'))
   
   if todo.user_id != user_id:
       flash('You do not have permission to perform this action')
       return redirect(url_for('index'))
   
   todo.completed = not todo.completed
   db.session.commit()
   invalidate_cache(user_id)
   
   flash('Task status updated')
   return redirect(url_for('index'))

@app.route('/delete_todo/<int:id>')
def delete_todo(id):
   if 'user_id' not in session:
       return redirect(url_for('login'))
   
   user_id = session['user_id']
   todo = db.session.get(Todo, id)
   if not todo:
       flash('Task not found')
       return redirect(url_for('index'))
   
   if todo.user_id != user_id:
       flash('No permission to delete')
       return redirect(url_for('index'))
   
   db.session.delete(todo)
   db.session.commit()
   invalidate_cache(user_id)
   
   flash('Task deleted successfully')
   return redirect(url_for('index'))

@app.route('/check_redis')
def check_redis():
   if 'user_id' not in session:
       return redirect(url_for('login'))
   
   user_id = session['user_id']
   cache_key = f'user:{user_id}:todos'
   cached_data = redis_client.get(cache_key)
   
   if cached_data:
       todos = json.loads(cached_data)
       ttl = redis_client.ttl(cache_key)
       return f"""
           <h2>Redis Cache Status</h2>
           <p>Cache exists for user {user_id} with TTL: {ttl} seconds</p>
           <pre>{json.dumps(todos, indent=2)}</pre>
       """
   else:
       return f"<h2>No cache found for user {user_id}</h2>"

@app.route('/user_stats')
def user_stats():
   if 'user_id' not in session:
       return redirect(url_for('login'))
   
   user_id = session['user_id']
   stats = {
       'active_todos': Todo.query.filter_by(user_id=user_id, completed=False).count(),
       'completed_todos': Todo.query.filter_by(user_id=user_id, completed=True).count()
   }
   return json.dumps(stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
