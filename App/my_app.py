from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import redis
import json
from datetime import datetime
import logging

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ================================
# Application Setup
# ================================
app = Flask(__name__)
app.secret_key = os.urandom(24)

# ================================
# SQLAlchemy Configuration
# ================================
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://mika:mikarotem@flask-db.c5sgseyquqxi.eu-central-1.rds.amazonaws.com:3306/task_manager_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ================================
# Redis Configuration
# ================================
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    db=0
)

# ================================
# Flask-Session Configuration – Store sessions in Redis
# ================================
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis_client
Session(app)

# ================================
# Models
# ================================
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

# ================================
# Helper Functions – Cache for todos
# ================================
def get_cached_todos(user_id):
    """
    Returns the list of todos from Redis if the cache exists.
    Otherwise, it queries the database, stores the result in Redis for one hour,
    and returns the data.
    """
    cache_key = f'user:{user_id}:todos'
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        logger.info(f"\n🚀 Retrieved data from Redis cache for user {user_id}")
        return json.loads(cached_data)
    
    logger.info(f"\n📁 No cache found! Retrieving data from the database for user {user_id}")
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
    """
    Clears the todos cache for the user.
    """
    cache_key = f'user:{user_id}:todos'
    redis_client.delete(cache_key)
    logger.info(f"🗑️ Cleared cache for user {user_id}")

# ================================
# Application Routes
# ================================

# Home page – displays the list of todos using the index.html template
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

# Registration page – uses the register.html template
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists, please choose another.')
            return redirect(url_for('register'))
        
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login page – uses the login.html template
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
        
        flash('Invalid username or password.')
    
    return render_template('login.html')

# Logout – clears the session and redirects to the login page
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

# Add todo – processes the add todo form
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
    
    flash('Todo added successfully!')
    return redirect(url_for('index'))

# Toggle the status of a todo
@app.route('/toggle_todo/<int:id>')
def toggle_todo(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    todo = db.session.get(Todo, id)
    if not todo:
        flash('Todo not found')
        return redirect(url_for('index'))
    
    if todo.user_id != user_id:
        flash('You are not authorized to perform this action')
        return redirect(url_for('index'))
    
    todo.completed = not todo.completed
    db.session.commit()
    invalidate_cache(user_id)
    
    flash('Todo status updated')
    return redirect(url_for('index'))

# Delete todo
@app.route('/delete_todo/<int:id>')
def delete_todo(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    todo = db.session.get(Todo, id)
    if not todo:
        flash('Todo not found')
        return redirect(url_for('index'))
    
    if todo.user_id != user_id:
        flash('You are not authorized to delete this todo')
        return redirect(url_for('index'))
    
    db.session.delete(todo)
    db.session.commit()
    invalidate_cache(user_id)
    
    flash('Todo deleted successfully')
    return redirect(url_for('index'))

# Check Redis cache status
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

# Display user statistics
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

# ================================
# Run the Application
# ================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
