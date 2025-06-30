
resource "aws_security_group" "rds" {
  name        = "task-manager-app-rds-sg"
  description = "Security group for Task manager App"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "task-manager-app-rds-sg"
  }
}

# Security Group for redis
resource "aws_security_group" "redis_sg" {
  name        = "task-manager-app-REDIS-sg-new"
  description = "Security group for App Redis"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "app-redis-sg"
  }
}

# RDS Subnet Group
resource "aws_db_subnet_group" "flask" {
  name       = "flask-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "Flask DB subnet group"
  }
}

# RDS Instance
resource "aws_db_instance" "flask" {
  identifier        = "flask-db"
  engine              = "mysql"
  engine_version      = "8.0.32" 
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.flask.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  publicly_accessible = false
  skip_final_snapshot = true

  tags = {
    Environment = "production"
    Project     = "flask-app"
  }
}

