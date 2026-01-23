# Complete Databases Guide - SQL & NoSQL

## Table of Contents
1. [Introduction to Databases](#introduction-to-databases)
2. [MySQL](#mysql)
3. [PostgreSQL](#postgresql)
4. [MongoDB (NoSQL)](#mongodb-nosql)
5. [Redis (NoSQL)](#redis-nosql)
6. [Cassandra (NoSQL)](#cassandra-nosql)
7. [Read vs Write Operations](#read-vs-write-operations)
8. [SMB vs Enterprise Architecture](#smb-vs-enterprise-architecture)
9. [Database Optimization](#database-optimization)
10. [Replication & Sharding](#replication--sharding)
11. [Interview Questions (3 YOE)](#interview-questions-3-years-experience)

---

## Introduction to Databases

### SQL vs NoSQL Comparison

| Feature | SQL (Relational) | NoSQL (Non-Relational) |
|---------|------------------|------------------------|
| **Data Model** | Tables with rows and columns | Document, Key-Value, Column-family, Graph |
| **Schema** | Fixed schema (predefined) | Flexible/Dynamic schema |
| **Scalability** | Vertical (scale-up) | Horizontal (scale-out) |
| **ACID** | Full ACID compliance | Eventual consistency (BASE) |
| **Joins** | Complex joins supported | Limited or no joins |
| **Best For** | Complex queries, transactions | High throughput, flexible data |
| **Examples** | MySQL, PostgreSQL, Oracle | MongoDB, Redis, Cassandra |
| **Use Cases** | Banking, ERP, CRM | Real-time analytics, caching, IoT |

### When to Use SQL
- **Structured data** with clear relationships
- **ACID transactions** required (banking, e-commerce)
- **Complex queries** with joins
- **Data integrity** is critical
- **Reporting and analytics** on structured data

### When to Use NoSQL
- **Unstructured/semi-structured** data
- **High scalability** requirements
- **Flexible schema** (rapid development)
- **High read/write throughput**
- **Real-time applications** (chat, gaming)
- **Big data** and distributed systems

---

## MySQL

### Introduction
- **Type:** Relational Database (RDBMS)
- **License:** Open Source (GPL) / Commercial
- **Current Version:** 8.0+
- **Storage Engines:** InnoDB (default), MyISAM, Memory
- **ACID Compliance:** Yes
- **Use Cases:** Web applications, e-commerce, CMS, ERP

### Installation

**Ubuntu/Debian:**
```bash
# Update package index
sudo apt update

# Install MySQL Server
sudo apt install mysql-server

# Secure installation
sudo mysql_secure_installation

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Check status
sudo systemctl status mysql

# Login to MySQL
sudo mysql -u root -p
```

**Windows:**
```powershell
# Download MySQL Installer from mysql.com
# Run installer and select MySQL Server

# Add MySQL to PATH (if not added automatically)
$env:PATH += ";C:\Program Files\MySQL\MySQL Server 8.0\bin"

# Start MySQL Service
net start MySQL80

# Login to MySQL
mysql -u root -p
```

**Docker:**
```bash
# Run MySQL container
docker run --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=mypassword \
  -e MYSQL_DATABASE=mydb \
  -p 3306:3306 \
  -d mysql:8.0

# Connect to MySQL
docker exec -it mysql-db mysql -uroot -p
```

### Basic Configuration
```sql
-- Create database
CREATE DATABASE myapp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'strong_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON myapp_db.* TO 'appuser'@'localhost';
FLUSH PRIVILEGES;

-- Show databases
SHOW DATABASES;

-- Use database
USE myapp_db;
```

### Data Types
```sql
-- Numeric Types
TINYINT           -- 1 byte (-128 to 127)
SMALLINT          -- 2 bytes (-32768 to 32767)
MEDIUMINT         -- 3 bytes
INT / INTEGER     -- 4 bytes (-2B to 2B)
BIGINT            -- 8 bytes
DECIMAL(10,2)     -- Fixed-point (exact)
FLOAT             -- 4 bytes (approximate)
DOUBLE            -- 8 bytes (approximate)

-- String Types
CHAR(10)          -- Fixed length (max 255)
VARCHAR(255)      -- Variable length (max 65535)
TEXT              -- Up to 65,535 characters
MEDIUMTEXT        -- Up to 16MB
LONGTEXT          -- Up to 4GB
ENUM('a','b','c') -- Enumeration
JSON              -- JSON data type

-- Date/Time Types
DATE              -- YYYY-MM-DD
TIME              -- HH:MM:SS
DATETIME          -- YYYY-MM-DD HH:MM:SS
TIMESTAMP         -- Auto-updating timestamp
YEAR              -- 4-digit year

-- Binary Types
BLOB              -- Binary large object
MEDIUMBLOB        -- Up to 16MB
LONGBLOB          -- Up to 4GB
```

### CREATE - Tables and Schemas

```sql
-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Posts table with foreign key
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INT NOT NULL,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_author (author_id),
    INDEX idx_status (status),
    INDEX idx_published (published_at),
    FULLTEXT INDEX idx_content (title, content)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Comments table
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_post (post_id),
    INDEX idx_user (user_id)
) ENGINE=InnoDB;

-- Tags table (many-to-many)
CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Post-Tags junction table
CREATE TABLE post_tags (
    post_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    INDEX idx_tag (tag_id)
) ENGINE=InnoDB;
```

### READ Operations

```sql
-- Basic SELECT
SELECT * FROM users;
SELECT id, username, email FROM users;

-- WHERE conditions
SELECT * FROM users WHERE is_active = TRUE;
SELECT * FROM users WHERE created_at > '2024-01-01';
SELECT * FROM users WHERE username LIKE 'john%';

-- Multiple conditions
SELECT * FROM users 
WHERE is_active = TRUE 
AND created_at > '2024-01-01'
ORDER BY created_at DESC;

-- IN operator
SELECT * FROM users WHERE id IN (1, 2, 3, 4, 5);

-- BETWEEN
SELECT * FROM posts WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- NULL checks
SELECT * FROM users WHERE full_name IS NOT NULL;

-- Pattern matching
SELECT * FROM users WHERE email LIKE '%@gmail.com';
SELECT * FROM users WHERE username REGEXP '^[a-z]+$';

-- Sorting
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10;
SELECT * FROM users ORDER BY username ASC, created_at DESC;

-- Pagination
SELECT * FROM posts 
ORDER BY created_at DESC 
LIMIT 10 OFFSET 20;  -- Page 3 (skip 20, show 10)

-- Aggregate functions
SELECT COUNT(*) FROM users;
SELECT COUNT(*) as total_users, SUM(id) as sum_ids FROM users;
SELECT MAX(created_at) as latest_post FROM posts;
SELECT MIN(created_at) as first_post FROM posts;
SELECT AVG(id) as avg_id FROM users;

-- GROUP BY
SELECT status, COUNT(*) as count 
FROM posts 
GROUP BY status;

SELECT author_id, COUNT(*) as post_count, MAX(created_at) as latest_post
FROM posts
GROUP BY author_id
HAVING post_count > 5
ORDER BY post_count DESC;

-- DISTINCT
SELECT DISTINCT status FROM posts;
SELECT COUNT(DISTINCT author_id) as unique_authors FROM posts;

-- JOINS
-- INNER JOIN
SELECT u.username, p.title, p.created_at
FROM users u
INNER JOIN posts p ON u.id = p.author_id
WHERE p.status = 'published'
ORDER BY p.created_at DESC;

-- LEFT JOIN
SELECT u.username, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.author_id
GROUP BY u.id, u.username
ORDER BY post_count DESC;

-- Multiple JOINS
SELECT 
    u.username,
    p.title,
    COUNT(c.id) as comment_count
FROM posts p
INNER JOIN users u ON p.author_id = u.id
LEFT JOIN comments c ON p.id = c.post_id
GROUP BY p.id, u.username, p.title
HAVING comment_count > 0
ORDER BY comment_count DESC;

-- Many-to-many JOIN
SELECT p.title, GROUP_CONCAT(t.name) as tags
FROM posts p
LEFT JOIN post_tags pt ON p.id = pt.post_id
LEFT JOIN tags t ON pt.tag_id = t.id
GROUP BY p.id, p.title;

-- Subqueries
SELECT * FROM users 
WHERE id IN (
    SELECT DISTINCT author_id FROM posts WHERE status = 'published'
);

-- EXISTS
SELECT u.* FROM users u
WHERE EXISTS (
    SELECT 1 FROM posts p WHERE p.author_id = u.id AND p.status = 'published'
);

-- UNION
SELECT username as name, 'user' as type FROM users
UNION
SELECT title as name, 'post' as type FROM posts;
```

### WRITE Operations

```sql
-- INSERT single row
INSERT INTO users (username, email, password_hash, full_name)
VALUES ('johndoe', 'john@example.com', 'hashed_password', 'John Doe');

-- INSERT multiple rows
INSERT INTO users (username, email, password_hash) VALUES
('user1', 'user1@example.com', 'hash1'),
('user2', 'user2@example.com', 'hash2'),
('user3', 'user3@example.com', 'hash3');

-- INSERT with SELECT
INSERT INTO archived_posts (title, content, author_id)
SELECT title, content, author_id 
FROM posts 
WHERE status = 'archived';

-- INSERT IGNORE (skip duplicates)
INSERT IGNORE INTO users (username, email, password_hash)
VALUES ('existing_user', 'existing@example.com', 'hash');

-- ON DUPLICATE KEY UPDATE
INSERT INTO users (username, email, password_hash)
VALUES ('johndoe', 'john@example.com', 'new_hash')
ON DUPLICATE KEY UPDATE 
    password_hash = VALUES(password_hash),
    updated_at = CURRENT_TIMESTAMP;

-- UPDATE single row
UPDATE users 
SET full_name = 'John Smith', updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- UPDATE multiple rows
UPDATE posts 
SET status = 'published', published_at = CURRENT_TIMESTAMP
WHERE status = 'draft' AND author_id = 1;

-- UPDATE with calculation
UPDATE users 
SET login_count = login_count + 1, last_login = CURRENT_TIMESTAMP
WHERE id = 1;

-- UPDATE with JOIN
UPDATE posts p
INNER JOIN users u ON p.author_id = u.id
SET p.status = 'archived'
WHERE u.is_active = FALSE;

-- DELETE single row
DELETE FROM users WHERE id = 1;

-- DELETE multiple rows
DELETE FROM posts WHERE status = 'draft' AND created_at < '2024-01-01';

-- DELETE with JOIN
DELETE p FROM posts p
INNER JOIN users u ON p.author_id = u.id
WHERE u.is_active = FALSE;

-- DELETE all rows (DANGEROUS!)
DELETE FROM temp_data;

-- TRUNCATE (faster than DELETE, resets AUTO_INCREMENT)
TRUNCATE TABLE temp_data;

-- REPLACE (DELETE + INSERT)
REPLACE INTO users (id, username, email, password_hash)
VALUES (1, 'johndoe', 'john@example.com', 'new_hash');
```

### Transactions (ACID)

```sql
-- Start transaction
START TRANSACTION;

-- Multiple operations
INSERT INTO users (username, email, password_hash) 
VALUES ('newuser', 'new@example.com', 'hash');

SET @user_id = LAST_INSERT_ID();

INSERT INTO posts (title, content, author_id)
VALUES ('First Post', 'Content here', @user_id);

-- Commit (save changes)
COMMIT;

-- Rollback (undo changes)
ROLLBACK;

-- Example: Transfer money (banking)
START TRANSACTION;

-- Deduct from account A
UPDATE accounts SET balance = balance - 100 WHERE id = 1;

-- Add to account B
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Check if both succeeded
SELECT balance FROM accounts WHERE id IN (1, 2);

-- Commit if all good, otherwise ROLLBACK
COMMIT;
```

### Indexes

```sql
-- Create index
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_username ON users(username);

-- Composite index
CREATE INDEX idx_status_date ON posts(status, created_at);

-- Unique index
CREATE UNIQUE INDEX idx_unique_email ON users(email);

-- Fulltext index
CREATE FULLTEXT INDEX idx_fulltext_content ON posts(title, content);

-- Show indexes
SHOW INDEX FROM users;

-- Drop index
DROP INDEX idx_email ON users;

-- Analyze index usage
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';
```

### Stored Procedures

```sql
-- Create stored procedure
DELIMITER $$

CREATE PROCEDURE GetUserPosts(IN userId INT)
BEGIN
    SELECT p.id, p.title, p.created_at
    FROM posts p
    WHERE p.author_id = userId
    ORDER BY p.created_at DESC;
END$$

DELIMITER ;

-- Call procedure
CALL GetUserPosts(1);

-- Procedure with OUT parameter
DELIMITER $$

CREATE PROCEDURE GetUserStats(IN userId INT, OUT postCount INT, OUT commentCount INT)
BEGIN
    SELECT COUNT(*) INTO postCount FROM posts WHERE author_id = userId;
    SELECT COUNT(*) INTO commentCount FROM comments WHERE user_id = userId;
END$$

DELIMITER ;

-- Call with OUT parameters
CALL GetUserStats(1, @posts, @comments);
SELECT @posts, @comments;

-- Drop procedure
DROP PROCEDURE IF EXISTS GetUserPosts;
```

### Triggers

```sql
-- Create trigger
DELIMITER $$

CREATE TRIGGER before_user_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END$$

DELIMITER ;

-- Trigger to log changes
CREATE TABLE user_audit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(10),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE TRIGGER after_user_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_audit (user_id, action) VALUES (NEW.id, 'INSERT');
END$$

CREATE TRIGGER after_user_delete
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_audit (user_id, action) VALUES (OLD.id, 'DELETE');
END$$

DELIMITER ;

-- Show triggers
SHOW TRIGGERS;

-- Drop trigger
DROP TRIGGER IF EXISTS before_user_update;
```

### Views

```sql
-- Create view
CREATE VIEW user_post_stats AS
SELECT 
    u.id,
    u.username,
    u.email,
    COUNT(p.id) as post_count,
    MAX(p.created_at) as latest_post
FROM users u
LEFT JOIN posts p ON u.id = p.author_id
GROUP BY u.id, u.username, u.email;

-- Use view
SELECT * FROM user_post_stats WHERE post_count > 5;

-- Update view
CREATE OR REPLACE VIEW user_post_stats AS
SELECT 
    u.id,
    u.username,
    COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.author_id
WHERE u.is_active = TRUE
GROUP BY u.id, u.username;

-- Drop view
DROP VIEW IF EXISTS user_post_stats;
```

### MySQL with Python

```python
import mysql.connector
from mysql.connector import Error

# Connect to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='appuser',
            password='password',
            database='myapp_db'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# READ - Select users
def get_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    return users

# WRITE - Insert user
def create_user(connection, username, email, password_hash):
    cursor = connection.cursor()
    query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
    values = (username, email, password_hash)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        user_id = cursor.lastrowid
        print(f"User created with ID: {user_id}")
        return user_id
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()

# UPDATE user
def update_user(connection, user_id, full_name):
    cursor = connection.cursor()
    query = "UPDATE users SET full_name = %s WHERE id = %s"
    values = (full_name, user_id)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        print(f"User {user_id} updated")
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()

# DELETE user
def delete_user(connection, user_id):
    cursor = connection.cursor()
    query = "DELETE FROM users WHERE id = %s"
    
    try:
        cursor.execute(query, (user_id,))
        connection.commit()
        print(f"User {user_id} deleted")
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()

# Transaction example
def transfer_money(connection, from_account, to_account, amount):
    cursor = connection.cursor()
    
    try:
        connection.start_transaction()
        
        # Deduct from sender
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE id = %s",
            (amount, from_account)
        )
        
        # Add to receiver
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE id = %s",
            (amount, to_account)
        )
        
        connection.commit()
        print("Transfer successful")
    except Error as e:
        connection.rollback()
        print(f"Transfer failed: {e}")
    finally:
        cursor.close()

# Usage
conn = create_connection()
if conn:
    users = get_users(conn)
    print(users)
    
    user_id = create_user(conn, 'newuser', 'new@example.com', 'hashed_pass')
    update_user(conn, user_id, 'New User')
    
    conn.close()
```

### MySQL Connection Pooling

```python
from mysql.connector import pooling

# Create connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    pool_reset_session=True,
    host='localhost',
    user='appuser',
    password='password',
    database='myapp_db'
)

# Get connection from pool
def get_connection_from_pool():
    return connection_pool.get_connection()

# Use connection
conn = get_connection_from_pool()
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
cursor.close()
conn.close()  # Returns connection to pool
```

---

## PostgreSQL

### Introduction
- **Type:** Object-Relational Database (ORDBMS)
- **License:** Open Source (PostgreSQL License)
- **Current Version:** 15+
- **ACID Compliance:** Full
- **Advanced Features:** JSON/JSONB, Arrays, Full-text search, GIS (PostGIS)
- **Use Cases:** Enterprise applications, GIS, Analytics, JSON data

### Installation

**Ubuntu/Debian:**
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Check status
sudo systemctl status postgresql

# Switch to postgres user
sudo -i -u postgres

# Access PostgreSQL
psql

# Or directly
sudo -u postgres psql
```

**Windows:**
```powershell
# Download installer from postgresql.org
# Run installer

# Add to PATH
$env:PATH += ";C:\Program Files\PostgreSQL\15\bin"

# Access PostgreSQL
psql -U postgres
```

**Docker:**
```bash
# Run PostgreSQL container
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -d postgres:15

# Connect
docker exec -it postgres-db psql -U postgres -d mydb
```

### Basic Configuration

```sql
-- Create database
CREATE DATABASE myapp_db;

-- Connect to database
\c myapp_db

-- Create user
CREATE USER appuser WITH PASSWORD 'strong_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE myapp_db TO appuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO appuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO appuser;

-- List databases
\l

-- List tables
\dt

-- Describe table
\d table_name

-- Quit
\q
```

### Data Types

```sql
-- Numeric Types
SMALLINT              -- 2 bytes
INTEGER / INT         -- 4 bytes
BIGINT                -- 8 bytes
DECIMAL(10,2)         -- Exact numeric
NUMERIC(10,2)         -- Same as DECIMAL
REAL                  -- 4 bytes float
DOUBLE PRECISION      -- 8 bytes float
SERIAL                -- Auto-incrementing integer
BIGSERIAL             -- Auto-incrementing bigint

-- String Types
CHAR(10)              -- Fixed length
VARCHAR(255)          -- Variable length
TEXT                  -- Unlimited length

-- Boolean
BOOLEAN               -- TRUE/FALSE

-- Date/Time
DATE                  -- Date only
TIME                  -- Time only
TIMESTAMP             -- Date and time
TIMESTAMPTZ           -- Timestamp with timezone
INTERVAL              -- Time interval

-- JSON
JSON                  -- JSON data (stored as text)
JSONB                 -- Binary JSON (faster, indexable)

-- Arrays
INTEGER[]             -- Array of integers
TEXT[]                -- Array of text

-- UUID
UUID                  -- Universally Unique Identifier

-- Network Types
INET                  -- IP address
CIDR                  -- Network address
MACADDR               -- MAC address

-- Geometric Types
POINT                 -- Point on plane
LINE                  -- Infinite line
POLYGON               -- Closed path

-- Range Types
INT4RANGE             -- Range of integers
TSRANGE               -- Range of timestamps
DATERANGE             -- Range of dates
```

### CREATE - Tables and Schemas

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}',
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);

-- Posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    published_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}',
    search_vector TSVECTOR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_author ON posts(author_id);
CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_posts_search ON posts USING GIN(search_vector);

-- Comments table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comments_post ON comments(post_id);
CREATE INDEX idx_comments_user ON comments(user_id);

-- Tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Post-Tags junction table
CREATE TABLE post_tags (
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (post_id, tag_id)
);

CREATE INDEX idx_post_tags_tag ON post_tags(tag_id);
```

### READ Operations

```sql
-- Basic SELECT
SELECT * FROM users;
SELECT id, username, email FROM users;

-- WHERE conditions
SELECT * FROM users WHERE is_active = TRUE;
SELECT * FROM users WHERE created_at > '2024-01-01';
SELECT * FROM users WHERE username ILIKE 'john%';  -- Case-insensitive

-- Multiple conditions
SELECT * FROM users 
WHERE is_active = TRUE 
AND created_at > '2024-01-01'
ORDER BY created_at DESC;

-- JSONB queries
SELECT * FROM users WHERE metadata->>'country' = 'USA';
SELECT * FROM users WHERE metadata @> '{"country": "USA"}';
SELECT * FROM users WHERE metadata ? 'phone';  -- Key exists

-- Array queries
SELECT * FROM users WHERE 'python' = ANY(tags);
SELECT * FROM users WHERE tags @> ARRAY['python', 'sql'];

-- Pattern matching
SELECT * FROM users WHERE email LIKE '%@gmail.com';
SELECT * FROM users WHERE email ~ '^[a-z]+@gmail\.com$';  -- Regex

-- Pagination with LIMIT and OFFSET
SELECT * FROM posts 
ORDER BY created_at DESC 
LIMIT 10 OFFSET 20;

-- Window functions
SELECT 
    username,
    created_at,
    ROW_NUMBER() OVER (ORDER BY created_at) as row_num,
    RANK() OVER (ORDER BY created_at) as rank,
    DENSE_RANK() OVER (ORDER BY created_at) as dense_rank
FROM users;

-- Partition window functions
SELECT 
    p.title,
    u.username,
    p.created_at,
    ROW_NUMBER() OVER (PARTITION BY p.author_id ORDER BY p.created_at DESC) as post_rank
FROM posts p
JOIN users u ON p.author_id = u.id;

-- Common Table Expressions (CTE)
WITH active_users AS (
    SELECT id, username FROM users WHERE is_active = TRUE
)
SELECT au.username, COUNT(p.id) as post_count
FROM active_users au
LEFT JOIN posts p ON au.id = p.author_id
GROUP BY au.username;

-- Recursive CTE (hierarchical data)
WITH RECURSIVE category_tree AS (
    -- Base case
    SELECT id, name, parent_id, 1 as level
    FROM categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive case
    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree;

-- Full-text search
SELECT * FROM posts 
WHERE search_vector @@ to_tsquery('english', 'postgresql & python');

-- DISTINCT ON (PostgreSQL specific)
SELECT DISTINCT ON (author_id) *
FROM posts
ORDER BY author_id, created_at DESC;

-- JOINS
SELECT u.username, p.title, p.created_at
FROM users u
INNER JOIN posts p ON u.id = p.author_id
WHERE p.status = 'published'
ORDER BY p.created_at DESC;

-- Aggregate functions
SELECT 
    status,
    COUNT(*) as count,
    AVG(LENGTH(content)) as avg_length
FROM posts
GROUP BY status;

-- HAVING clause
SELECT author_id, COUNT(*) as post_count
FROM posts
GROUP BY author_id
HAVING COUNT(*) > 5
ORDER BY post_count DESC;

-- LATERAL JOIN (like CROSS APPLY in SQL Server)
SELECT u.username, recent_posts.*
FROM users u
LEFT JOIN LATERAL (
    SELECT title, created_at
    FROM posts
    WHERE author_id = u.id
    ORDER BY created_at DESC
    LIMIT 3
) recent_posts ON TRUE;
```

### WRITE Operations

```sql
-- INSERT single row
INSERT INTO users (username, email, password_hash, full_name)
VALUES ('johndoe', 'john@example.com', 'hashed_password', 'John Doe');

-- INSERT multiple rows
INSERT INTO users (username, email, password_hash) VALUES
('user1', 'user1@example.com', 'hash1'),
('user2', 'user2@example.com', 'hash2'),
('user3', 'user3@example.com', 'hash3');

-- INSERT with RETURNING (PostgreSQL specific)
INSERT INTO users (username, email, password_hash)
VALUES ('newuser', 'new@example.com', 'hash')
RETURNING id, username, created_at;

-- INSERT with JSONB
INSERT INTO users (username, email, password_hash, metadata)
VALUES ('user', 'user@example.com', 'hash', '{"country": "USA", "age": 25}');

-- INSERT with array
INSERT INTO users (username, email, password_hash, tags)
VALUES ('user', 'user@example.com', 'hash', ARRAY['python', 'sql', 'javascript']);

-- INSERT ... ON CONFLICT (UPSERT)
INSERT INTO users (username, email, password_hash)
VALUES ('johndoe', 'john@example.com', 'new_hash')
ON CONFLICT (username) 
DO UPDATE SET 
    password_hash = EXCLUDED.password_hash,
    updated_at = CURRENT_TIMESTAMP;

-- INSERT ... ON CONFLICT DO NOTHING
INSERT INTO users (username, email, password_hash)
VALUES ('johndoe', 'john@example.com', 'hash')
ON CONFLICT (username) DO NOTHING;

-- UPDATE single row
UPDATE users 
SET full_name = 'John Smith', updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- UPDATE with JSONB
UPDATE users 
SET metadata = metadata || '{"verified": true}'
WHERE id = 1;

-- UPDATE array (add element)
UPDATE users 
SET tags = array_append(tags, 'new_tag')
WHERE id = 1;

-- UPDATE with RETURNING
UPDATE users 
SET is_active = FALSE
WHERE id = 1
RETURNING id, username, is_active;

-- UPDATE with JOIN
UPDATE posts p
SET status = 'archived'
FROM users u
WHERE p.author_id = u.id AND u.is_active = FALSE;

-- DELETE single row
DELETE FROM users WHERE id = 1;

-- DELETE with RETURNING
DELETE FROM users 
WHERE id = 1
RETURNING id, username;

-- DELETE with JOIN
DELETE FROM posts p
USING users u
WHERE p.author_id = u.id AND u.is_active = FALSE;
```

### Transactions

```sql
-- Start transaction
BEGIN;

-- Multiple operations
INSERT INTO users (username, email, password_hash) 
VALUES ('newuser', 'new@example.com', 'hash')
RETURNING id INTO user_id;

INSERT INTO posts (title, content, author_id)
VALUES ('First Post', 'Content here', user_id);

-- Commit
COMMIT;

-- Rollback
ROLLBACK;

-- Savepoints
BEGIN;
INSERT INTO users (username, email, password_hash) VALUES ('user1', 'user1@example.com', 'hash1');
SAVEPOINT sp1;
INSERT INTO users (username, email, password_hash) VALUES ('user2', 'user2@example.com', 'hash2');
ROLLBACK TO SAVEPOINT sp1;  -- Rollback to savepoint
COMMIT;
```

### PostgreSQL with Python (psycopg2)

```python
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from psycopg2.pool import SimpleConnectionPool

# Connect to PostgreSQL
def create_connection():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='appuser',
            password='password',
            database='myapp_db',
            port='5432'
        )
        print("Connected to PostgreSQL")
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

# READ - Select users
def get_users(connection):
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    return users

# WRITE - Insert user with RETURNING
def create_user(connection, username, email, password_hash):
    cursor = connection.cursor()
    query = """
        INSERT INTO users (username, email, password_hash) 
        VALUES (%s, %s, %s)
        RETURNING id, username, created_at
    """
    
    try:
        cursor.execute(query, (username, email, password_hash))
        user = cursor.fetchone()
        connection.commit()
        print(f"User created: {user}")
        return user
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()

# Bulk insert with execute_values
def bulk_insert_users(connection, users):
    cursor = connection.cursor()
    query = "INSERT INTO users (username, email, password_hash) VALUES %s"
    
    try:
        execute_values(cursor, query, users)
        connection.commit()
        print(f"{len(users)} users inserted")
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()

# UPSERT example
def upsert_user(connection, username, email, password_hash):
    cursor = connection.cursor()
    query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        ON CONFLICT (username)
        DO UPDATE SET 
            password_hash = EXCLUDED.password_hash,
            updated_at = CURRENT_TIMESTAMP
        RETURNING id
    """
    
    try:
        cursor.execute(query, (username, email, password_hash))
        user_id = cursor.fetchone()[0]
        connection.commit()
        return user_id
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()

# Connection Pool
connection_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host='localhost',
    user='appuser',
    password='password',
    database='myapp_db'
)

def get_connection_from_pool():
    return connection_pool.getconn()

def return_connection_to_pool(connection):
    connection_pool.putconn(connection)

# Usage
conn = get_connection_from_pool()
users = get_users(conn)
print(users)
return_connection_to_pool(conn)
```

### PostgreSQL Advanced Features

```sql
-- JSONB Operations
-- Create table with JSONB
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    attributes JSONB
);

-- Insert with JSONB
INSERT INTO products (name, attributes) VALUES
('Laptop', '{"brand": "Dell", "ram": 16, "storage": 512, "ports": ["USB-C", "HDMI"]}'),
('Phone', '{"brand": "Apple", "storage": 256, "camera": {"front": 12, "back": 48}}');

-- Query JSONB
SELECT * FROM products WHERE attributes->>'brand' = 'Dell';
SELECT * FROM products WHERE (attributes->>'ram')::int > 8;
SELECT * FROM products WHERE attributes @> '{"brand": "Dell"}';
SELECT * FROM products WHERE attributes->'ports' @> '["HDMI"]';

-- Update JSONB
UPDATE products 
SET attributes = attributes || '{"warranty": "2 years"}'
WHERE id = 1;

-- Remove JSONB key
UPDATE products 
SET attributes = attributes - 'warranty'
WHERE id = 1;

-- Full-text Search
-- Create full-text search
ALTER TABLE posts ADD COLUMN search_vector TSVECTOR;

-- Update search vector
UPDATE posts 
SET search_vector = to_tsvector('english', title || ' ' || content);

-- Create index
CREATE INDEX idx_posts_search ON posts USING GIN(search_vector);

-- Search
SELECT * FROM posts 
WHERE search_vector @@ to_tsquery('english', 'postgresql & (tutorial | guide)');

-- Rank results
SELECT 
    title,
    ts_rank(search_vector, to_tsquery('english', 'postgresql')) as rank
FROM posts
WHERE search_vector @@ to_tsquery('english', 'postgresql')
ORDER BY rank DESC;

-- Array Operations
SELECT * FROM users WHERE 'python' = ANY(tags);
SELECT * FROM users WHERE tags && ARRAY['python', 'sql'];  -- Overlaps
SELECT * FROM users WHERE tags @> ARRAY['python'];  -- Contains
SELECT array_length(tags, 1) FROM users;
SELECT array_append(tags, 'new_tag') FROM users;
SELECT unnest(tags) as tag FROM users;  -- Explode array
```

---

## MongoDB (NoSQL)

### Introduction
- **Type:** Document-oriented NoSQL Database
- **Data Model:** JSON-like documents (BSON)
- **Schema:** Flexible/Dynamic schema
- **Scalability:** Horizontal (sharding)
- **Consistency:** Eventual consistency (configurable)
- **Use Cases:** Content management, real-time analytics, IoT, mobile apps

### Installation

**Ubuntu/Debian:**
```bash
# Import MongoDB GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Check status
sudo systemctl status mongod

# Connect to MongoDB
mongosh
```

**Windows:**
```powershell
# Download MongoDB installer from mongodb.com
# Run installer

# Start MongoDB service
net start MongoDB

# Connect to MongoDB
mongosh
```

**Docker:**
```bash
# Run MongoDB container
docker run --name mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -p 27017:27017 \
  -d mongo:6.0

# Connect to MongoDB
docker exec -it mongodb mongosh -u admin -p password
```

### Basic Commands

```javascript
// Show databases
show dbs

// Create/Use database
use myapp_db

// Show collections
show collections

// Drop database
db.dropDatabase()

// Drop collection
db.users.drop()

// Get collection stats
db.users.stats()
```

### Data Modeling

```javascript
// Users collection
{
  _id: ObjectId("507f1f77bcf86cd799439011"),
  username: "johndoe",
  email: "john@example.com",
  password_hash: "hashed_password",
  profile: {
    full_name: "John Doe",
    age: 30,
    address: {
      street: "123 Main St",
      city: "New York",
      country: "USA"
    }
  },
  tags: ["developer", "python", "mongodb"],
  is_active: true,
  created_at: ISODate("2024-01-15T10:30:00Z"),
  updated_at: ISODate("2024-01-15T10:30:00Z")
}

// Posts collection (embedded comments)
{
  _id: ObjectId("507f1f77bcf86cd799439012"),
  title: "Introduction to MongoDB",
  content: "MongoDB is a NoSQL database...",
  author_id: ObjectId("507f1f77bcf86cd799439011"),
  status: "published",
  tags: ["mongodb", "nosql", "database"],
  comments: [
    {
      _id: ObjectId("507f1f77bcf86cd799439013"),
      user_id: ObjectId("507f1f77bcf86cd799439014"),
      content: "Great post!",
      created_at: ISODate("2024-01-16T10:30:00Z")
    }
  ],
  stats: {
    views: 1500,
    likes: 45,
    shares: 12
  },
  published_at: ISODate("2024-01-15T12:00:00Z"),
  created_at: ISODate("2024-01-15T10:30:00Z"),
  updated_at: ISODate("2024-01-15T10:30:00Z")
}
```

### CREATE Operations

```javascript
// Insert single document
db.users.insertOne({
  username: "johndoe",
  email: "john@example.com",
  password_hash: "hashed_password",
  profile: {
    full_name: "John Doe",
    age: 30
  },
  tags: ["developer", "python"],
  is_active: true,
  created_at: new Date()
})

// Insert multiple documents
db.users.insertMany([
  {
    username: "user1",
    email: "user1@example.com",
    password_hash: "hash1",
    created_at: new Date()
  },
  {
    username: "user2",
    email: "user2@example.com",
    password_hash: "hash2",
    created_at: new Date()
  }
])

// Insert with custom _id
db.users.insertOne({
  _id: "custom-id-123",
  username: "customuser",
  email: "custom@example.com"
})
```

### READ Operations

```javascript
// Find all documents
db.users.find()

// Find with pretty print
db.users.find().pretty()

// Find specific fields (projection)
db.users.find({}, { username: 1, email: 1, _id: 0 })

// Find one document
db.users.findOne({ username: "johndoe" })

// Find with conditions
db.users.find({ is_active: true })
db.users.find({ "profile.age": { $gte: 18 } })
db.users.find({ tags: "python" })
db.users.find({ tags: { $in: ["python", "javascript"] } })

// Multiple conditions (AND)
db.users.find({
  is_active: true,
  "profile.age": { $gte: 18 }
})

// OR conditions
db.users.find({
  $or: [
    { username: "johndoe" },
    { email: "john@example.com" }
  ]
})

// NOT conditions
db.users.find({ is_active: { $ne: false } })

// Regular expressions
db.users.find({ email: /gmail\.com$/ })
db.users.find({ username: { $regex: "^john", $options: "i" } })

// Array queries
db.users.find({ tags: { $all: ["python", "mongodb"] } })
db.users.find({ tags: { $size: 3 } })

// Nested document queries
db.users.find({ "profile.address.city": "New York" })

// Exists
db.users.find({ "profile.phone": { $exists: true } })

// Comparison operators
db.posts.find({ "stats.views": { $gt: 1000 } })
db.posts.find({ "stats.views": { $gte: 1000, $lte: 5000 } })

// Sorting
db.users.find().sort({ created_at: -1 })  // -1 = descending
db.users.find().sort({ username: 1 })     // 1 = ascending

// Pagination (limit & skip)
db.users.find().limit(10)
db.users.find().skip(20).limit(10)  // Page 3

// Count
db.users.countDocuments()
db.users.countDocuments({ is_active: true })

// Distinct
db.users.distinct("tags")
db.posts.distinct("status")

// Aggregation Pipeline
db.posts.aggregate([
  { $match: { status: "published" } },
  { $group: {
    _id: "$author_id",
    post_count: { $sum: 1 },
    total_views: { $sum: "$stats.views" }
  }},
  { $sort: { post_count: -1 } },
  { $limit: 10 }
])

// Lookup (join)
db.posts.aggregate([
  {
    $lookup: {
      from: "users",
      localField: "author_id",
      foreignField: "_id",
      as: "author"
    }
  },
  { $unwind: "$author" },
  {
    $project: {
      title: 1,
      "author.username": 1,
      "author.email": 1
    }
  }
])

// Group by with multiple operations
db.posts.aggregate([
  {
    $group: {
      _id: "$status",
      count: { $sum: 1 },
      avg_views: { $avg: "$stats.views" },
      max_views: { $max: "$stats.views" },
      min_views: { $min: "$stats.views" }
    }
  }
])

// Unwind array
db.posts.aggregate([
  { $unwind: "$tags" },
  { $group: { _id: "$tags", count: { $sum: 1 } }},
  { $sort: { count: -1 } }
])
```

### UPDATE Operations

```javascript
// Update single document
db.users.updateOne(
  { username: "johndoe" },
  { $set: { "profile.full_name": "John Smith" } }
)

// Update multiple documents
db.users.updateMany(
  { is_active: false },
  { $set: { status: "inactive" } }
)

// Replace entire document
db.users.replaceOne(
  { username: "johndoe" },
  {
    username: "johndoe",
    email: "john@example.com",
    is_active: true
  }
)

// Update operators
// $set - Set field value
db.users.updateOne(
  { username: "johndoe" },
  { $set: { is_active: false, updated_at: new Date() } }
)

// $unset - Remove field
db.users.updateOne(
  { username: "johndoe" },
  { $unset: { temp_field: "" } }
)

// $inc - Increment value
db.posts.updateOne(
  { _id: ObjectId("...") },
  { $inc: { "stats.views": 1 } }
)

// $mul - Multiply value
db.products.updateOne(
  { _id: ObjectId("...") },
  { $mul: { price: 1.1 } }  // Increase by 10%
)

// $push - Add to array
db.users.updateOne(
  { username: "johndoe" },
  { $push: { tags: "new_tag" } }
)

// $addToSet - Add to array (if not exists)
db.users.updateOne(
  { username: "johndoe" },
  { $addToSet: { tags: "unique_tag" } }
)

// $pull - Remove from array
db.users.updateOne(
  { username: "johndoe" },
  { $pull: { tags: "old_tag" } }
)

// $pop - Remove first or last element
db.users.updateOne(
  { username: "johndoe" },
  { $pop: { tags: 1 } }  // 1 = last, -1 = first
)

// Update nested document
db.users.updateOne(
  { username: "johndoe" },
  { $set: { "profile.address.city": "Los Angeles" } }
)

// Update array element
db.posts.updateOne(
  { _id: ObjectId("..."), "comments._id": ObjectId("...") },
  { $set: { "comments.$.content": "Updated comment" } }
)

// Upsert (update or insert)
db.users.updateOne(
  { username: "newuser" },
  { $set: { email: "new@example.com", created_at: new Date() } },
  { upsert: true }
)

// Update with current date
db.users.updateOne(
  { username: "johndoe" },
  { $currentDate: { updated_at: true } }
)

// Bulk update
db.users.bulkWrite([
  {
    updateOne: {
      filter: { username: "user1" },
      update: { $set: { is_active: false } }
    }
  },
  {
    updateOne: {
      filter: { username: "user2" },
      update: { $set: { is_active: true } }
    }
  }
])
```

### DELETE Operations

```javascript
// Delete single document
db.users.deleteOne({ username: "johndoe" })

// Delete multiple documents
db.users.deleteMany({ is_active: false })

// Delete all documents
db.users.deleteMany({})

// Delete with condition
db.posts.deleteMany({ status: "draft", created_at: { $lt: new Date("2024-01-01") } })
```

### Indexes

```javascript
// Create single field index
db.users.createIndex({ email: 1 })  // 1 = ascending
db.users.createIndex({ username: -1 })  // -1 = descending

// Create compound index
db.users.createIndex({ username: 1, email: 1 })

// Create unique index
db.users.createIndex({ email: 1 }, { unique: true })

// Create text index for full-text search
db.posts.createIndex({ title: "text", content: "text" })

// Search with text index
db.posts.find({ $text: { $search: "mongodb tutorial" } })

// Text search with score
db.posts.find(
  { $text: { $search: "mongodb" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } })

// Create TTL index (auto-delete after time)
db.sessions.createIndex({ created_at: 1 }, { expireAfterSeconds: 3600 })

// Create partial index
db.users.createIndex(
  { email: 1 },
  { partialFilterExpression: { is_active: true } }
)

// List indexes
db.users.getIndexes()

// Drop index
db.users.dropIndex("email_1")
db.users.dropIndex({ email: 1 })

// Drop all indexes (except _id)
db.users.dropIndexes()

// Explain query plan
db.users.find({ email: "john@example.com" }).explain("executionStats")
```

### MongoDB with Python (PyMongo)

```python
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
from bson.objectid import ObjectId
from datetime import datetime

# Connect to MongoDB
def create_connection():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['myapp_db']
        print("Connected to MongoDB")
        return db
    except Exception as e:
        print(f"Error: {e}")
        return None

# READ - Find users
def get_users(db):
    users = list(db.users.find({}, {'password_hash': 0}))
    return users

# READ - Find one user
def get_user_by_username(db, username):
    user = db.users.find_one({'username': username}, {'password_hash': 0})
    return user

# WRITE - Insert user
def create_user(db, username, email, password_hash):
    user = {
        'username': username,
        'email': email,
        'password_hash': password_hash,
        'is_active': True,
        'created_at': datetime.utcnow()
    }
    
    try:
        result = db.users.insert_one(user)
        print(f"User created with ID: {result.inserted_id}")
        return result.inserted_id
    except DuplicateKeyError:
        print("User already exists")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# UPDATE user
def update_user(db, user_id, full_name):
    try:
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'profile.full_name': full_name,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        print(f"Modified {result.modified_count} document(s)")
        return result.modified_count
    except Exception as e:
        print(f"Error: {e}")
        return 0

# DELETE user
def delete_user(db, user_id):
    try:
        result = db.users.delete_one({'_id': ObjectId(user_id)})
        print(f"Deleted {result.deleted_count} document(s)")
        return result.deleted_count
    except Exception as e:
        print(f"Error: {e}")
        return 0

# Aggregation
def get_user_post_stats(db):
    pipeline = [
        {
            '$lookup': {
                'from': 'posts',
                'localField': '_id',
                'foreignField': 'author_id',
                'as': 'posts'
            }
        },
        {
            '$project': {
                'username': 1,
                'email': 1,
                'post_count': {'$size': '$posts'}
            }
        },
        {
            '$sort': {'post_count': -1}
        }
    ]
    
    results = list(db.users.aggregate(pipeline))
    return results

# Bulk operations
def bulk_insert_users(db, users):
    try:
        result = db.users.insert_many(users, ordered=False)
        print(f"Inserted {len(result.inserted_ids)} users")
        return result.inserted_ids
    except Exception as e:
        print(f"Error: {e}")
        return []

# Usage
db = create_connection()
if db:
    # Create unique indexes
    db.users.create_index('username', unique=True)
    db.users.create_index('email', unique=True)
    
    # CRUD operations
    user_id = create_user(db, 'johndoe', 'john@example.com', 'hashed_pass')
    users = get_users(db)
    print(users)
    
    update_user(db, str(user_id), 'John Doe')
    
    stats = get_user_post_stats(db)
    print(stats)
```

### MongoDB Transactions (Replica Set Required)

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/?replicaSet=rs0')
db = client['myapp_db']

# Start session
with client.start_session() as session:
    with session.start_transaction():
        try:
            # Multiple operations in transaction
            db.accounts.update_one(
                {'_id': ObjectId('account1')},
                {'$inc': {'balance': -100}},
                session=session
            )
            
            db.accounts.update_one(
                {'_id': ObjectId('account2')},
                {'$inc': {'balance': 100}},
                session=session
            )
            
            # Commit transaction
            session.commit_transaction()
            print("Transaction successful")
        except Exception as e:
            # Rollback on error
            session.abort_transaction()
            print(f"Transaction failed: {e}")
```

---

## Redis (NoSQL)

### Introduction
- **Type:** In-memory Key-Value Store
- **Data Structures:** Strings, Lists, Sets, Sorted Sets, Hashes, Bitmaps, HyperLogLogs, Streams
- **Persistence:** Optional (RDB snapshots, AOF logs)
- **Use Cases:** Caching, Session storage, Real-time analytics, Message queues, Leaderboards

### Installation

**Ubuntu/Debian:**
```bash
# Install Redis
sudo apt update
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Check status
sudo systemctl status redis-server

# Connect to Redis
redis-cli

# Test
ping
# Response: PONG
```

**Windows:**
```powershell
# Download Redis for Windows from GitHub (tporadowski/redis)
# Or use WSL

# Start Redis
redis-server

# Connect
redis-cli
```

**Docker:**
```bash
# Run Redis container
docker run --name redis-db \
  -p 6379:6379 \
  -d redis:7

# Connect
docker exec -it redis-db redis-cli
```

### Basic Commands

```bash
# Strings
SET key "value"
GET key
SET name "John Doe"
GET name
MSET key1 "value1" key2 "value2" key3 "value3"
MGET key1 key2 key3

# Set with expiration (seconds)
SETEX session:123 3600 "user_data"  # Expires in 1 hour
SET cache:user:1 "data" EX 3600

# Increment/Decrement
SET counter 0
INCR counter          # Returns 1
INCRBY counter 5      # Returns 6
DECR counter          # Returns 5
DECRBY counter 2      # Returns 3

# Check if key exists
EXISTS name
EXISTS key1 key2 key3  # Returns count of existing keys

# Delete keys
DEL key
DEL key1 key2 key3

# Set expiration
EXPIRE key 60         # Expires in 60 seconds
TTL key               # Check remaining time
PERSIST key           # Remove expiration

# Rename key
RENAME oldkey newkey

# Get all keys (DANGEROUS in production!)
KEYS *
KEYS user:*

# Scan keys (better for production)
SCAN 0 MATCH user:* COUNT 10

# Lists (like arrays)
LPUSH mylist "item1"           # Add to left (head)
RPUSH mylist "item2"           # Add to right (tail)
LPUSH mylist "item3" "item4"   # Add multiple
LRANGE mylist 0 -1             # Get all items
LRANGE mylist 0 10             # Get first 10 items
LPOP mylist                    # Remove and return first item
RPOP mylist                    # Remove and return last item
LLEN mylist                    # Get list length
LINDEX mylist 0                # Get item at index

# Sets (unique items)
SADD myset "member1"
SADD myset "member2" "member3"
SMEMBERS myset                 # Get all members
SISMEMBER myset "member1"      # Check if member exists
SCARD myset                    # Get set size
SREM myset "member1"           # Remove member
SPOP myset                     # Remove and return random member

# Set operations
SADD set1 "a" "b" "c"
SADD set2 "b" "c" "d"
SINTER set1 set2               # Intersection: b, c
SUNION set1 set2               # Union: a, b, c, d
SDIFF set1 set2                # Difference: a

# Sorted Sets (with scores)
ZADD leaderboard 100 "player1"
ZADD leaderboard 200 "player2" 150 "player3"
ZRANGE leaderboard 0 -1        # Get all (ascending)
ZREVRANGE leaderboard 0 -1     # Get all (descending)
ZRANGE leaderboard 0 -1 WITHSCORES
ZRANK leaderboard "player1"    # Get rank (0-indexed)
ZSCORE leaderboard "player1"   # Get score
ZINCRBY leaderboard 10 "player1"  # Increment score
ZCARD leaderboard              # Get count
ZREM leaderboard "player1"     # Remove member

# Get top 10
ZREVRANGE leaderboard 0 9 WITHSCORES

# Get by score range
ZRANGEBYSCORE leaderboard 100 200

# Hashes (like dictionaries/objects)
HSET user:1 name "John Doe"
HSET user:1 email "john@example.com" age 30
HGET user:1 name
HGETALL user:1                 # Get all fields
HMGET user:1 name email        # Get multiple fields
HDEL user:1 age                # Delete field
HEXISTS user:1 name            # Check if field exists
HKEYS user:1                   # Get all field names
HVALS user:1                   # Get all values
HLEN user:1                    # Get number of fields
HINCRBY user:1 age 1           # Increment field value

# Database selection (Redis has 16 databases by default)
SELECT 0                       # Database 0 (default)
SELECT 1                       # Database 1

# Flush database
FLUSHDB                        # Clear current database
FLUSHALL                       # Clear all databases (DANGEROUS!)

# Info and stats
INFO
INFO memory
INFO stats
DBSIZE                         # Number of keys

# Save database
SAVE                           # Synchronous save
BGSAVE                         # Background save
```

### Caching Patterns

```bash
# Cache-aside pattern
# 1. Check cache
GET cache:user:123

# 2. If miss, get from database and set cache
SET cache:user:123 '{"name":"John","email":"john@example.com"}' EX 3600

# Write-through pattern
# Update both cache and database
SET cache:user:123 '{"name":"John Smith","email":"john@example.com"}' EX 3600

# Cache with JSON
SET user:1 '{"id":1,"name":"John","email":"john@example.com","active":true}' EX 3600
```

### Redis with Python

```python
import redis
import json
from datetime import timedelta

# Connect to Redis
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True  # Automatically decode bytes to strings
)

# Test connection
try:
    r.ping()
    print("Connected to Redis")
except redis.ConnectionError:
    print("Failed to connect to Redis")

# Strings
r.set('name', 'John Doe')
name = r.get('name')
print(name)

# Set with expiration
r.setex('session:123', timedelta(hours=1), 'user_data')
r.set('cache:user:1', 'data', ex=3600)  # Alternative syntax

# Increment
r.set('counter', 0)
r.incr('counter')
r.incrby('counter', 5)
print(r.get('counter'))

# Check existence
exists = r.exists('name')
print(f"Key exists: {exists}")

# Delete
r.delete('name')

# Multiple operations
r.mset({'key1': 'value1', 'key2': 'value2', 'key3': 'value3'})
values = r.mget('key1', 'key2', 'key3')
print(values)

# Lists
r.lpush('mylist', 'item1', 'item2', 'item3')
r.rpush('mylist', 'item4')
items = r.lrange('mylist', 0, -1)
print(items)

# Sets
r.sadd('myset', 'member1', 'member2', 'member3')
members = r.smembers('myset')
print(members)

is_member = r.sismember('myset', 'member1')
print(f"Is member: {is_member}")

# Sorted Sets (leaderboard)
r.zadd('leaderboard', {'player1': 100, 'player2': 200, 'player3': 150})
r.zincrby('leaderboard', 10, 'player1')

# Get top 10
top_players = r.zrevrange('leaderboard', 0, 9, withscores=True)
print(top_players)

# Hashes
r.hset('user:1', mapping={
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
})

user = r.hgetall('user:1')
print(user)

name = r.hget('user:1', 'name')
print(name)

# Store JSON in cache
user_data = {
    'id': 1,
    'name': 'John Doe',
    'email': 'john@example.com'
}

r.set('cache:user:1', json.dumps(user_data), ex=3600)
cached_data = json.loads(r.get('cache:user:1'))
print(cached_data)

# Pipeline (batch operations)
pipe = r.pipeline()
pipe.set('key1', 'value1')
pipe.set('key2', 'value2')
pipe.incr('counter')
pipe.execute()

# Pub/Sub (simple example)
def message_handler(message):
    print(f"Received: {message['data']}")

# Subscribe (in separate thread/process)
pubsub = r.pubsub()
pubsub.subscribe('news')

# Publish
r.publish('news', 'Breaking news!')

# Cache decorator
def cache_result(key, ttl=3600):
    def decorator(func):
        def wrapper(*args, **kwargs):
            cached = r.get(key)
            if cached:
                return json.loads(cached)
            
            result = func(*args, **kwargs)
            r.set(key, json.dumps(result), ex=ttl)
            return result
        return wrapper
    return decorator

@cache_result('expensive_operation', ttl=3600)
def expensive_operation():
    # Simulate expensive operation
    return {'result': 'computed value'}
```

### Redis Connection Pool

```python
import redis

# Create connection pool
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=10,
    decode_responses=True
)

# Get connection from pool
r = redis.Redis(connection_pool=pool)

# Use connection
r.set('key', 'value')
value = r.get('key')

# Connection is automatically returned to pool
```

---

## Cassandra (NoSQL)

### Introduction
- **Type:** Wide-column store (Column-family)
- **Architecture:** Distributed, peer-to-peer
- **Consistency:** Tunable consistency (AP in CAP theorem)
- **Scalability:** Linear horizontal scaling
- **No Single Point of Failure**
- **Use Cases:** Time-series data, IoT, messaging, analytics

### Key Concepts

**Keyspace:** Like a database in SQL
**Table:** Like a table in SQL
**Partition Key:** Determines data distribution
**Clustering Key:** Determines data ordering within partition
**Replication Factor:** Number of copies of data

### Installation

**Ubuntu/Debian:**
```bash
# Add Cassandra repository
echo "deb https://debian.cassandra.apache.org 41x main" | sudo tee /etc/apt/sources.list.d/cassandra.list
wget -q -O - https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -

# Install Cassandra
sudo apt update
sudo apt install cassandra

# Start Cassandra
sudo systemctl start cassandra
sudo systemctl enable cassandra

# Check status
sudo systemctl status cassandra

# Connect to Cassandra
cqlsh
```

**Docker:**
```bash
# Run Cassandra container
docker run --name cassandra-db \
  -p 9042:9042 \
  -d cassandra:4.1

# Connect
docker exec -it cassandra-db cqlsh
```

### CQL (Cassandra Query Language)

```sql
-- Create keyspace
CREATE KEYSPACE myapp_db
WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 3
};

-- Use keyspace
USE myapp_db;

-- Create table with partition key
CREATE TABLE users (
  user_id UUID PRIMARY KEY,
  username TEXT,
  email TEXT,
  created_at TIMESTAMP
);

-- Create table with composite primary key
CREATE TABLE posts (
  post_id UUID,
  author_id UUID,
  title TEXT,
  content TEXT,
  created_at TIMESTAMP,
  PRIMARY KEY (author_id, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);

-- Create table with partition key and clustering key
CREATE TABLE time_series_data (
  sensor_id UUID,
  timestamp TIMESTAMP,
  temperature DOUBLE,
  humidity DOUBLE,
  PRIMARY KEY (sensor_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Create secondary index
CREATE INDEX ON users (username);
CREATE INDEX ON users (email);

-- INSERT
INSERT INTO users (user_id, username, email, created_at)
VALUES (uuid(), 'johndoe', 'john@example.com', toTimestamp(now()));

-- INSERT with TTL (time to live)
INSERT INTO sessions (session_id, user_id, data)
VALUES (uuid(), uuid(), 'session_data')
USING TTL 3600;  -- Expires in 1 hour

-- SELECT
SELECT * FROM users;
SELECT * FROM users WHERE user_id = uuid;
SELECT * FROM posts WHERE author_id = uuid;
SELECT * FROM posts WHERE author_id = uuid AND created_at > '2024-01-01';

-- UPDATE
UPDATE users
SET email = 'newemail@example.com'
WHERE user_id = uuid;

-- UPDATE with counter
CREATE TABLE post_stats (
  post_id UUID PRIMARY KEY,
  views COUNTER
);

UPDATE post_stats SET views = views + 1 WHERE post_id = uuid;

-- DELETE
DELETE FROM users WHERE user_id = uuid;

-- DELETE column
DELETE email FROM users WHERE user_id = uuid;

-- Batch operations
BEGIN BATCH
  INSERT INTO users (user_id, username, email) VALUES (uuid(), 'user1', 'user1@example.com');
  INSERT INTO posts (post_id, author_id, title) VALUES (uuid(), uuid(), 'Post 1');
  UPDATE users SET email = 'updated@example.com' WHERE user_id = uuid;
APPLY BATCH;

-- Drop table
DROP TABLE users;

-- Drop keyspace
DROP KEYSPACE myapp_db;
```

### Cassandra with Python

```python
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import uuid4
from datetime import datetime

# Connect to Cassandra
cluster = Cluster(['localhost'], port=9042)
session = cluster.connect()

# Create keyspace
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS myapp_db
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
""")

# Use keyspace
session.set_keyspace('myapp_db')

# Create table
session.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY,
        username TEXT,
        email TEXT,
        created_at TIMESTAMP
    )
""")

# Insert data
user_id = uuid4()
session.execute("""
    INSERT INTO users (user_id, username, email, created_at)
    VALUES (%s, %s, %s, %s)
""", (user_id, 'johndoe', 'john@example.com', datetime.now()))

# Prepared statements (better performance)
prepared = session.prepare("""
    INSERT INTO users (user_id, username, email, created_at)
    VALUES (?, ?, ?, ?)
""")

session.execute(prepared, (uuid4(), 'user1', 'user1@example.com', datetime.now()))

# Query data
rows = session.execute("SELECT * FROM users")
for row in rows:
    print(row.user_id, row.username, row.email)

# Query with parameters
rows = session.execute(
    "SELECT * FROM users WHERE user_id = %s",
    (user_id,)
)

# Close connection
cluster.shutdown()
```

---

## Read vs Write Operations

### Read-Heavy vs Write-Heavy Applications

| Aspect | Read-Heavy | Write-Heavy |
|--------|------------|-------------|
| **Examples** | News sites, blogs, catalogs | Social media, IoT sensors, logging |
| **Optimization Focus** | Caching, read replicas, indexes | Write buffers, batch writes, sharding |
| **Database Choice** | PostgreSQL, MySQL with replicas | Cassandra, MongoDB, time-series DBs |
| **Caching Strategy** | Aggressive caching (Redis) | Write-through, write-behind |
| **Replication** | Multiple read replicas | Multi-master or eventual consistency |
| **Consistency** | Strong consistency acceptable | Eventual consistency often OK |

### Read Operations Optimization

**1. Database Indexes**
```sql
-- MySQL/PostgreSQL
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_post_author_status ON posts(author_id, status);

-- Covering index (includes all needed columns)
CREATE INDEX idx_posts_covering ON posts(author_id, status) INCLUDE (title, created_at);

-- Partial index (PostgreSQL)
CREATE INDEX idx_active_users ON users(email) WHERE is_active = TRUE;
```

**2. Query Optimization**
```sql
-- BAD: N+1 query problem
SELECT * FROM posts;
-- Then for each post:
SELECT * FROM users WHERE id = post.author_id;

-- GOOD: Join in single query
SELECT p.*, u.username, u.email
FROM posts p
INNER JOIN users u ON p.author_id = u.id;

-- Use EXPLAIN to analyze
EXPLAIN ANALYZE SELECT * FROM posts WHERE author_id = 123;
```

**3. Caching Layer (Redis)**
```python
import redis
import json

r = redis.Redis(decode_responses=True)

def get_user(user_id):
    # Try cache first
    cache_key = f'user:{user_id}'
    cached = r.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    # Cache miss - query database
    user = db.query(User).filter(User.id == user_id).first()
    
    # Store in cache (1 hour TTL)
    r.setex(cache_key, 3600, json.dumps(user))
    
    return user

def invalidate_user_cache(user_id):
    r.delete(f'user:{user_id}')
```

**4. Read Replicas**
```python
# Django example with read replicas
class MyRouter:
    def db_for_read(self, model, **hints):
        return 'replica'  # Route reads to replica
    
    def db_for_write(self, model, **hints):
        return 'default'  # Route writes to master

# SQLAlchemy example
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Master (write)
master_engine = create_engine('postgresql://localhost/db')

# Replica (read)
replica_engine = create_engine('postgresql://replica-host/db')

# Use replica for reads
ReadSession = sessionmaker(bind=replica_engine)
read_session = ReadSession()
users = read_session.query(User).all()

# Use master for writes
WriteSession = sessionmaker(bind=master_engine)
write_session = WriteSession()
new_user = User(username='john')
write_session.add(new_user)
write_session.commit()
```

**5. Materialized Views (PostgreSQL)**
```sql
-- Create materialized view
CREATE MATERIALIZED VIEW user_post_stats AS
SELECT 
    u.id,
    u.username,
    COUNT(p.id) as post_count,
    MAX(p.created_at) as latest_post
FROM users u
LEFT JOIN posts p ON u.id = p.author_id
GROUP BY u.id, u.username;

-- Create index on materialized view
CREATE INDEX idx_user_stats_post_count ON user_post_stats(post_count);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW user_post_stats;

-- Query (fast - pre-computed)
SELECT * FROM user_post_stats WHERE post_count > 10;
```

### Write Operations Optimization

**1. Batch Writes**
```python
# BAD: Individual inserts
for user in users:
    db.execute("INSERT INTO users (username, email) VALUES (?, ?)", 
               (user['username'], user['email']))
    db.commit()

# GOOD: Batch insert
db.executemany(
    "INSERT INTO users (username, email) VALUES (?, ?)",
    [(u['username'], u['email']) for u in users]
)
db.commit()

# PostgreSQL - COPY for bulk insert
import psycopg2
from io import StringIO

conn = psycopg2.connect("dbname=mydb")
cur = conn.cursor()

# Create CSV in memory
csv_data = StringIO()
for user in users:
    csv_data.write(f"{user['username']},{user['email']}\n")
csv_data.seek(0)

# Bulk copy
cur.copy_from(csv_data, 'users', columns=('username', 'email'), sep=',')
conn.commit()
```

**2. Async Writes (Fire and Forget)**
```python
from celery import Celery
from redis import Redis

celery_app = Celery('tasks', broker='redis://localhost:6379/0')
redis_client = Redis(decode_responses=True)

@celery_app.task
def write_to_database(data):
    """Background task for non-critical writes"""
    db.execute("INSERT INTO logs (data) VALUES (?)", (data,))
    db.commit()

# Immediate return, write happens in background
write_to_database.delay({'event': 'user_login', 'user_id': 123})

# For analytics/logging - write to Redis queue first
def log_event(event_type, data):
    redis_client.lpush('events:queue', json.dumps({
        'type': event_type,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }))
    # Separate worker processes queue and writes to database
```

**3. Write-Behind Caching**
```python
def update_user(user_id, updates):
    # Update cache immediately
    cache_key = f'user:{user_id}'
    user = get_user(user_id)
    user.update(updates)
    redis_client.setex(cache_key, 3600, json.dumps(user))
    
    # Schedule database write for later
    write_to_database.delay(user_id, updates)
```

**4. Connection Pooling**
```python
# PostgreSQL with connection pool
from psycopg2.pool import SimpleConnectionPool

pool = SimpleConnectionPool(
    minconn=5,
    maxconn=20,
    host='localhost',
    database='mydb',
    user='user',
    password='password'
)

def execute_query(query, params):
    conn = pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.fetchall()
    finally:
        pool.putconn(conn)
```

**5. Optimistic Locking (Prevent Write Conflicts)**
```python
# SQLAlchemy with version column
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    version = Column(Integer, default=1, nullable=False)
    
    __mapper_args__ = {
        'version_id_col': version
    }

# Update with optimistic locking
user = session.query(User).filter(User.id == 1).first()
user.username = 'newname'
session.commit()  # Raises error if version changed
```

### Real-World Patterns

**Pattern 1: E-commerce Product Catalog (Read-Heavy)**
```python
class ProductService:
    def __init__(self, db, cache):
        self.db = db
        self.cache = cache
    
    def get_product(self, product_id):
        # Check cache (Redis)
        cache_key = f'product:{product_id}'
        cached = self.cache.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # Query database (read replica)
        product = self.db.replica.query(Product).filter(
            Product.id == product_id
        ).first()
        
        # Cache for 1 hour
        self.cache.setex(cache_key, 3600, json.dumps(product.to_dict()))
        
        return product
    
    def update_product(self, product_id, updates):
        # Update database (master)
        product = self.db.master.query(Product).filter(
            Product.id == product_id
        ).first()
        
        for key, value in updates.items():
            setattr(product, key, value)
        
        self.db.master.commit()
        
        # Invalidate cache
        self.cache.delete(f'product:{product_id}')
```

**Pattern 2: Social Media Feed (Write-Heavy)**
```python
class FeedService:
    def __init__(self, cassandra_session, redis_client):
        self.db = cassandra_session
        self.cache = redis_client
    
    def post_update(self, user_id, content):
        # Write to Cassandra (optimized for writes)
        post_id = uuid.uuid4()
        self.db.execute("""
            INSERT INTO posts (post_id, user_id, content, created_at)
            VALUES (%s, %s, %s, %s)
        """, (post_id, user_id, content, datetime.now()))
        
        # Add to user's timeline (Redis sorted set)
        self.cache.zadd(
            f'timeline:{user_id}',
            {str(post_id): time.time()}
        )
        
        # Fan out to followers (async)
        fanout_to_followers.delay(user_id, post_id)
    
    def get_timeline(self, user_id, limit=50):
        # Get from Redis (fast)
        post_ids = self.cache.zrevrange(
            f'timeline:{user_id}',
            0,
            limit - 1
        )
        
        # Batch fetch from Cassandra
        posts = []
        for post_id in post_ids:
            post = self.db.execute(
                "SELECT * FROM posts WHERE post_id = %s",
                (uuid.UUID(post_id),)
            ).one()
            posts.append(post)
        
        return posts
```

**Pattern 3: Analytics/Logging (Write-Heavy)**
```python
class AnalyticsService:
    def __init__(self):
        self.redis = Redis()
        self.batch_size = 1000
    
    def track_event(self, event_type, user_id, data):
        # Write to Redis queue (fast)
        event = {
            'type': event_type,
            'user_id': user_id,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        self.redis.lpush('analytics:queue', json.dumps(event))
        
        # Process in background worker
        queue_length = self.redis.llen('analytics:queue')
        if queue_length >= self.batch_size:
            process_analytics_batch.delay()
    
    def process_batch(self):
        # Get batch from queue
        events = []
        for _ in range(self.batch_size):
            event = self.redis.rpop('analytics:queue')
            if not event:
                break
            events.append(json.loads(event))
        
        # Bulk write to database (PostgreSQL/ClickHouse)
        if events:
            self.db.executemany(
                "INSERT INTO events (type, user_id, data, timestamp) VALUES (?, ?, ?, ?)",
                [(e['type'], e['user_id'], json.dumps(e['data']), e['timestamp']) 
                 for e in events]
            )
            self.db.commit()
```

---

## SMB vs Enterprise Architecture

### Small/Medium Business (SMB)

**Characteristics:**
- 1-10K users
- Single region
- Limited budget
- Simple architecture
- Monolithic application

**Database Architecture:**
```
┌─────────────────────────────────────┐
│         Application Server          │
│    (Single instance or 2-3 nodes)   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         MySQL/PostgreSQL            │
│         (Single instance)           │
│         + Daily backups             │
└─────────────────────────────────────┘
```

**Example Setup:**
```yaml
# Docker Compose for SMB
version: '3.8'

services:
  app:
    image: myapp:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    # Automated backups
    command: >
      bash -c "
      postgres &
      while true; do
        pg_dump -U user myapp > /backups/backup_$(date +%Y%m%d).sql
        sleep 86400
      done
      "
  
  redis:
    image: redis:7
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**Database Configuration (PostgreSQL):**
```sql
-- postgresql.conf for SMB (4GB RAM, 2 CPU)
shared_buffers = 1GB              # 25% of RAM
effective_cache_size = 3GB        # 75% of RAM
maintenance_work_mem = 256MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 10MB
min_wal_size = 1GB
max_wal_size = 4GB
max_connections = 100
```

**Backup Strategy:**
```bash
#!/bin/bash
# Simple backup script for SMB

# Daily full backup
pg_dump -U user -h localhost myapp > /backups/myapp_$(date +%Y%m%d).sql

# Compress old backups
find /backups -name "*.sql" -mtime +1 -exec gzip {} \;

# Delete backups older than 30 days
find /backups -name "*.sql.gz" -mtime +30 -delete

# Upload to S3
aws s3 sync /backups s3://my-backups/postgres/
```

### Enterprise Architecture

**Characteristics:**
- 100K+ users
- Multi-region
- High availability (99.99% uptime)
- Complex microservices
- Large budget

**Database Architecture:**
```
┌────────────────────────────────────────────────────────────┐
│                      Load Balancer                         │
└─────────────┬──────────────────────────────────────────────┘
              │
    ┌─────────┴─────────┬──────────────┬─────────────┐
    ▼                   ▼              ▼             ▼
┌─────────┐      ┌─────────┐    ┌─────────┐   ┌─────────┐
│  App 1  │      │  App 2  │    │  App 3  │   │  App N  │
└────┬────┘      └────┬────┘    └────┬────┘   └────┬────┘
     │                │              │             │
     └────────────────┴──────────────┴─────────────┘
                      │
          ┌───────────┴──────────────┐
          ▼                          ▼
    ┌──────────┐              ┌──────────┐
    │  Redis   │              │PostgreSQL│
    │  Cluster │              │  Master  │
    │(Caching) │              └─────┬────┘
    └──────────┘                    │
                          ┌─────────┼─────────┐
                          ▼         ▼         ▼
                    ┌─────────┬─────────┬─────────┐
                    │ Replica │ Replica │ Replica │
                    │   (R1)  │   (R2)  │   (R3)  │
                    └─────────┴─────────┴─────────┘
```

**Multi-Region Setup:**
```
Region 1 (US-East)              Region 2 (EU-West)
┌─────────────────┐            ┌─────────────────┐
│   PostgreSQL    │◄──────────►│   PostgreSQL    │
│   Master (US)   │ Replication│   Master (EU)   │
└────────┬────────┘            └────────┬────────┘
         │                              │
    ┌────┴────┐                    ┌────┴────┐
    ▼         ▼                    ▼         ▼
┌────────┐ ┌────────┐          ┌────────┐ ┌────────┐
│Replica │ │Replica │          │Replica │ │Replica │
└────────┘ └────────┘          └────────┘ └────────┘
```

**Microservices with Database per Service:**
```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    User      │    │    Order     │    │   Payment    │
│   Service    │    │   Service    │    │   Service    │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ PostgreSQL   │    │ PostgreSQL   │    │ PostgreSQL   │
│  (Users DB)  │    │ (Orders DB)  │    │ (Payments DB)│
└──────────────┘    └──────────────┘    └──────────────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │   Event Bus    │
                  │ (Kafka/RabbitMQ)│
                  └────────────────┘
```

**Database Configuration (PostgreSQL Enterprise):**
```sql
-- postgresql.conf for Enterprise (128GB RAM, 32 CPU)
shared_buffers = 32GB             # 25% of RAM
effective_cache_size = 96GB       # 75% of RAM
maintenance_work_mem = 2GB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 500
random_page_cost = 1.1
effective_io_concurrency = 300
work_mem = 50MB
min_wal_size = 4GB
max_wal_size = 16GB
max_connections = 500
max_worker_processes = 32
max_parallel_workers_per_gather = 8
max_parallel_workers = 32

-- Replication settings
wal_level = replica
max_wal_senders = 10
wal_keep_size = 1GB
hot_standby = on
```

**High Availability with Patroni (PostgreSQL):**
```yaml
# patroni.yml
scope: postgres-cluster
namespace: /db/
name: postgres-node1

restapi:
  listen: 0.0.0.0:8008
  connect_address: node1:8008

etcd:
  hosts: etcd1:2379,etcd2:2379,etcd3:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      parameters:
        max_connections: 500
        shared_buffers: 32GB
        effective_cache_size: 96GB

postgresql:
  listen: 0.0.0.0:5432
  connect_address: node1:5432
  data_dir: /var/lib/postgresql/15/main
  pgpass: /tmp/pgpass
  authentication:
    replication:
      username: replicator
      password: rep_password
    superuser:
      username: postgres
      password: postgres_password
  parameters:
    wal_level: replica
    hot_standby: "on"
    max_wal_senders: 10
    max_replication_slots: 10
    wal_keep_size: 1GB
```

**Monitoring Stack:**
```yaml
# Prometheus + Grafana + Postgres Exporter
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
  
  postgres_exporter:
    image: prometheuscommunity/postgres-exporter
    environment:
      - DATA_SOURCE_NAME=postgresql://user:pass@postgres:5432/mydb?sslmode=disable
    ports:
      - "9187:9187"

volumes:
  prometheus_data:
  grafana_data:
```

**Comparison Table:**

| Feature | SMB | Enterprise |
|---------|-----|------------|
| **Database** | Single instance | Clustered, multi-region |
| **Read Replicas** | 0-1 | 3-10+ |
| **Caching** | Single Redis | Redis Cluster |
| **Backup** | Daily full backup | Continuous backup + PITR |
| **Monitoring** | Basic logs | Full observability stack |
| **Failover** | Manual | Automatic (Patroni, etc.) |
| **Scaling** | Vertical | Horizontal + Vertical |
| **Cost** | $100-500/month | $10K-100K+/month |
| **Team Size** | 1-3 engineers | 10-50+ engineers |
| **SLA** | 99.5% | 99.99% |

---

## Database Optimization

### Query Optimization

**1. Use EXPLAIN ANALYZE**
```sql
-- PostgreSQL/MySQL
EXPLAIN ANALYZE SELECT * FROM posts WHERE author_id = 123;

-- Look for:
-- - Seq Scan (bad) vs Index Scan (good)
-- - High cost values
-- - Large row estimates
```

**2. Avoid SELECT ***
```sql
-- BAD
SELECT * FROM users WHERE id = 1;

-- GOOD (only select needed columns)
SELECT id, username, email FROM users WHERE id = 1;
```

**3. Use WHERE Instead of HAVING**
```sql
-- BAD
SELECT author_id, COUNT(*) as count
FROM posts
GROUP BY author_id
HAVING author_id = 123;

-- GOOD
SELECT author_id, COUNT(*) as count
FROM posts
WHERE author_id = 123
GROUP BY author_id;
```

**4. Avoid Functions in WHERE Clause**
```sql
-- BAD (index not used)
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- GOOD (index used)
SELECT * FROM users 
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

**5. Use JOIN Instead of Subqueries**
```sql
-- BAD (subquery for each row)
SELECT u.*, (SELECT COUNT(*) FROM posts WHERE author_id = u.id) as post_count
FROM users u;

-- GOOD (single join)
SELECT u.*, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.author_id
GROUP BY u.id;
```

**6. Limit Result Set**
```sql
-- Always use LIMIT for pagination
SELECT * FROM posts ORDER BY created_at DESC LIMIT 50 OFFSET 0;

-- Use WHERE for better performance
SELECT * FROM posts 
WHERE created_at < '2024-01-01' 
ORDER BY created_at DESC 
LIMIT 50;
```

### Index Optimization

**1. Create Appropriate Indexes**
```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_posts_author_status ON posts(author_id, status);

-- Covering index (includes all needed columns)
CREATE INDEX idx_posts_covering ON posts(author_id, status) INCLUDE (title, created_at);

-- Partial index (PostgreSQL)
CREATE INDEX idx_active_users ON users(email) WHERE is_active = TRUE;

-- Functional index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
```

**2. Monitor Index Usage**
```sql
-- PostgreSQL: Find unused indexes
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelname NOT LIKE 'pg_toast%'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Drop unused indexes
DROP INDEX idx_unused_index;
```

**3. Index Maintenance**
```sql
-- PostgreSQL: Reindex
REINDEX INDEX idx_users_email;
REINDEX TABLE users;
REINDEX DATABASE myapp_db;

-- Analyze tables
ANALYZE users;
ANALYZE VERBOSE;

-- Vacuum
VACUUM users;
VACUUM FULL;  -- Reclaims disk space
VACUUM ANALYZE;  -- Both vacuum and analyze
```

### Connection Pooling

**PgBouncer (PostgreSQL Connection Pooler):**
```ini
; pgbouncer.ini
[databases]
myapp_db = host=localhost port=5432 dbname=myapp_db

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
max_db_connections = 100
max_user_connections = 100
```

**Application Connection Pooling:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/mydb',
    poolclass=QueuePool,
    pool_size=20,          # Number of permanent connections
    max_overflow=10,       # Max temporary connections
    pool_timeout=30,       # Timeout for getting connection
    pool_recycle=3600,     # Recycle connections after 1 hour
    pool_pre_ping=True     # Verify connection before using
)
```

### Partitioning (PostgreSQL)

**Range Partitioning (by date):**
```sql
-- Create partitioned table
CREATE TABLE logs (
    id SERIAL,
    user_id INTEGER,
    action TEXT,
    created_at TIMESTAMP NOT NULL
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE logs_2024_01 PARTITION OF logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE logs_2024_02 PARTITION OF logs
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

CREATE TABLE logs_2024_03 PARTITION OF logs
    FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');

-- Create default partition
CREATE TABLE logs_default PARTITION OF logs DEFAULT;

-- Create indexes on partitions
CREATE INDEX ON logs_2024_01 (user_id);
CREATE INDEX ON logs_2024_02 (user_id);
CREATE INDEX ON logs_2024_03 (user_id);

-- Query (PostgreSQL automatically uses correct partition)
SELECT * FROM logs WHERE created_at >= '2024-02-01' AND created_at < '2024-03-01';
```

**List Partitioning (by category):**
```sql
CREATE TABLE users (
    id SERIAL,
    username TEXT,
    country TEXT NOT NULL
) PARTITION BY LIST (country);

CREATE TABLE users_us PARTITION OF users FOR VALUES IN ('US');
CREATE TABLE users_uk PARTITION OF users FOR VALUES IN ('UK');
CREATE TABLE users_eu PARTITION OF users FOR VALUES IN ('DE', 'FR', 'IT');
```

---

## Replication & Sharding

### Replication

**Master-Slave Replication (Read Replicas):**
```
         ┌─────────────┐
         │   Master    │
         │  (Writes)   │
         └──────┬──────┘
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Replica 1  │   │  Replica 2  │
│   (Reads)   │   │   (Reads)   │
└─────────────┘   └─────────────┘
```

**PostgreSQL Replication Setup:**

**Master (primary) configuration:**
```sql
-- postgresql.conf
wal_level = replica
max_wal_senders = 10
wal_keep_size = 1GB
hot_standby = on

-- pg_hba.conf
host replication replicator 192.168.1.0/24 md5

-- Create replication user
CREATE USER replicator REPLICATION LOGIN ENCRYPTED PASSWORD 'password';
```

**Replica (standby) configuration:**
```bash
# Stop PostgreSQL on replica
sudo systemctl stop postgresql

# Remove data directory
sudo rm -rf /var/lib/postgresql/15/main/*

# Base backup from master
pg_basebackup -h master_ip -D /var/lib/postgresql/15/main -U replicator -P -v -R -X stream -C -S replica_1

# Start PostgreSQL
sudo systemctl start postgresql

# Check replication status (on master)
SELECT * FROM pg_stat_replication;
```

**MySQL Replication Setup:**

**Master configuration:**
```ini
# my.cnf
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
```

```sql
-- Create replication user
CREATE USER 'replicator'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'replicator'@'%';
FLUSH PRIVILEGES;

-- Show master status
SHOW MASTER STATUS;
-- Note: File and Position
```

**Replica configuration:**
```ini
# my.cnf
[mysqld]
server-id = 2
relay-log = mysql-relay-bin
read_only = 1
```

```sql
-- Configure replication
CHANGE MASTER TO
    MASTER_HOST='master_ip',
    MASTER_USER='replicator',
    MASTER_PASSWORD='password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=12345;

-- Start replication
START SLAVE;

-- Check status
SHOW SLAVE STATUS\G
```

### Sharding

**Horizontal Sharding (Split by rows):**
```
Users Table (10M records)

Shard 1:          Shard 2:          Shard 3:
Users 1-3.3M      Users 3.3M-6.6M   Users 6.6M-10M
```

**Sharding Strategies:**

**1. Range-Based Sharding:**
```python
def get_shard_by_user_id(user_id):
    if user_id <= 3_300_000:
        return 'shard1'
    elif user_id <= 6_600_000:
        return 'shard2'
    else:
        return 'shard3'

# Usage
user_id = 5_000_000
shard = get_shard_by_user_id(user_id)
db = get_database_connection(shard)
user = db.query(User).filter(User.id == user_id).first()
```

**2. Hash-Based Sharding:**
```python
import hashlib

def get_shard_by_hash(key, num_shards=4):
    hash_value = int(hashlib.md5(str(key).encode()).hexdigest(), 16)
    return f'shard{hash_value % num_shards + 1}'

# Usage
user_id = 12345
shard = get_shard_by_hash(user_id, num_shards=4)
db = get_database_connection(shard)
```

**3. Geographic Sharding:**
```python
SHARD_MAP = {
    'US': 'us_db',
    'EU': 'eu_db',
    'ASIA': 'asia_db'
}

def get_shard_by_region(region):
    return SHARD_MAP.get(region, 'us_db')  # Default to US

# Usage
user_region = 'EU'
shard = get_shard_by_region(user_region)
db = get_database_connection(shard)
```

**Sharding with SQLAlchemy:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define shards
SHARDS = {
    'shard1': create_engine('postgresql://localhost/shard1'),
    'shard2': create_engine('postgresql://localhost/shard2'),
    'shard3': create_engine('postgresql://localhost/shard3'),
    'shard4': create_engine('postgresql://localhost/shard4'),
}

def get_session(shard_id):
    engine = SHARDS[shard_id]
    Session = sessionmaker(bind=engine)
    return Session()

# Shard routing
def get_user(user_id):
    shard_id = f'shard{(user_id % 4) + 1}'
    session = get_session(shard_id)
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    return user

def create_user(user_data):
    user_id = generate_user_id()
    shard_id = f'shard{(user_id % 4) + 1}'
    session = get_session(shard_id)
    
    user = User(id=user_id, **user_data)
    session.add(user)
    session.commit()
    session.close()
    
    return user
```

**Challenges with Sharding:**
- **Cross-shard queries:** Difficult to join data across shards
- **Rebalancing:** Moving data when adding/removing shards
- **Transactions:** Distributed transactions are complex
- **Hotspots:** Uneven data distribution

**Solutions:**
- **Consistent Hashing:** Better data distribution
- **Shard Key Design:** Choose carefully (user_id, tenant_id, etc.)
- **Caching:** Reduce cross-shard queries
- **Service Layer:** Abstract sharding logic

---

## Interview Questions (3 Years Experience)

### Q1: Explain the difference between SQL and NoSQL databases. When would you use each?

**Answer:**

**SQL (Relational):**
- **Structure:** Fixed schema with tables, rows, columns
- **Relationships:** Foreign keys, JOINs
- **ACID:** Full ACID compliance
- **Scaling:** Vertical (limited)
- **Examples:** MySQL, PostgreSQL, Oracle

**NoSQL (Non-Relational):**
- **Structure:** Flexible schema (document, key-value, column-family, graph)
- **Relationships:** Embedded documents or manual references
- **Consistency:** BASE (eventual consistency)
- **Scaling:** Horizontal (unlimited)
- **Examples:** MongoDB, Redis, Cassandra

**Use SQL when:**
- Complex queries with multiple JOINs
- ACID transactions required (banking, e-commerce)
- Structured data with clear relationships
- Strong data integrity needed

**Use NoSQL when:**
- Flexible schema (rapid development)
- Massive scale (millions of users)
- High read/write throughput
- Unstructured or semi-structured data
- Real-time applications

### Q2: What is database indexing? How does it improve performance?

**Answer:**

An index is a data structure that improves query performance by allowing the database to find rows faster.

**How it works:**
```sql
-- Without index: Full table scan (O(n))
SELECT * FROM users WHERE email = 'john@example.com';
-- Scans all rows

-- With index: Index scan (O(log n))
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'john@example.com';
-- Uses B-tree to find row quickly
```

**Types of Indexes:**
- **B-tree Index:** Default, good for range queries
- **Hash Index:** Fast equality lookups
- **GIN/GiST:** Full-text search (PostgreSQL)
- **Covering Index:** Includes all needed columns

**Trade-offs:**
- **Pros:** Faster SELECT queries
- **Cons:** Slower INSERT/UPDATE/DELETE, uses disk space

**Best Practices:**
- Index foreign keys
- Index columns in WHERE, JOIN, ORDER BY
- Use composite indexes for multiple columns
- Don't over-index (adds overhead)
- Monitor index usage

### Q3: Explain ACID properties in databases.

**Answer:**

**A - Atomicity:**
All operations in a transaction succeed or all fail (all-or-nothing).

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- Both succeed or both fail
```

**C - Consistency:**
Database remains in valid state before and after transaction.

```sql
-- Constraint: balance >= 0
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
-- Fails if balance would go negative
```

**I - Isolation:**
Concurrent transactions don't interfere with each other.

**Isolation Levels:**
- **Read Uncommitted:** Dirty reads possible
- **Read Committed:** No dirty reads
- **Repeatable Read:** No dirty/non-repeatable reads
- **Serializable:** Full isolation

**D - Durability:**
Committed data persists even after system failure.

```sql
COMMIT;  -- Data written to disk (WAL)
-- Survives power loss
```

### Q4: What is database normalization? Explain the normal forms.

**Answer:**

Normalization reduces data redundancy and improves data integrity.

**1NF (First Normal Form):**
- Atomic values (no arrays/lists)
- Each row is unique

```sql
-- NOT 1NF
CREATE TABLE users (
    id INT,
    name VARCHAR(100),
    phones VARCHAR(255)  -- "555-1234, 555-5678"
);

-- 1NF
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE user_phones (
    user_id INT,
    phone VARCHAR(20),
    PRIMARY KEY (user_id, phone)
);
```

**2NF (Second Normal Form):**
- Must be in 1NF
- No partial dependencies (all non-key attributes depend on entire primary key)

**3NF (Third Normal Form):**
- Must be in 2NF
- No transitive dependencies (non-key attributes don't depend on other non-key attributes)

```sql
-- NOT 3NF
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),  -- Depends on customer_id (transitive)
    customer_email VARCHAR(100)  -- Depends on customer_id (transitive)
);

-- 3NF
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(id)
);

CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

**When to Denormalize:**
- Read-heavy applications
- Performance optimization
- Data warehousing
- Caching layers

### Q5: What is the N+1 query problem? How do you solve it?

**Answer:**

**Problem:** Making N additional queries for N records.

```python
# N+1 Problem
posts = session.query(Post).all()  # 1 query
for post in posts:
    author = session.query(User).filter(User.id == post.author_id).first()  # N queries
    print(f"{post.title} by {author.username}")
# Total: 1 + N queries
```

**Solutions:**

**1. Eager Loading (JOIN):**
```python
# SQLAlchemy
posts = session.query(Post).join(User).all()  # 1 query

# Django ORM
posts = Post.objects.select_related('author').all()  # 1 query
```

**2. Prefetch Related (Separate queries):**
```python
# Django ORM
posts = Post.objects.prefetch_related('author').all()  # 2 queries (better than N+1)
```

**3. Batch Loading:**
```python
# Get all posts
posts = session.query(Post).all()

# Get all authors in one query
author_ids = [post.author_id for post in posts]
authors = session.query(User).filter(User.id.in_(author_ids)).all()
author_dict = {author.id: author for author in authors}

# Match posts to authors
for post in posts:
    post.author = author_dict[post.author_id]
```

### Q6: Explain database replication and its types.

**Answer:**

Replication creates copies of data across multiple database servers.

**Types:**

**1. Master-Slave (Primary-Replica):**
```
Master (Write) → Replica 1 (Read)
               → Replica 2 (Read)
               → Replica 3 (Read)
```
- **Pros:** Scales reads, high availability
- **Cons:** Single write point, replication lag

**2. Master-Master (Multi-Master):**
```
Master 1 ⟷ Master 2
```
- **Pros:** Scales writes, no single point of failure
- **Cons:** Conflict resolution, complexity

**3. Synchronous vs Asynchronous:**
- **Synchronous:** Wait for replica confirmation (no data loss, slower)
- **Asynchronous:** Don't wait (faster, possible data loss)

**Use Cases:**
- **Read scaling:** Multiple read replicas
- **High availability:** Automatic failover
- **Geographic distribution:** Replicas in multiple regions
- **Backup:** Real-time backup

### Q7: What is sharding? How does it differ from partitioning?

**Answer:**

**Sharding:** Horizontal partitioning across multiple servers.

```
Users Table (10M records)

Server 1:         Server 2:         Server 3:
Users 1-3.3M      Users 3.3M-6.6M   Users 6.6M-10M
```

**Partitioning:** Dividing table within single database.

```sql
-- PostgreSQL partitioning
CREATE TABLE logs (
    id SERIAL,
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

CREATE TABLE logs_2024_01 PARTITION OF logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

**Differences:**

| Aspect | Sharding | Partitioning |
|--------|----------|--------------|
| **Scope** | Multiple servers | Single server |
| **Purpose** | Scale beyond single server | Improve performance |
| **Complexity** | High | Medium |
| **Application Changes** | Required | Transparent |
| **Joins** | Difficult across shards | Easy |

**Sharding Strategies:**
- **Range:** user_id 1-1M → shard1, 1M-2M → shard2
- **Hash:** hash(user_id) % num_shards
- **Geographic:** US → us_shard, EU → eu_shard

### Q8: How do you optimize slow queries?

**Answer:**

**Step 1: Identify Slow Queries**
```sql
-- PostgreSQL: Enable slow query log
ALTER DATABASE mydb SET log_min_duration_statement = 1000;  -- Log queries > 1s

-- MySQL
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
```

**Step 2: Analyze with EXPLAIN**
```sql
EXPLAIN ANALYZE SELECT * FROM posts WHERE author_id = 123;
```

**Step 3: Common Optimizations**

**1. Add Indexes:**
```sql
CREATE INDEX idx_posts_author ON posts(author_id);
```

**2. Rewrite Query:**
```sql
-- BAD: Function on indexed column
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- GOOD
SELECT * FROM users WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

**3. Limit Result Set:**
```sql
SELECT * FROM posts ORDER BY created_at DESC LIMIT 50;
```

**4. Use JOINs Instead of Subqueries:**
```sql
-- BAD
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);

-- GOOD
SELECT DISTINCT u.* FROM users u INNER JOIN orders o ON u.id = o.user_id;
```

**5. Avoid SELECT *:**
```sql
SELECT id, title, created_at FROM posts;  -- Only needed columns
```

**6. Cache Results:**
```python
# Redis caching
cached = redis.get(f'user:{user_id}')
if not cached:
    user = db.query(User).filter(User.id == user_id).first()
    redis.setex(f'user:{user_id}', 3600, json.dumps(user))
```

### Q9: Explain CAP theorem and BASE properties.

**Answer:**

**CAP Theorem:**
In distributed systems, you can only guarantee 2 out of 3:

**C - Consistency:** All nodes see same data at same time
**A - Availability:** Every request gets a response
**P - Partition Tolerance:** System continues despite network failures

**Trade-offs:**
- **CP:** Consistent but may be unavailable (MongoDB, HBase)
- **AP:** Available but may be inconsistent (Cassandra, DynamoDB)
- **CA:** Consistent and available but no partition tolerance (traditional RDBMS)

**BASE Properties (NoSQL alternative to ACID):**

**BA - Basically Available:** System guarantees availability
**S - Soft state:** State may change without input (eventual consistency)
**E - Eventual consistency:** System becomes consistent over time

**Example:**
```python
# Instagram likes (AP system)
# User A likes post → Write to US datacenter
# User B (in EU) sees old count → Eventually sees new count after replication
```

### Q10: What are database transactions and isolation levels?

**Answer:**

**Transaction:** Group of operations that execute as single unit.

```python
# Example: Money transfer
with db.begin():
    # Deduct from sender
    db.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    
    # Add to receiver
    db.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    
    # Both succeed or both fail
```

**Isolation Levels:**

**1. Read Uncommitted (Lowest):**
- **Problem:** Dirty reads (read uncommitted data)
```sql
-- Transaction 1
BEGIN;
UPDATE accounts SET balance = 1000 WHERE id = 1;
-- Not committed yet

-- Transaction 2 can read uncommitted value
SELECT balance FROM accounts WHERE id = 1;  -- Sees 1000
```

**2. Read Committed:**
- **Problem:** Non-repeatable reads
```sql
-- Transaction 1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Returns 100

-- Transaction 2
UPDATE accounts SET balance = 200 WHERE id = 1;
COMMIT;

-- Transaction 1
SELECT balance FROM accounts WHERE id = 1;  -- Returns 200 (changed!)
```

**3. Repeatable Read:**
- **Problem:** Phantom reads (new rows appear)
```sql
-- Transaction 1
BEGIN;
SELECT COUNT(*) FROM posts WHERE status = 'published';  -- Returns 10

-- Transaction 2
INSERT INTO posts (status) VALUES ('published');
COMMIT;

-- Transaction 1
SELECT COUNT(*) FROM posts WHERE status = 'published';  -- Returns 11 (phantom!)
```

**4. Serializable (Highest):**
- **No problems, full isolation**
- **Slowest (locks):**

```sql
-- Set isolation level
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
-- Your queries
COMMIT;
```

---

**This comprehensive databases guide covers MySQL, PostgreSQL, MongoDB, Redis, Cassandra, real-world patterns, SMB vs Enterprise architecture, optimization techniques, replication & sharding, and interview questions for 3 years of experience.**