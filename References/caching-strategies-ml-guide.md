# Caching Strategies for ML/Data Science - Complete Guide

> **Comprehensive reference for caching types, strategies, advantages, disadvantages, and implementations in Python, ML, and AI systems**

---

## Table of Contents

1. [Introduction to Caching](#introduction-to-caching)
2. [Cache Types Overview](#cache-types-overview)
3. [Memory Caching](#memory-caching)
4. [Disk Caching](#disk-caching)
5. [Distributed Caching](#distributed-caching)
6. [Database Query Caching](#database-query-caching)
7. [Web/API Caching](#web-api-caching)
8. [ML Model Caching](#ml-model-caching)
9. [Feature Caching](#feature-caching)
10. [Result Caching](#result-caching)
11. [Cache Eviction Policies](#cache-eviction-policies)
12. [Python Caching Implementations](#python-caching-implementations)
13. [ML/AI Specific Caching](#ml-ai-specific-caching)
14. [Cache Invalidation Strategies](#cache-invalidation-strategies)
15. [Performance Comparison](#performance-comparison)
16. [Best Practices](#best-practices)
17. [Interview Questions](#interview-questions)

---

## Introduction to Caching

### What is Caching?

**Caching** is storing frequently accessed data in a fast-access location to reduce:
- Computation time
- Network latency
- Database load
- API calls
- Cost

### Why Caching Matters in ML/AI

```python
# Without caching
def predict(data):
    preprocessed = preprocess(data)        # 100ms
    features = extract_features(data)      # 500ms
    model = load_model()                   # 2000ms
    result = model.predict(features)       # 50ms
    return result
# Total: 2650ms per request

# With caching
@cache
def load_model():
    # Only runs once, then cached
    return model

# Total: 650ms per request (75% faster!)
```

### Cache Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│                    SPEED vs COST                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CPU Registers    │ Fastest   │ Smallest  │ ~1ns       │
│  CPU L1 Cache     │ ↓         │ ↓         │ ~1ns       │
│  CPU L2 Cache     │ ↓         │ ↓         │ ~4ns       │
│  CPU L3 Cache     │ ↓         │ ↓         │ ~10ns      │
│  RAM              │ ↓         │ ↓         │ ~100ns     │
│  SSD              │ ↓         │ ↓         │ ~100μs     │
│  HDD              │ ↓         │ ↓         │ ~10ms      │
│  Network/API      │ Slowest   │ Largest   │ ~100ms     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Key Concepts

**1. Cache Hit:** Data found in cache (fast!)
**2. Cache Miss:** Data not in cache (slow, need to fetch)
**3. Hit Rate:** % of requests served from cache
**4. TTL (Time To Live):** How long data stays in cache
**5. Eviction:** Removing old data to make space

---

## Cache Types Overview

### Comparison Table

| Cache Type | Speed | Size | Persistence | Cost | Use Case |
|------------|-------|------|-------------|------|----------|
| **In-Memory** | Very Fast | Small-Medium | No | High | Hot data, sessions |
| **Disk** | Medium | Large | Yes | Medium | Preprocessed data |
| **Distributed** | Fast | Very Large | Yes | High | Multi-server apps |
| **Database** | Medium-Fast | Large | Yes | Medium | Query results |
| **CDN** | Fast | Very Large | Yes | Medium | Static content |
| **Application** | Very Fast | Small | No | Low | Function results |
| **Browser** | Very Fast | Small | Partial | Free | Web assets |

---

## Memory Caching

### Types of Memory Caches

#### 1. Local Memory (In-Process)

**Description:** Store data in application's RAM

**Advantages:**
✅ Extremely fast (nanoseconds)
✅ No network latency
✅ Simple implementation
✅ No external dependencies
✅ Thread-safe with proper locking
✅ Best for single-server applications

**Disadvantages:**
❌ Limited by RAM
❌ Lost on restart
❌ Not shared across processes
❌ Not shared across servers
❌ Can cause memory issues if not managed
❌ Data inconsistency in multi-server setup

**Implementation:**

```python
# Simple dictionary cache
class SimpleCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value):
        self.cache[key] = value
    
    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

# Usage
cache = SimpleCache()
cache.set('user_123', {'name': 'John', 'age': 30})
user = cache.get('user_123')

# With LRU (Least Recently Used)
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(x, y):
    print(f"Computing {x} + {y}...")
    return x + y

print(expensive_computation(5, 3))  # Computes
print(expensive_computation(5, 3))  # Returns from cache
print(expensive_computation(5, 3))  # Returns from cache

# Cache info
print(expensive_computation.cache_info())
# CacheInfo(hits=2, misses=1, maxsize=128, currsize=1)
```

#### 2. Redis (In-Memory Data Store)

**Description:** Remote in-memory database with persistence

**Advantages:**
✅ Shared across processes/servers
✅ Very fast (sub-millisecond)
✅ Persistence options (RDB, AOF)
✅ Rich data structures (strings, lists, sets, hashes)
✅ Built-in TTL support
✅ Atomic operations
✅ Pub/Sub messaging
✅ Clustering support
✅ High availability (Redis Sentinel)

**Disadvantages:**
❌ Network latency (vs local memory)
❌ Additional infrastructure
❌ Cost (if managed service)
❌ Memory limited (expensive for large data)
❌ Single-threaded (per instance)
❌ Requires maintenance
❌ Data serialization overhead

**Implementation:**

```python
import redis
import json
import pickle

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(
            host=host, 
            port=port, 
            db=db,
            decode_responses=False  # Handle binary data
        )
    
    def get(self, key):
        """Get value from cache"""
        value = self.client.get(key)
        if value:
            return pickle.loads(value)
        return None
    
    def set(self, key, value, ttl=3600):
        """Set value with TTL (seconds)"""
        serialized = pickle.dumps(value)
        self.client.setex(key, ttl, serialized)
    
    def get_many(self, keys):
        """Get multiple keys at once"""
        values = self.client.mget(keys)
        return [pickle.loads(v) if v else None for v in values]
    
    def set_many(self, data_dict, ttl=3600):
        """Set multiple keys at once"""
        pipe = self.client.pipeline()
        for key, value in data_dict.items():
            serialized = pickle.dumps(value)
            pipe.setex(key, ttl, serialized)
        pipe.execute()
    
    def delete(self, key):
        """Delete key"""
        self.client.delete(key)
    
    def exists(self, key):
        """Check if key exists"""
        return self.client.exists(key) > 0
    
    def clear(self):
        """Clear all cache"""
        self.client.flushdb()
    
    def increment(self, key, amount=1):
        """Atomic increment"""
        return self.client.incr(key, amount)

# Usage
cache = RedisCache()

# Cache ML model predictions
def get_prediction_cached(user_id, features):
    cache_key = f"prediction:{user_id}:{hash(str(features))}"
    
    # Check cache
    result = cache.get(cache_key)
    if result:
        print("Cache hit!")
        return result
    
    # Cache miss - compute
    print("Cache miss - computing...")
    result = ml_model.predict(features)
    
    # Store in cache (1 hour TTL)
    cache.set(cache_key, result, ttl=3600)
    return result

# Batch caching
predictions = {
    'user_1': [0.95, 0.05],
    'user_2': [0.12, 0.88],
    'user_3': [0.67, 0.33]
}
cache.set_many(predictions, ttl=1800)  # 30 minutes

# Rate limiting with Redis
def is_rate_limited(user_id, max_requests=100, window=3600):
    """Allow max_requests per window (seconds)"""
    key = f"rate_limit:{user_id}"
    count = cache.increment(key)
    
    if count == 1:
        # First request, set expiry
        cache.client.expire(key, window)
    
    return count > max_requests
```

#### 3. Memcached

**Description:** Distributed memory caching system

**Advantages:**
✅ Simple and fast
✅ Multi-threaded (scales better than Redis)
✅ Lower memory overhead
✅ Efficient for simple key-value
✅ Widely supported
✅ Automatic memory management
✅ Good for large-scale deployments

**Disadvantages:**
❌ No persistence (pure memory)
❌ Only supports strings (need serialization)
❌ No complex data structures
❌ No built-in replication
❌ No transactions
❌ Lost on restart
❌ Limited to 1MB per value (by default)

**Implementation:**

```python
import pylibmc

class MemcachedCache:
    def __init__(self, servers=['127.0.0.1:11211']):
        self.client = pylibmc.Client(
            servers,
            binary=True,
            behaviors={
                "tcp_nodelay": True,
                "ketama": True  # Consistent hashing
            }
        )
    
    def get(self, key):
        """Get value"""
        value = self.client.get(key)
        if value:
            return pickle.loads(value)
        return None
    
    def set(self, key, value, ttl=3600):
        """Set value with TTL"""
        serialized = pickle.dumps(value)
        self.client.set(key, serialized, time=ttl)
    
    def get_multi(self, keys):
        """Get multiple keys"""
        values = self.client.get_multi(keys)
        return {k: pickle.loads(v) for k, v in values.items()}
    
    def set_multi(self, data_dict, ttl=3600):
        """Set multiple keys"""
        serialized = {k: pickle.dumps(v) for k, v in data_dict.items()}
        self.client.set_multi(serialized, time=ttl)
    
    def delete(self, key):
        """Delete key"""
        self.client.delete(key)
    
    def flush_all(self):
        """Clear all cache"""
        self.client.flush_all()

# Usage
cache = MemcachedCache()

# Cache database query results
def get_user_data(user_id):
    cache_key = f"user_data:{user_id}"
    
    # Try cache
    data = cache.get(cache_key)
    if data:
        return data
    
    # Fetch from database
    data = db.query(f"SELECT * FROM users WHERE id={user_id}")
    
    # Cache for 10 minutes
    cache.set(cache_key, data, ttl=600)
    return data
```

### Memory Cache Comparison

| Feature | Local Memory | Redis | Memcached |
|---------|-------------|-------|-----------|
| **Speed** | Fastest | Very Fast | Very Fast |
| **Shared** | No | Yes | Yes |
| **Persistence** | No | Yes | No |
| **Data Structures** | Any Python | Rich | Strings only |
| **Clustering** | No | Yes | Yes |
| **Threading** | Single | Single | Multi |
| **Use Case** | Single server | Complex needs | Simple KV, scale |

---

## Disk Caching

### Types of Disk Caches

#### 1. File-Based Caching

**Description:** Store cache data in files on disk

**Advantages:**
✅ Survives restarts
✅ Unlimited storage (disk space)
✅ Simple implementation
✅ No external dependencies
✅ Good for large objects
✅ Operating system manages I/O
✅ Can use compression

**Disadvantages:**
❌ Slower than memory (100-1000x)
❌ File system overhead
❌ Locking issues (concurrent access)
❌ Manual cleanup needed
❌ Platform-specific issues
❌ Fragmentation over time

**Implementation:**

```python
import os
import pickle
import hashlib
import json
import time
from pathlib import Path

class DiskCache:
    def __init__(self, cache_dir='./cache', ttl=3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = ttl
    
    def _get_cache_path(self, key):
        """Generate cache file path from key"""
        # Hash key to create filename
        key_hash = hashlib.md5(str(key).encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"
    
    def get(self, key):
        """Get value from disk cache"""
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        # Check if expired
        age = time.time() - cache_path.stat().st_mtime
        if age > self.ttl:
            cache_path.unlink()  # Delete expired cache
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Cache read error: {e}")
            return None
    
    def set(self, key, value):
        """Set value to disk cache"""
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
        except Exception as e:
            print(f"Cache write error: {e}")
    
    def delete(self, key):
        """Delete cached value"""
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            cache_path.unlink()
    
    def clear(self):
        """Clear all cache"""
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink()
    
    def size(self):
        """Get total cache size in bytes"""
        return sum(f.stat().st_size for f in self.cache_dir.glob("*.cache"))
    
    def cleanup_expired(self):
        """Remove expired cache files"""
        current_time = time.time()
        for cache_file in self.cache_dir.glob("*.cache"):
            age = current_time - cache_file.stat().st_mtime
            if age > self.ttl:
                cache_file.unlink()

# Usage
cache = DiskCache(cache_dir='./ml_cache', ttl=86400)  # 1 day

# Cache preprocessed data
def load_preprocessed_data(dataset_name):
    cache_key = f"preprocessed_{dataset_name}"
    
    # Try cache
    data = cache.get(cache_key)
    if data is not None:
        print("Loading from cache...")
        return data
    
    # Process data
    print("Processing data...")
    data = preprocess_dataset(dataset_name)
    
    # Cache it
    cache.set(cache_key, data)
    return data

# Cleanup old cache
cache.cleanup_expired()
print(f"Cache size: {cache.size() / 1024**2:.2f} MB")
```

#### 2. SQLite Caching

**Description:** Use SQLite database for caching

**Advantages:**
✅ Persistent across restarts
✅ ACID transactions
✅ Indexing for fast lookups
✅ SQL query capabilities
✅ Built into Python
✅ Automatic memory management
✅ Concurrent reads
✅ Metadata storage

**Disadvantages:**
❌ Slower than memory cache
❌ Overhead of SQL engine
❌ Write locking (single writer)
❌ Not ideal for very large values
❌ Requires serialization
❌ Database file can grow large

**Implementation:**

```python
import sqlite3
import pickle
import time
from datetime import datetime

class SQLiteCache:
    def __init__(self, db_path='cache.db', ttl=3600):
        self.db_path = db_path
        self.ttl = ttl
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value BLOB,
                    created_at REAL,
                    access_count INTEGER DEFAULT 0,
                    last_accessed REAL
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_created ON cache(created_at)')
            conn.commit()
    
    def get(self, key):
        """Get value from cache"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT value, created_at FROM cache WHERE key = ?',
                (key,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            value_blob, created_at = row
            
            # Check expiry
            age = time.time() - created_at
            if age > self.ttl:
                self.delete(key)
                return None
            
            # Update access stats
            conn.execute('''
                UPDATE cache 
                SET access_count = access_count + 1,
                    last_accessed = ?
                WHERE key = ?
            ''', (time.time(), key))
            conn.commit()
            
            return pickle.loads(value_blob)
    
    def set(self, key, value):
        """Set value in cache"""
        value_blob = pickle.dumps(value)
        current_time = time.time()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO cache 
                (key, value, created_at, last_accessed)
                VALUES (?, ?, ?, ?)
            ''', (key, value_blob, current_time, current_time))
            conn.commit()
    
    def delete(self, key):
        """Delete key from cache"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM cache WHERE key = ?', (key,))
            conn.commit()
    
    def clear(self):
        """Clear all cache"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM cache')
            conn.commit()
    
    def cleanup_expired(self):
        """Remove expired entries"""
        cutoff_time = time.time() - self.ttl
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'DELETE FROM cache WHERE created_at < ?',
                (cutoff_time,)
            )
            deleted = cursor.rowcount
            conn.commit()
        return deleted
    
    def get_stats(self):
        """Get cache statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT 
                    COUNT(*) as total_entries,
                    SUM(LENGTH(value)) as total_size,
                    AVG(access_count) as avg_access_count,
                    MAX(access_count) as max_access_count
                FROM cache
            ''')
            row = cursor.fetchone()
            return {
                'total_entries': row[0],
                'total_size_mb': (row[1] or 0) / 1024**2,
                'avg_access_count': row[2] or 0,
                'max_access_count': row[3] or 0
            }

# Usage
cache = SQLiteCache(db_path='ml_cache.db', ttl=86400)

# Cache feature engineering results
def engineer_features(user_id, raw_data):
    cache_key = f"features:{user_id}"
    
    # Try cache
    features = cache.get(cache_key)
    if features is not None:
        return features
    
    # Engineer features
    features = compute_features(raw_data)
    cache.set(cache_key, features)
    return features

# Cleanup and stats
deleted = cache.cleanup_expired()
stats = cache.get_stats()
print(f"Deleted {deleted} expired entries")
print(f"Cache stats: {stats}")
```

#### 3. Joblib Caching (Memory)

**Description:** Caching for expensive function calls (ML focused)

**Advantages:**
✅ Designed for NumPy/Pandas
✅ Automatic hashing of inputs
✅ Works with large arrays
✅ Decorator-based (easy to use)
✅ Smart caching (only changed inputs)
✅ Persistent to disk
✅ Compression support

**Disadvantages:**
❌ Disk-based (slower than memory)
❌ Large disk space for big data
❌ No TTL support
❌ Manual cleanup needed
❌ Not distributed

**Implementation:**

```python
from joblib import Memory
import numpy as np
import pandas as pd

# Create memory object
memory = Memory(location='./joblib_cache', verbose=0)

@memory.cache
def expensive_preprocessing(df):
    """Cached preprocessing function"""
    print("Preprocessing data...")
    # Expensive operations
    df = df.fillna(df.mean())
    df['feature1'] = df['col1'] * df['col2']
    df['feature2'] = np.log1p(df['col3'])
    return df

@memory.cache
def train_model(X, y, n_estimators=100):
    """Cached model training"""
    print("Training model...")
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X, y)
    return model

# Usage
df = pd.read_csv('data.csv')

# First call: computes and caches
df_processed = expensive_preprocessing(df)

# Second call: returns from cache (instant)
df_processed = expensive_preprocessing(df)

# Different input: computes and caches
df2 = pd.read_csv('data2.csv')
df2_processed = expensive_preprocessing(df2)  # Computes

# Same model parameters: cached
model = train_model(X_train, y_train, n_estimators=100)  # Computes
model = train_model(X_train, y_train, n_estimators=100)  # Cached

# Different parameters: computes new
model2 = train_model(X_train, y_train, n_estimators=200)  # Computes

# Clear cache
memory.clear()

# Reduce cache (keep only recent)
memory.reduce_size()
```

---

## Distributed Caching

### 1. Redis Cluster

**Description:** Distributed Redis across multiple nodes

**Advantages:**
✅ Horizontal scaling
✅ Data partitioning (sharding)
✅ High availability
✅ Automatic failover
✅ Handles TBs of data
✅ Linear performance scaling
✅ Multiple replicas

**Disadvantages:**
❌ Complex setup
❌ Network overhead
❌ No multi-key operations across shards
❌ Resharding is complex
❌ Higher latency than single instance
❌ More expensive

**Implementation:**

```python
from redis.cluster import RedisCluster

class RedisClusterCache:
    def __init__(self, startup_nodes):
        """
        startup_nodes: [{'host': '127.0.0.1', 'port': 7000}, ...]
        """
        self.client = RedisCluster(
            startup_nodes=startup_nodes,
            decode_responses=False,
            skip_full_coverage_check=False
        )
    
    def get(self, key):
        value = self.client.get(key)
        if value:
            return pickle.loads(value)
        return None
    
    def set(self, key, value, ttl=3600):
        serialized = pickle.dumps(value)
        self.client.setex(key, ttl, serialized)
    
    def get_many(self, keys):
        """Get multiple keys (may span multiple nodes)"""
        # Note: mget not supported in cluster mode for keys on different nodes
        # Need to fetch individually
        results = {}
        for key in keys:
            results[key] = self.get(key)
        return results
    
    def delete(self, key):
        self.client.delete(key)
    
    def exists(self, key):
        return self.client.exists(key) > 0

# Usage
startup_nodes = [
    {'host': '127.0.0.1', 'port': 7000},
    {'host': '127.0.0.1', 'port': 7001},
    {'host': '127.0.0.1', 'port': 7002},
]

cache = RedisClusterCache(startup_nodes)

# Use same as regular Redis
cache.set('user:1000', user_data, ttl=3600)
data = cache.get('user:1000')
```

### 2. Hazelcast

**Description:** In-memory data grid for distributed caching

**Advantages:**
✅ Distributed and replicated
✅ Automatic partitioning
✅ Built-in data structures
✅ Fast queries
✅ Elastic scaling
✅ Works across data centers
✅ Rich querying capabilities

**Disadvantages:**
❌ Java-based (JVM required)
❌ Python client has limitations
❌ Memory intensive
❌ Complex configuration
❌ Less Python ecosystem support
❌ Expensive at scale

### 3. Apache Ignite

**Description:** Distributed in-memory cache with persistence

**Advantages:**
✅ In-memory + disk persistence
✅ SQL support
✅ ACID transactions
✅ Distributed computing
✅ Very fast
✅ ML library included

**Disadvantages:**
❌ Complex setup
❌ High memory requirements
❌ Steep learning curve
❌ Overhead for simple use cases

---

## Database Query Caching

### 1. ORM-Level Caching (SQLAlchemy)

**Description:** Cache at database ORM layer

**Advantages:**
✅ Transparent to application
✅ Automatic cache invalidation
✅ Reduces DB load
✅ Easy integration
✅ Per-query control

**Disadvantages:**
❌ Application-specific
❌ Not shared across instances
❌ Memory overhead
❌ Complex invalidation

**Implementation:**

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dogpile.cache import make_region

# Setup cache region
cache_region = make_region().configure(
    'dogpile.cache.redis',
    expiration_time=3600,
    arguments={
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'redis_expiration_time': 3600,
        'distributed_lock': True
    }
)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Cached query function
def get_user_by_id(user_id):
    """Get user with caching"""
    
    @cache_region.cache_on_arguments()
    def _get_user(user_id):
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()
        session.close()
        return user
    
    return _get_user(user_id)

# Cache query results
@cache_region.cache_on_arguments()
def get_active_users():
    """Get all active users (cached)"""
    session = Session()
    users = session.query(User).filter(User.active == True).all()
    session.close()
    return users

# Invalidate cache
def update_user(user_id, new_data):
    """Update user and invalidate cache"""
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    user.name = new_data['name']
    session.commit()
    session.close()
    
    # Invalidate cache
    cache_region.delete(f'get_user_by_id|{user_id}')
```

### 2. Query Result Caching

**Description:** Cache raw query results

**Implementation:**

```python
import hashlib
import json

class QueryCache:
    def __init__(self, cache_backend):
        self.cache = cache_backend
    
    def _query_key(self, query, params):
        """Generate cache key from query and parameters"""
        query_str = f"{query}:{json.dumps(params, sort_keys=True)}"
        return f"query:{hashlib.md5(query_str.encode()).hexdigest()}"
    
    def execute_cached(self, query, params=None, ttl=3600):
        """Execute query with caching"""
        params = params or {}
        cache_key = self._query_key(query, params)
        
        # Try cache
        result = self.cache.get(cache_key)
        if result is not None:
            print("Query result from cache")
            return result
        
        # Execute query
        print("Executing query...")
        result = execute_database_query(query, params)
        
        # Cache result
        self.cache.set(cache_key, result, ttl=ttl)
        return result
    
    def invalidate_pattern(self, pattern):
        """Invalidate all queries matching pattern"""
        # For queries involving specific tables
        # Delete all cached queries for that table
        pass

# Usage
from redis import Redis
cache_backend = RedisCache()
query_cache = QueryCache(cache_backend)

# Cached query
users = query_cache.execute_cached(
    "SELECT * FROM users WHERE age > ?",
    params={'age': 18},
    ttl=1800
)

# Same query from cache
users = query_cache.execute_cached(
    "SELECT * FROM users WHERE age > ?",
    params={'age': 18}
)  # Returns from cache
```

---

## Web/API Caching

### 1. HTTP Caching Headers

**Description:** Browser and CDN caching via HTTP headers

**Advantages:**
✅ Reduces server load
✅ Reduces bandwidth
✅ Faster for users
✅ Standard protocol
✅ Free (browser-based)

**Disadvantages:**
❌ Limited control
❌ User can bypass
❌ Stale data issues

**Implementation:**

```python
from flask import Flask, make_response, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/api/static-data')
def static_data():
    """Data that rarely changes"""
    data = {'config': 'value', 'version': '1.0'}
    response = make_response(jsonify(data))
    
    # Cache for 1 hour
    response.headers['Cache-Control'] = 'public, max-age=3600'
    response.headers['Expires'] = (datetime.now() + timedelta(hours=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    return response

@app.route('/api/user-data')
def user_data():
    """User-specific data (don't cache)"""
    data = get_user_data()
    response = make_response(jsonify(data))
    
    # No caching
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    
    return response

@app.route('/api/ml-prediction')
def ml_prediction():
    """ML prediction with conditional caching"""
    # Use ETag for conditional requests
    data = get_prediction()
    response = make_response(jsonify(data))
    
    # Generate ETag from data
    import hashlib
    etag = hashlib.md5(str(data).encode()).hexdigest()
    response.headers['ETag'] = etag
    
    # Allow caching but validate
    response.headers['Cache-Control'] = 'private, must-revalidate'
    
    return response
```

### 2. API Response Caching

**Description:** Cache API responses at application level

**Implementation:**

```python
from flask import Flask, request
from functools import wraps
import json

app = Flask(__name__)
cache = RedisCache()

def cache_api_response(ttl=3600):
    """Decorator to cache API responses"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Generate cache key from URL and query params
            cache_key = f"api:{request.path}:{json.dumps(dict(request.args), sort_keys=True)}"
            
            # Try cache
            cached = cache.get(cache_key)
            if cached:
                return jsonify(cached), 200
            
            # Execute function
            result = f(*args, **kwargs)
            
            # Cache response
            if isinstance(result, tuple):
                data, status_code = result
            else:
                data, status_code = result, 200
            
            if status_code == 200:
                cache.set(cache_key, data, ttl=ttl)
            
            return jsonify(data), status_code
        
        return wrapped
    return decorator

@app.route('/api/predictions/<model_name>')
@cache_api_response(ttl=1800)  # Cache for 30 minutes
def get_predictions(model_name):
    """Get model predictions (cached)"""
    features = request.args.get('features')
    
    # This will be cached
    predictions = ml_model.predict(features)
    
    return {'predictions': predictions.tolist()}

@app.route('/api/user/<user_id>/recommendations')
@cache_api_response(ttl=300)  # Cache for 5 minutes
def get_recommendations(user_id):
    """Get user recommendations (cached)"""
    recommendations = recommendation_engine.get_recommendations(user_id)
    return {'recommendations': recommendations}
```

### 3. CDN Caching

**Description:** Content Delivery Network caching

**Advantages:**
✅ Global distribution
✅ Reduced origin load
✅ Fast for users worldwide
✅ DDoS protection
✅ Automatic scaling

**Disadvantages:**
❌ Cost
❌ Cache invalidation complexity
❌ Not for dynamic content
❌ Configuration complexity

**Use Cases:**
- Static ML model files
- Preprocessed datasets
- API documentation
- Images and assets
- Model serving endpoints (with versioning)

---

## ML Model Caching

### 1. Model Loading Cache

**Description:** Cache loaded ML models in memory

**Advantages:**
✅ Avoid repeated loading (2-5 seconds)
✅ Instant predictions
✅ Reduced I/O
✅ Better throughput

**Disadvantages:**
❌ Memory intensive (models can be GBs)
❌ Stale models if not invalidated
❌ Version management complexity

**Implementation:**

```python
import pickle
from functools import lru_cache
import threading

class ModelCache:
    def __init__(self):
        self.models = {}
        self.lock = threading.Lock()
    
    def load_model(self, model_path, version='latest'):
        """Load model with caching"""
        cache_key = f"{model_path}:{version}"
        
        # Check cache
        with self.lock:
            if cache_key in self.models:
                print(f"Model {cache_key} loaded from cache")
                return self.models[cache_key]
        
        # Load model
        print(f"Loading model {cache_key} from disk...")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Cache it
        with self.lock:
            self.models[cache_key] = model
        
        return model
    
    def unload_model(self, model_path, version='latest'):
        """Remove model from cache"""
        cache_key = f"{model_path}:{version}"
        with self.lock:
            if cache_key in self.models:
                del self.models[cache_key]
                print(f"Model {cache_key} unloaded")
    
    def clear(self):
        """Clear all cached models"""
        with self.lock:
            self.models.clear()
    
    def list_cached(self):
        """List all cached models"""
        return list(self.models.keys())

# Global model cache
model_cache = ModelCache()

# Usage
def predict(data, model_name='fraud_detector'):
    # Load model (cached after first call)
    model = model_cache.load_model(f'models/{model_name}.pkl')
    
    # Predict
    prediction = model.predict(data)
    return prediction

# First call: loads from disk (slow)
result1 = predict(data)

# Subsequent calls: uses cached model (fast)
result2 = predict(data)
result3 = predict(data)
```

### 2. Singleton Pattern for Models

**Implementation:**

```python
class ModelSingleton:
    _instance = None
    _model = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_model(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    print("Loading model (one-time)...")
                    self._model = load_heavy_model()
        return self._model

# Usage
model_singleton = ModelSingleton()

def predict(features):
    model = model_singleton.get_model()
    return model.predict(features)
```

### 3. Model Warm-Up

**Description:** Pre-load models on application startup

**Implementation:**

```python
class ModelManager:
    def __init__(self):
        self.models = {}
        self.warmup_models()
    
    def warmup_models(self):
        """Load all models on startup"""
        model_configs = [
            {'name': 'fraud_detector', 'path': 'models/fraud.pkl'},
            {'name': 'recommender', 'path': 'models/recommender.pkl'},
            {'name': 'classifier', 'path': 'models/classifier.pkl'},
        ]
        
        print("Warming up models...")
        for config in model_configs:
            print(f"  Loading {config['name']}...")
            with open(config['path'], 'rb') as f:
                self.models[config['name']] = pickle.load(f)
        print("All models loaded!")
    
    def get_model(self, name):
        return self.models.get(name)
    
    def reload_model(self, name, path):
        """Hot-reload a model"""
        print(f"Reloading {name}...")
        with open(path, 'rb') as f:
            self.models[name] = pickle.load(f)

# Initialize on app startup
model_manager = ModelManager()

# Models are ready immediately
model = model_manager.get_model('fraud_detector')
```

---

## Feature Caching

### Description

Cache computed features to avoid recalculation

**Advantages:**
✅ Avoid expensive feature computation
✅ Consistent features across requests
✅ Faster inference
✅ Reduced CPU usage

**Disadvantages:**
❌ Stale features if data changes
❌ Memory/storage overhead
❌ Invalidation complexity

**Implementation:**

```python
class FeatureCache:
    def __init__(self, cache_backend):
        self.cache = cache_backend
    
    def get_features(self, user_id, feature_version='v1'):
        """Get cached features or compute"""
        cache_key = f"features:{feature_version}:{user_id}"
        
        # Try cache
        features = self.cache.get(cache_key)
        if features is not None:
            return features
        
        # Compute features
        features = self._compute_features(user_id)
        
        # Cache with TTL (1 hour)
        self.cache.set(cache_key, features, ttl=3600)
        
        return features
    
    def _compute_features(self, user_id):
        """Expensive feature computation"""
        print(f"Computing features for user {user_id}...")
        
        # Get user data
        user_data = get_user_data(user_id)
        
        # Compute features
        features = {
            'age_normalized': user_data['age'] / 100,
            'income_log': np.log1p(user_data['income']),
            'days_since_signup': (datetime.now() - user_data['signup_date']).days,
            'purchase_frequency': user_data['total_purchases'] / user_data['days_active'],
            # ... many more expensive computations
        }
        
        return features
    
    def invalidate_features(self, user_id):
        """Invalidate cached features when user data changes"""
        # Delete all versions
        for version in ['v1', 'v2']:
            cache_key = f"features:{version}:{user_id}"
            self.cache.delete(cache_key)

# Usage
feature_cache = FeatureCache(RedisCache())

# Get features (computes first time)
features = feature_cache.get_features(user_id=123)

# Get again (from cache)
features = feature_cache.get_features(user_id=123)

# User updates profile
update_user_profile(user_id=123, new_data={...})
feature_cache.invalidate_features(user_id=123)

# Next call will recompute
features = feature_cache.get_features(user_id=123)
```

### Batch Feature Caching

**Implementation:**

```python
class BatchFeatureCache:
    def __init__(self, cache_backend):
        self.cache = cache_backend
    
    def get_batch_features(self, user_ids, feature_version='v1'):
        """Get features for multiple users (batch)"""
        
        # Generate cache keys
        cache_keys = [f"features:{feature_version}:{uid}" for uid in user_ids]
        
        # Batch get from cache
        cached_features = self.cache.get_many(cache_keys)
        
        # Find missing
        missing_user_ids = []
        for i, features in enumerate(cached_features):
            if features is None:
                missing_user_ids.append(user_ids[i])
        
        # Compute missing features
        if missing_user_ids:
            print(f"Computing features for {len(missing_user_ids)} users...")
            new_features = self._compute_batch_features(missing_user_ids)
            
            # Cache new features
            cache_data = {}
            for uid, features in zip(missing_user_ids, new_features):
                cache_key = f"features:{feature_version}:{uid}"
                cache_data[cache_key] = features
            
            self.cache.set_many(cache_data, ttl=3600)
            
            # Merge results
            result_dict = {uid: feat for uid, feat in zip(missing_user_ids, new_features)}
            for uid, feat in zip(user_ids, cached_features):
                if feat is not None:
                    result_dict[uid] = feat
            
            return [result_dict[uid] for uid in user_ids]
        
        return cached_features
    
    def _compute_batch_features(self, user_ids):
        """Compute features for multiple users efficiently"""
        # Batch database query
        users_data = get_users_data_batch(user_ids)
        
        # Vectorized feature computation
        features_list = []
        for user_data in users_data:
            features = compute_features(user_data)
            features_list.append(features)
        
        return features_list

# Usage
batch_cache = BatchFeatureCache(RedisCache())

# Get features for 1000 users
user_ids = list(range(1, 1001))
features = batch_cache.get_batch_features(user_ids)

# Most will be from cache on subsequent calls
features = batch_cache.get_batch_features(user_ids)
```

---

## Result Caching

### Description

Cache prediction results to avoid recomputation

**Implementation:**

```python
class PredictionCache:
    def __init__(self, cache_backend):
        self.cache = cache_backend
    
    def get_prediction(self, user_id, model_version, features_hash):
        """Get cached prediction"""
        cache_key = f"prediction:{model_version}:{user_id}:{features_hash}"
        
        prediction = self.cache.get(cache_key)
        if prediction is not None:
            print("Prediction from cache")
            return prediction
        
        # Not in cache
        return None
    
    def set_prediction(self, user_id, model_version, features_hash, prediction, ttl=3600):
        """Cache prediction result"""
        cache_key = f"prediction:{model_version}:{user_id}:{features_hash}"
        self.cache.set(cache_key, prediction, ttl=ttl)
    
    def predict_with_cache(self, user_id, features, model, model_version='v1'):
        """Make prediction with caching"""
        
        # Hash features for cache key
        features_hash = hashlib.md5(str(features).encode()).hexdigest()[:16]
        
        # Try cache
        prediction = self.get_prediction(user_id, model_version, features_hash)
        if prediction is not None:
            return prediction
        
        # Make prediction
        print("Computing prediction...")
        prediction = model.predict([features])[0]
        
        # Cache result
        self.set_prediction(user_id, model_version, features_hash, prediction, ttl=1800)
        
        return prediction

# Usage
pred_cache = PredictionCache(RedisCache())

features = [0.5, 0.3, 0.8, 0.2]
prediction = pred_cache.predict_with_cache(
    user_id=123,
    features=features,
    model=ml_model,
    model_version='v2.1'
)
```

---

## Cache Eviction Policies

### 1. LRU (Least Recently Used)

**Description:** Remove least recently accessed items

**Advantages:**
✅ Simple and effective
✅ Works well for temporal locality
✅ Good hit rate for typical workloads
✅ O(1) operations with proper implementation

**Disadvantages:**
❌ Doesn't consider access frequency
❌ Cache pollution from sequential scans
❌ Recent items may not be frequently used

**Implementation:**

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return None
        # Move to end (most recent)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def set(self, key, value):
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        # Evict if over capacity
        if len(self.cache) > self.capacity:
            # Remove first item (least recently used)
            oldest = next(iter(self.cache))
            print(f"Evicting {oldest} (LRU)")
            del self.cache[oldest]
    
    def __len__(self):
        return len(self.cache)

# Usage
lru = LRUCache(capacity=3)

lru.set('a', 1)
lru.set('b', 2)
lru.set('c', 3)
# Cache: a, b, c

lru.get('a')  # Access 'a'
# Cache: b, c, a (a moved to end)

lru.set('d', 4)  # Over capacity
# Evicts 'b' (least recently used)
# Cache: c, a, d
```

### 2. LFU (Least Frequently Used)

**Description:** Remove least frequently accessed items

**Advantages:**
✅ Considers access frequency
✅ Better for stable access patterns
✅ Protects popular items

**Disadvantages:**
❌ More complex implementation
❌ Requires frequency tracking
❌ Stale items can stay if accessed frequently in past

**Implementation:**

```python
from collections import defaultdict
import heapq

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> (value, frequency)
        self.freq_map = defaultdict(set)  # frequency -> set of keys
        self.min_freq = 0
        self.time = 0
    
    def get(self, key):
        if key not in self.cache:
            return None
        
        # Get value and update frequency
        value, freq = self.cache[key]
        self._update_freq(key, freq)
        
        return value
    
    def set(self, key, value):
        if self.capacity <= 0:
            return
        
        if key in self.cache:
            # Update existing
            _, freq = self.cache[key]
            self.cache[key] = (value, freq)
            self._update_freq(key, freq)
        else:
            # Add new
            if len(self.cache) >= self.capacity:
                # Evict LFU item
                self._evict()
            
            self.cache[key] = (value, 1)
            self.freq_map[1].add(key)
            self.min_freq = 1
    
    def _update_freq(self, key, freq):
        # Remove from old frequency
        self.freq_map[freq].discard(key)
        
        # Update min_freq if needed
        if not self.freq_map[freq] and freq == self.min_freq:
            self.min_freq += 1
        
        # Add to new frequency
        new_freq = freq + 1
        value, _ = self.cache[key]
        self.cache[key] = (value, new_freq)
        self.freq_map[new_freq].add(key)
    
    def _evict(self):
        # Remove one key with minimum frequency
        evict_key = self.freq_map[self.min_freq].pop()
        print(f"Evicting {evict_key} (LFU, freq={self.min_freq})")
        del self.cache[evict_key]

# Usage
lfu = LFUCache(capacity=3)

lfu.set('a', 1)  # freq: a=1
lfu.set('b', 2)  # freq: a=1, b=1
lfu.set('c', 3)  # freq: a=1, b=1, c=1

lfu.get('a')     # freq: a=2, b=1, c=1
lfu.get('a')     # freq: a=3, b=1, c=1
lfu.get('b')     # freq: a=3, b=2, c=1

lfu.set('d', 4)  # Evicts 'c' (LFU)
# freq: a=3, b=2, d=1
```

### 3. FIFO (First In First Out)

**Description:** Remove oldest inserted items

**Advantages:**
✅ Very simple
✅ Low overhead
✅ Predictable behavior

**Disadvantages:**
❌ Doesn't consider access patterns
❌ May evict frequently used items
❌ Poor hit rate

**Implementation:**

```python
from collections import deque

class FIFOCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.queue = deque()
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value):
        if key not in self.cache:
            if len(self.cache) >= self.capacity:
                # Evict oldest
                oldest = self.queue.popleft()
                print(f"Evicting {oldest} (FIFO)")
                del self.cache[oldest]
            
            self.queue.append(key)
        
        self.cache[key] = value

# Usage
fifo = FIFOCache(capacity=3)
fifo.set('a', 1)
fifo.set('b', 2)
fifo.set('c', 3)
fifo.set('d', 4)  # Evicts 'a'
```

### 4. TTL (Time To Live)

**Description:** Items expire after a time period

**Advantages:**
✅ Prevents stale data
✅ Automatic cleanup
✅ Predictable behavior

**Disadvantages:**
❌ May evict useful data
❌ Requires time tracking
❌ Expiry checks add overhead

**Implementation:**

```python
import time

class TTLCache:
    def __init__(self):
        self.cache = {}  # key -> (value, expiry_time)
    
    def get(self, key):
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                # Expired
                del self.cache[key]
        return None
    
    def set(self, key, value, ttl=3600):
        """Set value with TTL in seconds"""
        expiry = time.time() + ttl
        self.cache[key] = (value, expiry)
    
    def cleanup_expired(self):
        """Remove all expired items"""
        current_time = time.time()
        expired_keys = [
            k for k, (v, exp) in self.cache.items()
            if current_time >= exp
        ]
        for key in expired_keys:
            del self.cache[key]
        return len(expired_keys)

# Usage
ttl_cache = TTLCache()

ttl_cache.set('temp_data', 'value', ttl=5)  # 5 seconds
print(ttl_cache.get('temp_data'))  # 'value'

time.sleep(6)
print(ttl_cache.get('temp_data'))  # None (expired)
```

### Eviction Policy Comparison

| Policy | Use Case | Pros | Cons |
|--------|----------|------|------|
| **LRU** | General purpose | Simple, effective | May evict frequent items |
| **LFU** | Stable patterns | Protects popular items | Complex, stale data risk |
| **FIFO** | Simple needs | Very simple | Poor hit rate |
| **TTL** | Time-sensitive | Prevents stale data | May evict useful data |
| **Random** | Unknown pattern | No overhead | Unpredictable |
| **LRU-K** | Database | Better than LRU | More complex |

---

## Python Caching Implementations

### 1. functools.lru_cache (Built-in)

**Description:** Least Recently Used cache decorator (Python standard library)

**Advantages:**
✅ Built into Python (no dependencies)
✅ Very easy to use (decorator)
✅ Thread-safe
✅ Cache statistics
✅ Zero configuration
✅ Fast (C implementation)

**Disadvantages:**
❌ Memory-only (lost on restart)
❌ No TTL support
❌ No distributed caching
❌ Limited to 128 items by default
❌ Can't cache unhashable arguments
❌ All or nothing caching

**Implementation:**

```python
from functools import lru_cache, wraps
import time

# Basic usage
@lru_cache(maxsize=128)
def fibonacci(n):
    """Cached fibonacci calculation"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Without cache: fibonacci(30) takes ~0.5 seconds
# With cache: fibonacci(30) takes ~0.0001 seconds

print(fibonacci(30))  # Computes and caches
print(fibonacci(30))  # Returns from cache
print(fibonacci.cache_info())
# CacheInfo(hits=28, misses=31, maxsize=128, currsize=31)

# Clear cache
fibonacci.cache_clear()

# Advanced usage with typed parameter
@lru_cache(maxsize=256, typed=True)
def add(a, b):
    """Typed cache: add(1, 2) and add(1.0, 2.0) cached separately"""
    print(f"Computing {a} + {b}")
    return a + b

add(1, 2)      # Computes (int)
add(1.0, 2.0)  # Computes (float) - different cache entry
add(1, 2)      # From cache

# Custom LRU cache with TTL
def lru_cache_with_ttl(maxsize=128, ttl=3600):
    """LRU cache with time-to-live"""
    def decorator(func):
        cache = {}
        cache_times = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            current_time = time.time()
            
            # Check if in cache and not expired
            if key in cache:
                if current_time - cache_times[key] < ttl:
                    return cache[key]
                else:
                    # Expired
                    del cache[key]
                    del cache_times[key]
            
            # Compute
            result = func(*args, **kwargs)
            
            # Store in cache
            cache[key] = result
            cache_times[key] = current_time
            
            # Evict if over size (LRU)
            if len(cache) > maxsize:
                # Remove oldest
                oldest_key = min(cache_times.keys(), key=lambda k: cache_times[k])
                del cache[oldest_key]
                del cache_times[oldest_key]
            
            return result
        
        return wrapper
    return decorator

@lru_cache_with_ttl(maxsize=100, ttl=5)
def get_data(key):
    print(f"Fetching {key}...")
    return f"data_{key}"

print(get_data('user_1'))  # Fetches
print(get_data('user_1'))  # From cache
time.sleep(6)
print(get_data('user_1'))  # Fetches (expired)
```

### 2. cachetools Library

**Description:** Extensible caching library with multiple strategies

**Advantages:**
✅ Multiple cache types (LRU, LFU, TTL, etc.)
✅ Decorator support
✅ Size-limited and time-limited
✅ Thread-safe variants
✅ Custom cache implementations
✅ More flexible than functools

**Disadvantages:**
❌ External dependency
❌ Memory-only
❌ No distributed caching
❌ Manual cleanup for TTL

**Implementation:**

```python
from cachetools import LRUCache, LFUCache, TTLCache, cached
from cachetools.keys import hashkey
import time

# 1. LRU Cache
lru = LRUCache(maxsize=100)

@cached(cache=lru)
def expensive_function(x, y):
    print(f"Computing {x} * {y}...")
    return x * y

print(expensive_function(5, 3))  # Computes
print(expensive_function(5, 3))  # From cache

# 2. LFU Cache (Least Frequently Used)
lfu = LFUCache(maxsize=100)

@cached(cache=lfu)
def get_user_data(user_id):
    print(f"Fetching user {user_id}...")
    return {'id': user_id, 'name': f'User {user_id}'}

# 3. TTL Cache (Time To Live)
ttl_cache = TTLCache(maxsize=100, ttl=5)  # 5 seconds

@cached(cache=ttl_cache)
def get_current_price(symbol):
    print(f"Fetching price for {symbol}...")
    return f"${100.0}"

print(get_current_price('AAPL'))  # Fetches
print(get_current_price('AAPL'))  # From cache
time.sleep(6)
print(get_current_price('AAPL'))  # Fetches (expired)

# 4. Custom key function
def custom_key(user_id, include_details=False):
    """Custom cache key that ignores include_details parameter"""
    return hashkey(user_id)

@cached(cache=LRUCache(maxsize=100), key=custom_key)
def get_user(user_id, include_details=False):
    print(f"Fetching user {user_id}...")
    data = {'id': user_id, 'name': f'User {user_id}'}
    if include_details:
        data['details'] = 'Extra details...'
    return data

# Both calls use same cache entry
get_user(1, include_details=True)
get_user(1, include_details=False)  # From cache

# 5. Thread-safe caching
from cachetools import cached, TTLCache
from threading import RLock

cache = TTLCache(maxsize=100, ttl=60)
lock = RLock()

@cached(cache=cache, lock=lock)
def thread_safe_function(x):
    time.sleep(0.1)
    return x * 2

# Safe for multi-threaded use
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(thread_safe_function, range(100)))
```

### 3. diskcache Library

**Description:** Disk-based caching with SQLite backend

**Advantages:**
✅ Persistent across restarts
✅ No memory limits (uses disk)
✅ Fast (SQLite backend)
✅ Thread and process safe
✅ Multiple eviction policies
✅ Built-in data structures (deque, etc.)
✅ Index support

**Disadvantages:**
❌ Slower than memory cache
❌ Disk I/O overhead
❌ Not distributed
❌ File locking on Windows

**Implementation:**

```python
from diskcache import Cache, FanoutCache
import time

# Basic cache
cache = Cache('./cache_dir')

# Set and get
cache.set('key', 'value', expire=60)  # 60 seconds TTL
value = cache.get('key')

# Decorator usage
@cache.memoize(expire=3600, typed=True)
def expensive_computation(n):
    print(f"Computing for {n}...")
    time.sleep(1)
    return n ** 2

print(expensive_computation(5))  # Computes
print(expensive_computation(5))  # From disk cache

# Clear cache
cache.clear()

# Advanced: FanoutCache (better for concurrent access)
fanout_cache = FanoutCache('./fanout_cache', shards=8)

@fanout_cache.memoize(expire=3600)
def ml_feature_extraction(data_id):
    """Extract features with persistent caching"""
    print(f"Extracting features for {data_id}...")
    # Expensive feature extraction
    features = extract_features(data_id)
    return features

# Multiple processes can access safely
features = ml_feature_extraction(123)

# Cache statistics
print(cache.stats())
# {'hits': 5, 'misses': 3}

# Set with tags for bulk operations
cache.set('user:1', data1, tag='user_data')
cache.set('user:2', data2, tag='user_data')

# Evict by tag
cache.evict(tag='user_data')

# Close cache
cache.close()
```

### 4. Redis with Python Libraries

**redis-py (Standard Client):**

```python
import redis
import json
import pickle
from functools import wraps

class RedisLRUCache:
    def __init__(self, host='localhost', port=6379, db=0, maxsize=1000):
        self.client = redis.Redis(host=host, port=port, db=db)
        self.maxsize = maxsize
        self.cache_key = 'cache_keys'
    
    def _serialize(self, value):
        return pickle.dumps(value)
    
    def _deserialize(self, value):
        if value:
            return pickle.loads(value)
        return None
    
    def set(self, key, value, ttl=3600):
        """Set with LRU tracking"""
        # Serialize value
        serialized = self._serialize(value)
        
        # Set value with TTL
        self.client.setex(key, ttl, serialized)
        
        # Track in sorted set (for LRU)
        self.client.zadd(self.cache_key, {key: time.time()})
        
        # Evict if over size
        size = self.client.zcard(self.cache_key)
        if size > self.maxsize:
            # Remove oldest
            oldest = self.client.zrange(self.cache_key, 0, 0)
            if oldest:
                oldest_key = oldest[0].decode('utf-8')
                self.client.delete(oldest_key)
                self.client.zrem(self.cache_key, oldest_key)
    
    def get(self, key):
        """Get with LRU update"""
        value = self.client.get(key)
        if value:
            # Update access time
            self.client.zadd(self.cache_key, {key: time.time()})
            return self._deserialize(value)
        return None
    
    def cached(self, ttl=3600):
        """Decorator for caching functions"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = f"{func.__name__}:{args}:{kwargs}"
                
                # Try cache
                result = self.get(cache_key)
                if result is not None:
                    return result
                
                # Compute
                result = func(*args, **kwargs)
                
                # Cache
                self.set(cache_key, result, ttl=ttl)
                
                return result
            return wrapper
        return decorator

# Usage
redis_cache = RedisLRUCache(maxsize=1000)

@redis_cache.cached(ttl=1800)
def get_recommendations(user_id):
    print(f"Computing recommendations for {user_id}...")
    # Expensive recommendation computation
    return ['item1', 'item2', 'item3']

# First call: computes
recommendations = get_recommendations(123)

# Second call: from cache
recommendations = get_recommendations(123)
```

### 5. requests-cache (HTTP Caching)

**Description:** Cache HTTP requests automatically

**Advantages:**
✅ Automatic HTTP caching
✅ Multiple backends (SQLite, Redis, MongoDB)
✅ Respects HTTP cache headers
✅ TTL support
✅ URL pattern filtering
✅ Easy integration

**Disadvantages:**
❌ Only for HTTP requests
❌ Overhead for simple requests
❌ May cache errors

**Implementation:**

```python
import requests_cache
import requests

# Install session with caching
requests_cache.install_cache(
    'api_cache',
    backend='sqlite',
    expire_after=3600  # 1 hour
)

# Now all requests are cached
response = requests.get('https://api.example.com/data')  # Fetches
response = requests.get('https://api.example.com/data')  # From cache

print(f"From cache: {response.from_cache}")

# Per-request expiration
response = requests.get(
    'https://api.example.com/fresh-data',
    expire_after=60  # 1 minute
)

# Don't cache specific request
response = requests.get(
    'https://api.example.com/no-cache',
    expire_after=-1  # Never cache
)

# Clear cache
requests_cache.clear()

# Uninstall (back to normal requests)
requests_cache.uninstall_cache()

# Session-based caching
session = requests_cache.CachedSession(
    'ml_api_cache',
    backend='redis',
    expire_after=1800
)

# Use session for API calls
def get_model_predictions(data):
    response = session.post(
        'https://ml-api.com/predict',
        json={'data': data}
    )
    return response.json()
```

### 6. Flask-Caching (Web Framework)

**Description:** Caching for Flask web applications

**Implementation:**

```python
from flask import Flask
from flask_caching import Cache

app = Flask(__name__)

# Configure cache
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_DEFAULT_TIMEOUT': 300
})

# Cache view function
@app.route('/expensive')
@cache.cached(timeout=600)
def expensive_route():
    """Cached for 10 minutes"""
    result = expensive_computation()
    return {'result': result}

# Cache with key prefix
@app.route('/user/<int:user_id>')
@cache.cached(timeout=300, key_prefix='user_profile')
def user_profile(user_id):
    user = get_user_from_db(user_id)
    return user

# Memoize function (cache based on arguments)
@cache.memoize(timeout=600)
def get_user_recommendations(user_id, category):
    """Cache depends on user_id AND category"""
    return compute_recommendations(user_id, category)

# Manual caching
def process_data(data_id):
    cache_key = f'processed_data:{data_id}'
    
    # Try cache
    result = cache.get(cache_key)
    if result:
        return result
    
    # Process
    result = heavy_processing(data_id)
    
    # Store
    cache.set(cache_key, result, timeout=3600)
    return result

# Delete specific cache
@app.route('/user/<int:user_id>/update', methods=['POST'])
def update_user(user_id):
    # Update user
    update_user_in_db(user_id)
    
    # Invalidate cache
    cache.delete(f'user_profile/{user_id}')
    
    return {'status': 'updated'}

# Clear all cache
cache.clear()
```

---

## ML/AI Specific Caching

### 1. TensorFlow Model Caching

**Description:** Cache TensorFlow models and predictions

**Implementation:**

```python
import tensorflow as tf
import numpy as np
import pickle
import hashlib

class TensorFlowModelCache:
    def __init__(self):
        self.models = {}
        self.predictions_cache = {}
    
    def load_model(self, model_path):
        """Load and cache TensorFlow model"""
        if model_path in self.models:
            print(f"Model {model_path} loaded from cache")
            return self.models[model_path]
        
        print(f"Loading model {model_path}...")
        model = tf.keras.models.load_model(model_path)
        self.models[model_path] = model
        return model
    
    def predict_cached(self, model_path, input_data):
        """Predict with caching"""
        # Generate cache key from input
        input_hash = hashlib.md5(input_data.tobytes()).hexdigest()
        cache_key = f"{model_path}:{input_hash}"
        
        # Check prediction cache
        if cache_key in self.predictions_cache:
            print("Prediction from cache")
            return self.predictions_cache[cache_key]
        
        # Load model (cached)
        model = self.load_model(model_path)
        
        # Predict
        print("Computing prediction...")
        prediction = model.predict(input_data)
        
        # Cache prediction
        self.predictions_cache[cache_key] = prediction
        
        return prediction
    
    def clear_predictions(self):
        """Clear prediction cache (keep models)"""
        self.predictions_cache.clear()
    
    def clear_models(self):
        """Clear model cache"""
        self.models.clear()

# Usage
tf_cache = TensorFlowModelCache()

# First prediction: loads model and computes
input_data = np.random.randn(1, 224, 224, 3)
prediction = tf_cache.predict_cached('models/resnet50.h5', input_data)

# Same input: returns from cache
prediction = tf_cache.predict_cached('models/resnet50.h5', input_data)

# Different input: computes but model already cached
input_data2 = np.random.randn(1, 224, 224, 3)
prediction2 = tf_cache.predict_cached('models/resnet50.h5', input_data2)
```

### 2. PyTorch Model Caching

**Implementation:**

```python
import torch
import torch.nn as nn
import hashlib
import pickle

class PyTorchModelCache:
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.models = {}
        self.device = device
        self.prediction_cache = {}
    
    def load_model(self, model_path, model_class=None):
        """Load and cache PyTorch model"""
        if model_path in self.models:
            print(f"Model {model_path} loaded from cache")
            return self.models[model_path]
        
        print(f"Loading model {model_path}...")
        
        if model_class:
            # Load with model class
            model = model_class()
            model.load_state_dict(torch.load(model_path, map_location=self.device))
        else:
            # Load entire model
            model = torch.load(model_path, map_location=self.device)
        
        model.eval()
        model.to(self.device)
        
        self.models[model_path] = model
        return model
    
    @torch.no_grad()
    def predict_cached(self, model_path, input_tensor, model_class=None):
        """Predict with caching"""
        # Generate cache key
        input_hash = hashlib.md5(input_tensor.cpu().numpy().tobytes()).hexdigest()
        cache_key = f"{model_path}:{input_hash}"
        
        # Check cache
        if cache_key in self.prediction_cache:
            print("Prediction from cache")
            return self.prediction_cache[cache_key]
        
        # Load model (cached)
        model = self.load_model(model_path, model_class)
        
        # Predict
        print("Computing prediction...")
        input_tensor = input_tensor.to(self.device)
        output = model(input_tensor)
        
        # Cache output (move to CPU for storage)
        self.prediction_cache[cache_key] = output.cpu()
        
        return output
    
    def warm_up_model(self, model_path, input_shape, model_class=None):
        """Warm up model with dummy input"""
        model = self.load_model(model_path, model_class)
        dummy_input = torch.randn(input_shape).to(self.device)
        
        # Run inference to warm up
        with torch.no_grad():
            _ = model(dummy_input)
        
        print(f"Model {model_path} warmed up")

# Usage
pytorch_cache = PyTorchModelCache()

# Define model class
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 2)
    
    def forward(self, x):
        return self.fc(x)

# Warm up model
pytorch_cache.warm_up_model('models/my_model.pth', (1, 10), MyModel)

# Predict with caching
input_tensor = torch.randn(1, 10)
output = pytorch_cache.predict_cached('models/my_model.pth', input_tensor, MyModel)

# From cache
output = pytorch_cache.predict_cached('models/my_model.pth', input_tensor, MyModel)
```

### 3. Scikit-learn Pipeline Caching

**Implementation:**

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import hashlib
import numpy as np

class SklearnPipelineCache:
    def __init__(self, cache_dir='./sklearn_cache'):
        self.cache_dir = cache_dir
        self.pipelines = {}
        self.memory = joblib.Memory(cache_dir, verbose=0)
    
    def load_pipeline(self, pipeline_path):
        """Load and cache sklearn pipeline"""
        if pipeline_path in self.pipelines:
            print(f"Pipeline {pipeline_path} loaded from cache")
            return self.pipelines[pipeline_path]
        
        print(f"Loading pipeline {pipeline_path}...")
        pipeline = joblib.load(pipeline_path)
        self.pipelines[pipeline_path] = pipeline
        return pipeline
    
    @joblib.Memory.cache
    def transform_cached(self, data_hash, pipeline, X):
        """Cached transformation"""
        print("Transforming data...")
        return pipeline.transform(X)
    
    def predict_cached(self, pipeline_path, X):
        """Predict with caching of transformations"""
        # Load pipeline (cached)
        pipeline = self.load_pipeline(pipeline_path)
        
        # Hash input data
        data_hash = hashlib.md5(X.tobytes()).hexdigest()
        
        # Check if we have cached transformations
        cache_key = f"{pipeline_path}:{data_hash}"
        
        # Predict (transforms are cached via joblib)
        print("Predicting...")
        prediction = pipeline.predict(X)
        
        return prediction
    
    def clear_cache(self):
        """Clear transformation cache"""
        self.memory.clear()

# Usage
sklearn_cache = SklearnPipelineCache()

# Create and save pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier())
])

X_train = np.random.randn(1000, 10)
y_train = np.random.randint(0, 2, 1000)
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, 'models/pipeline.pkl')

# Predict with caching
X_test = np.random.randn(100, 10)

# First call: loads pipeline and transforms
predictions = sklearn_cache.predict_cached('models/pipeline.pkl', X_test)

# Second call: uses cached pipeline
predictions = sklearn_cache.predict_cached('models/pipeline.pkl', X_test)
```

### 4. Hugging Face Transformers Caching

**Description:** Cache transformer models and tokenizers

**Implementation:**

```python
from transformers import AutoTokenizer, AutoModel
import torch
import os

# Set cache directory
os.environ['TRANSFORMERS_CACHE'] = './hf_cache'

class TransformerCache:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
    
    def load_model(self, model_name):
        """Load and cache transformer model"""
        if model_name in self.models:
            print(f"Model {model_name} loaded from memory cache")
            return self.models[model_name]
        
        print(f"Loading model {model_name}...")
        # Hugging Face automatically caches downloaded models
        model = AutoModel.from_pretrained(model_name)
        model.eval()
        
        self.models[model_name] = model
        return model
    
    def load_tokenizer(self, model_name):
        """Load and cache tokenizer"""
        if model_name in self.tokenizers:
            return self.tokenizers[model_name]
        
        print(f"Loading tokenizer {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizers[model_name] = tokenizer
        return tokenizer
    
    def encode_cached(self, model_name, text):
        """Encode text with caching"""
        # Load tokenizer (cached)
        tokenizer = self.load_tokenizer(model_name)
        
        # Load model (cached)
        model = self.load_model(model_name)
        
        # Encode
        with torch.no_grad():
            inputs = tokenizer(text, return_tensors='pt', padding=True)
            outputs = model(**inputs)
        
        return outputs

# Usage
hf_cache = TransformerCache()

# First call: downloads and caches model
outputs = hf_cache.encode_cached('bert-base-uncased', 'Hello world')

# Second call: uses cached model
outputs = hf_cache.encode_cached('bert-base-uncased', 'Another text')
```

### 5. Feature Store Integration

**Description:** Cache features in a feature store

**Implementation:**

```python
import pandas as pd
from datetime import datetime, timedelta

class FeatureStore:
    def __init__(self, cache_backend):
        self.cache = cache_backend
        self.feature_ttl = {
            'user_demographics': 86400,  # 1 day
            'user_behavior': 3600,       # 1 hour
            'real_time_features': 300,   # 5 minutes
        }
    
    def get_features(self, entity_id, feature_groups):
        """Get features from cache or compute"""
        features = {}
        missing_groups = []
        
        # Try to get from cache
        for group in feature_groups:
            cache_key = f"features:{group}:{entity_id}"
            cached = self.cache.get(cache_key)
            
            if cached is not None:
                features[group] = cached
            else:
                missing_groups.append(group)
        
        # Compute missing features
        if missing_groups:
            computed = self._compute_features(entity_id, missing_groups)
            
            # Cache computed features
            for group, group_features in computed.items():
                cache_key = f"features:{group}:{entity_id}"
                ttl = self.feature_ttl.get(group, 3600)
                self.cache.set(cache_key, group_features, ttl=ttl)
                features[group] = group_features
        
        # Combine all features
        return self._combine_features(features)
    
    def _compute_features(self, entity_id, feature_groups):
        """Compute features from raw data"""
        features = {}
        
        for group in feature_groups:
            if group == 'user_demographics':
                features[group] = self._compute_demographics(entity_id)
            elif group == 'user_behavior':
                features[group] = self._compute_behavior(entity_id)
            elif group == 'real_time_features':
                features[group] = self._compute_realtime(entity_id)
        
        return features
    
    def _compute_demographics(self, user_id):
        """Compute demographic features"""
        print(f"Computing demographics for user {user_id}...")
        user = get_user_from_db(user_id)
        return {
            'age': user['age'],
            'gender': user['gender'],
            'location': user['location'],
        }
    
    def _compute_behavior(self, user_id):
        """Compute behavioral features"""
        print(f"Computing behavior for user {user_id}...")
        # Query user activity
        return {
            'total_purchases': 10,
            'avg_order_value': 50.0,
            'last_purchase_days': 5,
        }
    
    def _compute_realtime(self, user_id):
        """Compute real-time features"""
        print(f"Computing real-time features for user {user_id}...")
        return {
            'current_session_length': 120,
            'pages_viewed': 5,
        }
    
    def _combine_features(self, features):
        """Combine feature groups"""
        combined = {}
        for group_features in features.values():
            combined.update(group_features)
        return combined
    
    def batch_get_features(self, entity_ids, feature_groups):
        """Get features for multiple entities"""
        results = {}
        
        for entity_id in entity_ids:
            results[entity_id] = self.get_features(entity_id, feature_groups)
        
        return results
    
    def invalidate_features(self, entity_id, feature_groups=None):
        """Invalidate cached features"""
        if feature_groups is None:
            feature_groups = self.feature_ttl.keys()
        
        for group in feature_groups:
            cache_key = f"features:{group}:{entity_id}"
            self.cache.delete(cache_key)

# Usage
feature_store = FeatureStore(RedisCache())

# Get features for user (caches automatically)
features = feature_store.get_features(
    entity_id=123,
    feature_groups=['user_demographics', 'user_behavior', 'real_time_features']
)

# Subsequent calls use cache
features = feature_store.get_features(
    entity_id=123,
    feature_groups=['user_demographics', 'user_behavior']
)

# Batch get
batch_features = feature_store.batch_get_features(
    entity_ids=[123, 456, 789],
    feature_groups=['user_demographics', 'user_behavior']
)

# Invalidate when user updates profile
update_user_profile(user_id=123)
feature_store.invalidate_features(123, ['user_demographics'])
```

---

## Cache Invalidation Strategies

### "There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

### 1. Time-Based Invalidation (TTL)

**Description:** Expire cache after fixed time period

**Advantages:**
✅ Simple to implement
✅ Automatic cleanup
✅ Predictable behavior
✅ Works well for slowly changing data

**Disadvantages:**
❌ May serve stale data
❌ Doesn't reflect actual changes
❌ Fixed expiry may not fit all data

**Implementation:**

```python
class TTLInvalidation:
    def __init__(self, cache):
        self.cache = cache
        self.default_ttl = 3600
        
        # Different TTLs for different data types
        self.ttl_config = {
            'user_profile': 3600,      # 1 hour
            'product_catalog': 1800,   # 30 minutes
            'recommendations': 600,    # 10 minutes
            'real_time_data': 60,      # 1 minute
            'analytics': 86400,        # 1 day
        }
    
    def set(self, key, value, data_type='default'):
        """Set with appropriate TTL"""
        ttl = self.ttl_config.get(data_type, self.default_ttl)
        self.cache.set(key, value, ttl=ttl)
    
    def get(self, key):
        """Get (auto-expires via TTL)"""
        return self.cache.get(key)

# Usage
ttl_cache = TTLInvalidation(RedisCache())

# Set with appropriate TTL based on data type
ttl_cache.set('user:123', user_data, data_type='user_profile')
ttl_cache.set('recommendations:123', recs, data_type='recommendations')
```

### 2. Event-Based Invalidation

**Description:** Invalidate when specific events occur

**Advantages:**
✅ Always fresh data
✅ No stale data
✅ Efficient (only invalidate when changed)

**Disadvantages:**
❌ Complex to implement
❌ Need to track all events
❌ Potential for missed invalidations

**Implementation:**

```python
class EventBasedInvalidation:
    def __init__(self, cache):
        self.cache = cache
        self.invalidation_rules = {}
    
    def register_rule(self, event_type, cache_keys_func):
        """
        Register invalidation rule
        
        event_type: Name of event
        cache_keys_func: Function that returns keys to invalidate
        """
        self.invalidation_rules[event_type] = cache_keys_func
    
    def on_event(self, event_type, event_data):
        """Handle event and invalidate cache"""
        if event_type in self.invalidation_rules:
            # Get keys to invalidate
            keys_to_invalidate = self.invalidation_rules[event_type](event_data)
            
            # Invalidate
            for key in keys_to_invalidate:
                print(f"Invalidating {key} due to {event_type}")
                self.cache.delete(key)

# Usage
event_invalidation = EventBasedInvalidation(RedisCache())

# Register invalidation rules
def user_update_invalidation(event_data):
    """Invalidate user-related caches on update"""
    user_id = event_data['user_id']
    return [
        f'user_profile:{user_id}',
        f'user_features:{user_id}',
        f'user_recommendations:{user_id}',
    ]

def product_update_invalidation(event_data):
    """Invalidate product-related caches"""
    product_id = event_data['product_id']
    return [
        f'product:{product_id}',
        f'product_recommendations',  # Invalidate all recommendations
        'product_catalog',
    ]

event_invalidation.register_rule('user_updated', user_update_invalidation)
event_invalidation.register_rule('product_updated', product_update_invalidation)

# When events occur
def update_user(user_id, new_data):
    # Update database
    db.update_user(user_id, new_data)
    
    # Trigger invalidation
    event_invalidation.on_event('user_updated', {'user_id': user_id})

def update_product(product_id, new_data):
    # Update database
    db.update_product(product_id, new_data)
    
    # Trigger invalidation
    event_invalidation.on_event('product_updated', {'product_id': product_id})
```

### 3. Version-Based Invalidation

**Description:** Include version in cache key

**Advantages:**
✅ No explicit invalidation needed
✅ Can deploy new versions gradually
✅ Easy rollback
✅ No race conditions

**Disadvantages:**
❌ Old versions remain in cache (waste space)
❌ Need cleanup mechanism
❌ Version management overhead

**Implementation:**

```python
class VersionedCache:
    def __init__(self, cache):
        self.cache = cache
        self.current_versions = {}
    
    def set_version(self, namespace, version):
        """Set current version for namespace"""
        self.current_versions[namespace] = version
    
    def get_version(self, namespace):
        """Get current version"""
        return self.current_versions.get(namespace, 'v1')
    
    def set(self, namespace, key, value, ttl=3600):
        """Set with version"""
        version = self.get_version(namespace)
        versioned_key = f"{namespace}:{version}:{key}"
        self.cache.set(versioned_key, value, ttl=ttl)
    
    def get(self, namespace, key):
        """Get with version"""
        version = self.get_version(namespace)
        versioned_key = f"{namespace}:{version}:{key}"
        return self.cache.get(versioned_key)
    
    def bump_version(self, namespace):
        """Increment version (invalidates all)"""
        current = self.get_version(namespace)
        
        # Parse version (assuming format like 'v1', 'v2', etc.)
        version_num = int(current.replace('v', ''))
        new_version = f'v{version_num + 1}'
        
        self.set_version(namespace, new_version)
        print(f"Bumped {namespace} version: {current} -> {new_version}")
        
        return new_version

# Usage
versioned_cache = VersionedCache(RedisCache())

# Set initial versions
versioned_cache.set_version('user_features', 'v1')
versioned_cache.set_version('product_recommendations', 'v1')

# Use cache
versioned_cache.set('user_features', '123', features_v1)
versioned_cache.set('product_recommendations', '456', recs_v1)

# Get (uses current version)
features = versioned_cache.get('user_features', '123')

# Deploy new feature calculation logic
# Simply bump the version
versioned_cache.bump_version('user_features')

# Old cache is ignored, new features will be computed
features_new = versioned_cache.get('user_features', '123')  # None (new version)

# Recompute with new logic
features_v2 = compute_features_v2('123')
versioned_cache.set('user_features', '123', features_v2)
```

### 4. Write-Through Cache

**Description:** Update cache when writing to database

**Advantages:**
✅ Always consistent
✅ No stale data
✅ Simple invalidation

**Disadvantages:**
❌ Write latency (write to both)
❌ Complexity if write fails
❌ Transaction management needed

**Implementation:**

```python
class WriteThroughCache:
    def __init__(self, cache, database):
        self.cache = cache
        self.db = database
    
    def get(self, key):
        """Get from cache or database"""
        # Try cache first
        value = self.cache.get(key)
        if value is not None:
            return value
        
        # Cache miss - get from database
        value = self.db.get(key)
        if value is not None:
            # Populate cache
            self.cache.set(key, value)
        
        return value
    
    def set(self, key, value):
        """Write to both cache and database"""
        # Write to database first
        self.db.set(key, value)
        
        # Update cache
        self.cache.set(key, value)
    
    def delete(self, key):
        """Delete from both"""
        self.db.delete(key)
        self.cache.delete(key)

# Usage
write_through = WriteThroughCache(RedisCache(), database)

# Write (updates both)
write_through.set('user:123', user_data)

# Read (from cache)
user = write_through.get('user:123')
```

### 5. Cache-Aside (Lazy Loading)

**Description:** Application manages cache explicitly

**Advantages:**
✅ Simple
✅ Only cache what's needed
✅ Cache misses don't fail

**Disadvantages:**
❌ Application complexity
❌ Potential for stale data
❌ Cache stampede risk

**Implementation:**

```python
class CacheAside:
    def __init__(self, cache, database):
        self.cache = cache
        self.db = database
    
    def get(self, key, ttl=3600):
        """Get with cache-aside pattern"""
        # Try cache
        value = self.cache.get(key)
        if value is not None:
            return value
        
        # Cache miss - get from database
        value = self.db.get(key)
        if value is not None:
            # Populate cache
            self.cache.set(key, value, ttl=ttl)
        
        return value
    
    def update(self, key, value):
        """Update database and invalidate cache"""
        # Update database
        self.db.update(key, value)
        
        # Invalidate cache (don't update it)
        self.cache.delete(key)
        
        # Next read will repopulate cache

# Usage
cache_aside = CacheAside(RedisCache(), database)

# Read (cache-aside)
user = cache_aside.get('user:123')

# Update (invalidates cache)
cache_aside.update('user:123', new_user_data)
```

### 6. Dependency-Based Invalidation

**Description:** Invalidate caches with dependencies

**Implementation:**

```python
class DependencyInvalidation:
    def __init__(self, cache):
        self.cache = cache
        self.dependencies = {}  # cache_key -> [dependent_keys]
    
    def register_dependency(self, parent_key, dependent_keys):
        """Register cache dependencies"""
        if parent_key not in self.dependencies:
            self.dependencies[parent_key] = []
        self.dependencies[parent_key].extend(dependent_keys)
    
    def invalidate(self, key):
        """Invalidate key and all dependents"""
        keys_to_invalidate = [key]
        
        # Find all dependent keys recursively
        def find_dependents(k):
            if k in self.dependencies:
                for dep_key in self.dependencies[k]:
                    if dep_key not in keys_to_invalidate:
                        keys_to_invalidate.append(dep_key)
                        find_dependents(dep_key)
        
        find_dependents(key)
        
        # Invalidate all
        for k in keys_to_invalidate:
            print(f"Invalidating {k}")
            self.cache.delete(k)
        
        return keys_to_invalidate

# Usage
dep_cache = DependencyInvalidation(RedisCache())

# Register dependencies
# When user profile changes, recommendations depend on it
dep_cache.register_dependency(
    'user_profile:123',
    ['user_recommendations:123', 'user_feed:123']
)

# When product changes, recommendations depend on it
dep_cache.register_dependency(
    'product:456',
    ['product_recommendations', 'homepage_feed']
)

# Invalidate user profile (also invalidates recommendations and feed)
dep_cache.invalidate('user_profile:123')
# Invalidates: user_profile:123, user_recommendations:123, user_feed:123
```

---

## Performance Comparison

### Caching Performance Benchmarks

```python
import time
import numpy as np
from functools import lru_cache

def benchmark_cache_performance():
    """Compare different caching strategies"""
    
    # Test data
    def expensive_computation(x):
        """Simulate expensive operation"""
        time.sleep(0.01)  # 10ms operation
        return x ** 2
    
    # 1. No Cache
    start = time.time()
    results = []
    for i in range(100):
        results.append(expensive_computation(i % 10))  # Repeat pattern
    no_cache_time = time.time() - start
    
    # 2. LRU Cache (functools)
    @lru_cache(maxsize=128)
    def expensive_cached_lru(x):
        time.sleep(0.01)
        return x ** 2
    
    start = time.time()
    results = []
    for i in range(100):
        results.append(expensive_cached_lru(i % 10))
    lru_time = time.time() - start
    
    # 3. Dictionary Cache
    dict_cache = {}
    def expensive_cached_dict(x):
        if x in dict_cache:
            return dict_cache[x]
        result = expensive_computation(x)
        dict_cache[x] = result
        return result
    
    start = time.time()
    results = []
    for i in range(100):
        results.append(expensive_cached_dict(i % 10))
    dict_time = time.time() - start
    
    # 4. Redis Cache (network overhead)
    redis_cache = RedisCache()
    def expensive_cached_redis(x):
        cache_key = f"compute:{x}"
        result = redis_cache.get(cache_key)
        if result is not None:
            return result
        result = expensive_computation(x)
        redis_cache.set(cache_key, result)
        return result
    
    start = time.time()
    results = []
    for i in range(100):
        results.append(expensive_cached_redis(i % 10))
    redis_time = time.time() - start
    
    # Print results
    print("Performance Comparison (100 operations, 10 unique values):")
    print("="*60)
    print(f"No Cache:       {no_cache_time:.3f}s  (baseline)")
    print(f"LRU Cache:      {lru_time:.3f}s  ({no_cache_time/lru_time:.1f}x faster)")
    print(f"Dict Cache:     {dict_time:.3f}s  ({no_cache_time/dict_time:.1f}x faster)")
    print(f"Redis Cache:    {redis_time:.3f}s  ({no_cache_time/redis_time:.1f}x faster)")
    
    # Hit rates
    print(f"\nLRU Cache Info: {expensive_cached_lru.cache_info()}")
    print(f"Hit Rate: {expensive_cached_lru.cache_info().hits / 100 * 100:.1f}%")

# Run benchmark
benchmark_cache_performance()
```

**Expected Output:**
```
Performance Comparison (100 operations, 10 unique values):
============================================================
No Cache:       1.000s  (baseline)
LRU Cache:      0.110s  (9.1x faster)
Dict Cache:     0.110s  (9.1x faster)
Redis Cache:    0.150s  (6.7x faster)

LRU Cache Info: CacheInfo(hits=90, misses=10, maxsize=128, currsize=10)
Hit Rate: 90.0%
```

### Cache Size vs Performance

```python
def benchmark_cache_size():
    """Test impact of cache size on performance"""
    
    @lru_cache(maxsize=None)  # Unlimited
    def fib_unlimited(n):
        if n < 2:
            return n
        return fib_unlimited(n-1) + fib_unlimited(n-2)
    
    @lru_cache(maxsize=10)  # Small cache
    def fib_small(n):
        if n < 2:
            return n
        return fib_small(n-1) + fib_small(n-2)
    
    @lru_cache(maxsize=100)  # Medium cache
    def fib_medium(n):
        if n < 2:
            return n
        return fib_medium(n-1) + fib_medium(n-2)
    
    # Test with different sizes
    test_n = 30
    
    # Unlimited cache
    start = time.time()
    result = fib_unlimited(test_n)
    time_unlimited = time.time() - start
    
    # Small cache
    start = time.time()
    result = fib_small(test_n)
    time_small = time.time() - start
    
    # Medium cache
    start = time.time()
    result = fib_medium(test_n)
    time_medium = time.time() - start
    
    print(f"Fibonacci({test_n}):")
    print(f"Unlimited cache: {time_unlimited:.4f}s")
    print(f"Small cache (10): {time_small:.4f}s")
    print(f"Medium cache (100): {time_medium:.4f}s")
    
    print(f"\nCache Info:")
    print(f"Unlimited: {fib_unlimited.cache_info()}")
    print(f"Small:     {fib_small.cache_info()}")
    print(f"Medium:    {fib_medium.cache_info()}")
```

### Memory vs Speed Tradeoff

```python
def analyze_cache_tradeoff():
    """Analyze memory vs speed tradeoff"""
    
    import sys
    
    cache_sizes = [10, 50, 100, 500, 1000]
    results = []
    
    for size in cache_sizes:
        cache = LRUCache(capacity=size)
        
        # Fill cache
        for i in range(size):
            cache.set(f'key_{i}', {'data': 'x' * 1000})  # 1KB each
        
        # Measure memory
        memory_mb = sys.getsizeof(cache.cache) / 1024**2
        
        # Measure access time
        start = time.time()
        for _ in range(10000):
            cache.get(f'key_{size//2}')
        access_time = time.time() - start
        
        results.append({
            'size': size,
            'memory_mb': memory_mb,
            'access_time_ms': access_time * 1000
        })
    
    print("Cache Size vs Performance:")
    print("="*60)
    print(f"{'Size':<10} {'Memory (MB)':<15} {'Access Time (ms)':<20}")
    print("-"*60)
    for r in results:
        print(f"{r['size']:<10} {r['memory_mb']:<15.2f} {r['access_time_ms']:<20.4f}")
```

---

## Best Practices

### 1. Choose Right Cache Type

```python
"""
DECISION FLOWCHART:

Single Server?
    Yes → Local Memory Cache (LRU, dict)
    No  → Go to next question

Need Persistence?
    Yes → Disk Cache (diskcache, SQLite)
    No  → Memory Cache (Redis, Memcached)

Large Data (>100GB)?
    Yes → Distributed Cache (Redis Cluster, Hazelcast)
    No  → Single Redis Instance

Need Complex Data Structures?
    Yes → Redis (lists, sets, sorted sets)
    No  → Memcached (simpler, faster for basic KV)

Time-Sensitive Data?
    Yes → Short TTL Cache
    No  → Long TTL or Event-Based Invalidation
"""
```

### 2. Cache Key Design

```python
class CacheKeyBestPractices:
    """Best practices for cache key design"""
    
    @staticmethod
    def good_key_design():
        """Good cache key examples"""
        
        # 1. Include version in key
        key = f"user_profile:v2:{user_id}"
        
        # 2. Hierarchical namespacing
        key = f"app:production:user:profile:{user_id}"
        
        # 3. Include relevant parameters
        key = f"recommendations:{user_id}:{category}:{page}"
        
        # 4. Use consistent separators
        key = f"model:predictions:{model_version}:{input_hash}"
        
        # 5. Keep keys readable but not too long
        key = f"ml:features:v1:{user_id}"  # Good
        # key = f"machine_learning_features_version_1_user_{user_id}"  # Too long
    
    @staticmethod
    def bad_key_design():
        """Bad cache key examples"""
        
        # 1. No namespacing (key collisions!)
        key = f"{user_id}"  # BAD
        
        # 2. No version (can't invalidate easily)
        key = f"user_profile:{user_id}"  # BAD
        
        # 3. Too generic
        key = "data"  # BAD
        
        # 4. Inconsistent separators
        key = f"user.profile-{user_id}_v1"  # BAD
        
        # 5. Including timestamps (defeats caching!)
        key = f"user:{user_id}:{time.time()}"  # BAD

# Generate hash for complex parameters
def generate_cache_key(prefix, **kwargs):
    """Generate consistent cache key from parameters"""
    import json
    import hashlib
    
    # Sort parameters for consistency
    params_str = json.dumps(kwargs, sort_keys=True)
    params_hash = hashlib.md5(params_str.encode()).hexdigest()[:16]
    
    return f"{prefix}:{params_hash}"

# Usage
key = generate_cache_key('predictions', 
                         user_id=123, 
                         model='v2', 
                         features=[1,2,3])
```

### 3. Handle Cache Failures

```python
class ResilientCache:
    """Cache with fallback on failures"""
    
    def __init__(self, cache_backend):
        self.cache = cache_backend
        self.failure_count = 0
        self.max_failures = 3
    
    def get(self, key):
        """Get with error handling"""
        try:
            return self.cache.get(key)
        except Exception as e:
            self.failure_count += 1
            print(f"Cache get failed: {e}")
            
            # Disable cache if too many failures
            if self.failure_count > self.max_failures:
                print("Cache disabled due to failures")
                return None
            
            return None
    
    def set(self, key, value, ttl=3600):
        """Set with error handling"""
        try:
            self.cache.set(key, value, ttl=ttl)
            # Reset failure count on success
            self.failure_count = 0
        except Exception as e:
            self.failure_count += 1
            print(f"Cache set failed: {e}")
            
            # Don't fail the operation, just skip caching
            pass

# Usage in application
def get_data_with_fallback(key):
    """Resilient data fetching"""
    
    # Try cache
    try:
        cached = cache.get(key)
        if cached:
            return cached
    except Exception:
        # Cache failed, continue to source
        pass
    
    # Fetch from source
    data = fetch_from_source(key)
    
    # Try to cache (don't fail if caching fails)
    try:
        cache.set(key, data)
    except Exception:
        # Log but don't fail
        pass
    
    return data
```

### 4. Monitor Cache Performance

```python
class CacheMonitoring:
    """Monitor cache hit rates and performance"""
    
    def __init__(self, cache):
        self.cache = cache
        self.hits = 0
        self.misses = 0
        self.errors = 0
        self.total_get_time = 0
        self.total_set_time = 0
    
    def get(self, key):
        """Get with monitoring"""
        start = time.time()
        try:
            value = self.cache.get(key)
            self.total_get_time += time.time() - start
            
            if value is not None:
                self.hits += 1
            else:
                self.misses += 1
            
            return value
        except Exception as e:
            self.errors += 1
            raise
    
    def set(self, key, value, ttl=3600):
        """Set with monitoring"""
        start = time.time()
        try:
            self.cache.set(key, value, ttl=ttl)
            self.total_set_time += time.time() - start
        except Exception as e:
            self.errors += 1
            raise
    
    def get_stats(self):
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests * 100 if total_requests > 0 else 0
        avg_get_time = self.total_get_time / total_requests if total_requests > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total_requests': total_requests,
            'hit_rate_percent': hit_rate,
            'avg_get_time_ms': avg_get_time * 1000,
            'errors': self.errors
        }
    
    def print_stats(self):
        """Print cache statistics"""
        stats = self.get_stats()
        print("Cache Statistics:")
        print("="*50)
        print(f"Total Requests: {stats['total_requests']}")
        print(f"Hits:           {stats['hits']}")
        print(f"Misses:         {stats['misses']}")
        print(f"Hit Rate:       {stats['hit_rate_percent']:.2f}%")
        print(f"Avg Get Time:   {stats['avg_get_time_ms']:.3f} ms")
        print(f"Errors:         {stats['errors']}")

# Usage
monitored_cache = CacheMonitoring(RedisCache())

# Use cache
for i in range(1000):
    key = f"user_{i % 100}"  # Repeat pattern
    value = monitored_cache.get(key)
    if value is None:
        value = fetch_data(key)
        monitored_cache.set(key, value)

# Print statistics
monitored_cache.print_stats()
```

### 5. Cache Warming

```python
class CacheWarmer:
    """Pre-populate cache with frequently accessed data"""
    
    def __init__(self, cache):
        self.cache = cache
    
    def warm_up(self, data_loader_func, keys, ttl=3600):
        """Warm up cache with data"""
        print(f"Warming up cache for {len(keys)} keys...")
        
        for i, key in enumerate(keys):
            if i % 100 == 0:
                print(f"Progress: {i}/{len(keys)}")
            
            # Check if already cached
            if self.cache.get(key) is not None:
                continue
            
            # Load data
            data = data_loader_func(key)
            
            # Cache it
            self.cache.set(key, data, ttl=ttl)
        
        print("Cache warm-up complete!")
    
    def warm_up_batch(self, batch_loader_func, keys, batch_size=100, ttl=3600):
        """Warm up cache in batches (more efficient)"""
        print(f"Batch warming up cache for {len(keys)} keys...")
        
        for i in range(0, len(keys), batch_size):
            batch_keys = keys[i:i+batch_size]
            
            # Check which keys need loading
            missing_keys = []
            for key in batch_keys:
                if self.cache.get(key) is None:
                    missing_keys.append(key)
            
            if not missing_keys:
                continue
            
            # Load batch
            batch_data = batch_loader_func(missing_keys)
            
            # Cache batch
            cache_data = {k: v for k, v in zip(missing_keys, batch_data)}
            self.cache.set_many(cache_data, ttl=ttl)
            
            print(f"Loaded batch {i//batch_size + 1}")
        
        print("Batch warm-up complete!")

# Usage
warmer = CacheWarmer(RedisCache())

# Warm up on application startup
def load_user_data(user_id):
    return db.query(f"SELECT * FROM users WHERE id={user_id}")

# Get popular users
popular_user_ids = [1, 2, 3, 4, 5]  # ... top 1000 users

# Warm cache
warmer.warm_up(load_user_data, popular_user_ids)

# Now cache is pre-populated for popular users
```

### 6. Cache Stampede Prevention

```python
import threading

class StampedePreventionCache:
    """Prevent cache stampede (thundering herd)"""
    
    def __init__(self, cache):
        self.cache = cache
        self.locks = {}
        self.lock_lock = threading.Lock()
    
    def get_lock(self, key):
        """Get lock for specific key"""
        with self.lock_lock:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
            return self.locks[key]
    
    def get_or_compute(self, key, compute_func, ttl=3600):
        """Get from cache or compute (with stampede prevention)"""
        
        # Try cache
        value = self.cache.get(key)
        if value is not None:
            return value
        
        # Cache miss - acquire lock for this key
        lock = self.get_lock(key)
        
        with lock:
            # Double-check cache (another thread may have computed)
            value = self.cache.get(key)
            if value is not None:
                return value
            
            # Compute value (only one thread does this)
            print(f"Computing value for {key}")
            value = compute_func()
            
            # Cache it
            self.cache.set(key, value, ttl=ttl)
            
            return value

# Usage
stampede_cache = StampedePreventionCache(RedisCache())

def expensive_computation():
    """Expensive operation"""
    time.sleep(2)
    return "result"

# Multiple threads request same key
from concurrent.futures import ThreadPoolExecutor

def request_data():
    return stampede_cache.get_or_compute('expensive_key', expensive_computation)

# 10 concurrent requests, but computation happens only once!
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(lambda _: request_data(), range(10)))

# Only prints "Computing value for expensive_key" once
```

---

## Interview Questions

### Question 1: Cache vs Database

**Q: When would you use caching vs querying the database directly?**

**A:**

**Use Caching When:**
1. **Read-heavy workload** (>80% reads)
2. **Data doesn't change often** (user profiles, product catalog)
3. **Query is expensive** (complex joins, aggregations)
4. **High traffic** (thousands of requests/second)
5. **Latency matters** (real-time applications)
6. **Same data requested repeatedly** (hot data)

**Use Database When:**
1. **Write-heavy workload** (lots of updates)
2. **Data changes frequently** (real-time inventory)
3. **Need consistency** (financial transactions)
4. **Complex queries** (dynamic filters, sorting)
5. **Low traffic** (admin panels)
6. **Data rarely repeated** (unique queries)

**Example:**

```python
# E-commerce product page

# ❌ BAD: Query DB for every page view
def get_product_page(product_id):
    product = db.query(f"SELECT * FROM products WHERE id={product_id}")
    reviews = db.query(f"SELECT * FROM reviews WHERE product_id={product_id}")
    recommendations = db.query(f"...")  # Complex query
    return render_page(product, reviews, recommendations)

# ✅ GOOD: Cache product data
def get_product_page_cached(product_id):
    cache_key = f"product_page:{product_id}"
    
    # Try cache (1-5ms)
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Cache miss - query database (50-200ms)
    product = db.query(f"SELECT * FROM products WHERE id={product_id}")
    reviews = db.query(f"SELECT * FROM reviews WHERE product_id={product_id}")
    recommendations = compute_recommendations(product_id)
    
    page_data = render_page(product, reviews, recommendations)
    
    # Cache for 1 hour
    cache.set(cache_key, page_data, ttl=3600)
    
    return page_data

# Result: 10-50x faster, reduced DB load
```

**Metrics to Consider:**
- **Database**: 50-200ms query time, 1000 concurrent connections limit
- **Cache**: 1-5ms access time, handles 100,000+ req/sec

---

### Question 2: Cache Eviction Policy Choice

**Q: How would you choose between LRU, LFU, and FIFO for an ML inference service?**

**A:**

**Scenario: ML Model Inference Service**
- 10 models deployed
- Models vary in size (100MB - 2GB)
- Access pattern: Some models very popular, others rarely used
- Memory limit: 10GB

**Analysis:**

**FIFO (First In First Out):**
❌ Not suitable
- Doesn't consider access patterns
- May evict frequently used models
- Popular model could be evicted just because it was loaded first

**LRU (Least Recently Used):**
✅ Good choice
- Keeps recently used models in memory
- If model accessed recently, likely to be accessed again (temporal locality)
- Simple and effective
- Good for stable access patterns

**LFU (Least Frequently Used):**
✅ Best choice for this scenario
- Keeps most popular models in memory
- Protects frequently used models from eviction
- Better for skewed access distribution (80/20 rule)
- Some models may be used 1000x more than others

**Implementation:**

```python
class ModelCacheLFU:
    def __init__(self, max_memory_gb=10):
        self.max_memory_gb = max_memory_gb
        self.models = {}  # model_name -> (model, size_gb, frequency)
        self.total_memory_gb = 0
    
    def load_model(self, model_name):
        """Load model with LFU caching"""
        
        # Check if in cache
        if model_name in self.models:
            model, size_gb, freq = self.models[model_name]
            # Increment frequency
            self.models[model_name] = (model, size_gb, freq + 1)
            print(f"Model {model_name} loaded from cache (freq={freq+1})")
            return model
        
        # Load model from disk
        print(f"Loading model {model_name} from disk...")
        model, size_gb = load_model_from_disk(model_name)
        
        # Evict if needed
        while self.total_memory_gb + size_gb > self.max_memory_gb:
            self._evict_lfu()
        
        # Add to cache
        self.models[model_name] = (model, size_gb, 1)
        self.total_memory_gb += size_gb
        
        return model
    
    def _evict_lfu(self):
        """Evict least frequently used model"""
        if not self.models:
            return
        
        # Find model with lowest frequency
        lfu_model = min(self.models.items(), key=lambda x: x[1][2])
        model_name = lfu_model[0]
        size_gb = lfu_model[1][1]
        freq = lfu_model[1][2]
        
        print(f"Evicting {model_name} (freq={freq}, size={size_gb}GB)")
        del self.models[model_name]
        self.total_memory_gb -= size_gb

# Usage
model_cache = ModelCacheLFU(max_memory_gb=10)

# Simulate requests (zipf distribution - 80/20 rule)
# Popular models: model_1, model_2 (accessed frequently)
# Rare models: model_8, model_9, model_10 (accessed rarely)

for i in range(100):
    if i < 60:
        model = model_cache.load_model('model_1')  # Popular
    elif i < 80:
        model = model_cache.load_model('model_2')  # Popular
    else:
        model = model_cache.load_model(f'model_{i % 10}')  # Rare

# Result: Popular models stay in cache, rare models evicted
```

**Recommendation: Use LFU for ML inference with skewed access patterns**

---

### Question 3: Handling Stale Cache

**Q: How do you prevent serving stale data from cache in a recommendation system?**

**A:**

**Problem:**
- Recommendations based on user behavior
- User behavior changes (new purchases, clicks)
- Cache may serve outdated recommendations

**Solutions:**

**1. TTL (Time-Based Expiration):**

```python
# Short TTL for real-time data
cache.set(f'recommendations:{user_id}', recs, ttl=300)  # 5 minutes

# Pros: Simple, prevents very stale data
# Cons: May evict useful data, doesn't reflect actual changes
```

**2. Event-Based Invalidation:**

```python
def on_user_action(user_id, action):
    """Invalidate cache when user takes action"""
    
    # User made purchase
    if action == 'purchase':
        cache.delete(f'recommendations:{user_id}')
        cache.delete(f'cart_recommendations:{user_id}')
    
    # User clicked item
    elif action == 'click':
        cache.delete(f'recommendations:{user_id}')
    
    # User updated profile
    elif action == 'profile_update':
        cache.delete(f'recommendations:{user_id}')
        cache.delete(f'user_features:{user_id}')

# Pros: Always fresh, efficient
# Cons: Need to track all events, complex
```

**3. Versioned Cache:**

```python
class VersionedRecommendationCache:
    def __init__(self, cache):
        self.cache = cache
        self.user_versions = {}  # user_id -> version
    
    def get_recommendations(self, user_id):
        """Get recommendations with version"""
        version = self.user_versions.get(user_id, 0)
        cache_key = f'recs:{user_id}:v{version}'
        
        recs = self.cache.get(cache_key)
        if recs:
            return recs
        
        # Compute recommendations
        recs = compute_recommendations(user_id)
        self.cache.set(cache_key, recs, ttl=3600)
        return recs
    
    def on_user_action(self, user_id, action):
        """Bump version on user action"""
        current_version = self.user_versions.get(user_id, 0)
        self.user_versions[user_id] = current_version + 1
        print(f"User {user_id} version bumped to {current_version + 1}")

# Pros: No explicit invalidation, easy rollback
# Cons: Old versions waste space
```

**4. Hybrid Approach (Best):**

```python
class SmartRecommendationCache:
    def __init__(self, cache):
        self.cache = cache
    
    def get_recommendations(self, user_id):
        """Get recommendations with smart caching"""
        cache_key = f'recs:{user_id}'
        
        # Try cache
        cached_data = self.cache.get(cache_key)
        if cached_data:
            recs, last_action_time = cached_data
            
            # Check if user had recent actions
            recent_action_time = self.get_last_action_time(user_id)
            
            if recent_action_time <= last_action_time:
                # No new actions, cache is fresh
                return recs
            else:
                # User had new action, recompute
                print(f"Cache invalidated: new user action")
        
        # Compute recommendations
        recs = compute_recommendations(user_id)
        last_action_time = self.get_last_action_time(user_id)
        
        # Cache with metadata
        self.cache.set(cache_key, (recs, last_action_time), ttl=1800)
        return recs
    
    def get_last_action_time(self, user_id):
        """Get timestamp of user's last action"""
        return db.query(f"SELECT MAX(timestamp) FROM user_actions WHERE user_id={user_id}")

# Pros: Balance between freshness and performance
# Cons: Need to track action timestamps
```

**Recommendation:**
Use **hybrid approach** with:
- TTL of 30 minutes (prevent very stale data)
- Event-based invalidation for critical actions (purchases)
- Version tracking for easy debugging

---

### Question 4: Cache Warming Strategy

**Q: How would you warm up cache for a new ML model deployment?**

**A:**

**Scenario:**
- New recommendation model deployed
- 1 million active users
- Cold start: 0% cache hit rate
- Need to avoid DB overload

**Strategy:**

**1. Prioritized Warming:**

```python
class PrioritizedCacheWarmer:
    def __init__(self, cache, db):
        self.cache = cache
        self.db = db
    
    def warm_up_prioritized(self, model_version):
        """Warm up cache with prioritization"""
        
        # Priority 1: VIP users (1000 users) - warm immediately
        print("Warming VIP users...")
        vip_users = self.db.query("SELECT user_id FROM users WHERE is_vip=1 LIMIT 1000")
        self._warm_batch(vip_users, model_version, priority='high')
        
        # Priority 2: Active users (100,000 users) - warm gradually
        print("Warming active users...")
        active_users = self.db.query("""
            SELECT user_id FROM users 
            WHERE last_active > NOW() - INTERVAL 7 DAY
            LIMIT 100000
        """)
        self._warm_batch(active_users, model_version, priority='medium')
        
        # Priority 3: All users - lazy loading (warm on first request)
        print("Active users warmed. Others will be lazy-loaded.")
    
    def _warm_batch(self, user_ids, model_version, priority='medium'):
        """Warm up batch of users"""
        batch_size = 100 if priority == 'high' else 500
        rate_limit = 10 if priority == 'high' else 100  # requests per second
        
        for i in range(0, len(user_ids), batch_size):
            batch = user_ids[i:i+batch_size]
            
            # Compute recommendations
            recommendations = self.compute_batch_recommendations(batch, model_version)
            
            # Cache batch
            for user_id, recs in zip(batch, recommendations):
                cache_key = f'recs:{model_version}:{user_id}'
                self.cache.set(cache_key, recs, ttl=3600)
            
            # Rate limiting
            time.sleep(batch_size / rate_limit)
            
            if i % 10000 == 0:
                print(f"Warmed {i}/{len(user_ids)} users")
    
    def compute_batch_recommendations(self, user_ids, model_version):
        """Compute recommendations in batch (efficient)"""
        # Batch feature extraction
        features = self.db.query_batch(user_ids)
        
        # Batch prediction
        model = load_model(model_version)
        predictions = model.predict_batch(features)
        
        return predictions

# Usage
warmer = PrioritizedCacheWarmer(cache, db)

# On model deployment
warmer.warm_up_prioritized('v2.0')
```

**2. Progressive Warming:**

```python
def progressive_warm_up(cache, model_version, duration_minutes=60):
    """Warm up cache progressively over time"""
    
    # Get all users
    total_users = db.query("SELECT COUNT(*) FROM users")[0]
    users_per_minute = total_users // duration_minutes
    
    print(f"Progressive warm-up: {users_per_minute} users/minute for {duration_minutes} minutes")
    
    offset = 0
    for minute in range(duration_minutes):
        # Get batch of users
        users = db.query(f"SELECT user_id FROM users LIMIT {users_per_minute} OFFSET {offset}")
        
        # Compute and cache
        for user_id in users:
            recs = compute_recommendations(user_id, model_version)
            cache.set(f'recs:{model_version}:{user_id}', recs, ttl=7200)
        
        offset += users_per_minute
        print(f"Minute {minute+1}/{duration_minutes}: Warmed {offset}/{total_users} users")
        
        time.sleep(60)  # Wait 1 minute
    
    print("Progressive warm-up complete!")

# Usage: Start as background task after deployment
import threading
thread = threading.Thread(target=progressive_warm_up, args=(cache, 'v2.0', 60))
thread.daemon = True
thread.start()
```

**3. Hybrid: Instant + Background:**

```python
# On deployment:

# 1. Instant: Warm critical users (5 minutes)
warm_critical_users(cache, model_version='v2.0')

# 2. Switch traffic to new model
route_traffic_to_model('v2.0')

# 3. Background: Warm remaining users (1 hour)
start_background_warming(cache, model_version='v2.0')

# 4. Monitor cache hit rate
# Target: 60% hit rate within 10 minutes
#         80% hit rate within 30 minutes
#         95% hit rate within 1 hour
```

**Best Practice:**
- **Instant warm**: VIP users, recent active users
- **Progressive**: All users over 30-60 minutes
- **Monitor**: Track cache hit rate, adjust strategy
- **Rate limit**: Don't overload DB/model

---

### Question 5: Distributed Cache Consistency

**Q: How do you maintain cache consistency across multiple servers in a microservices architecture?**

**A:**

**Problem:**
- Multiple services
- Each service has local cache
- Data updates in one service
- Other services have stale cache

**Solutions:**

**1. Centralized Cache (Redis):**

```python
# All services use shared Redis cache
# ✅ Pros: Single source of truth, always consistent
# ❌ Cons: Network latency, single point of failure

class CentralizedCache:
    def __init__(self):
        self.redis = redis.Redis(host='cache-cluster.example.com')
    
    def get(self, key):
        return self.redis.get(key)
    
    def set(self, key, value, ttl=3600):
        self.redis.setex(key, ttl, value)
    
    def delete(self, key):
        self.redis.delete(key)

# Service A
cache = CentralizedCache()
user = cache.get('user:123')

# Service B (same cache)
cache = CentralizedCache()
user = cache.get('user:123')  # Always consistent
```

**2. Cache Invalidation via Messaging:**

```python
# Use message queue to broadcast invalidations

import pika  # RabbitMQ

class DistributedCacheWithMessaging:
    def __init__(self):
        self.local_cache = {}
        self.redis = redis.Redis()
        
        # Subscribe to invalidation messages
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('mq.example.com'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='cache_invalidations')
        self.channel.basic_consume(
            queue='cache_invalidations',
            on_message_callback=self._on_invalidation,
            auto_ack=True
        )
        
        # Start listening in background
        threading.Thread(target=self.channel.start_consuming, daemon=True).start()
    
    def get(self, key):
        """Get with two-level cache (local + Redis)"""
        # Try local cache first (fast)
        if key in self.local_cache:
            return self.local_cache[key]
        
        # Try Redis (medium)
        value = self.redis.get(key)
        if value:
            self.local_cache[key] = value
            return value
        
        return None
    
    def set(self, key, value, ttl=3600):
        """Set and broadcast invalidation"""
        # Update Redis
        self.redis.setex(key, ttl, value)
        
        # Update local cache
        self.local_cache[key] = value
        
        # Broadcast invalidation to other services
        self._broadcast_invalidation(key)
    
    def delete(self, key):
        """Delete and broadcast invalidation"""
        # Delete from Redis
        self.redis.delete(key)
        
        # Delete from local cache
        if key in self.local_cache:
            del self.local_cache[key]
        
        # Broadcast invalidation
        self._broadcast_invalidation(key)
    
    def _broadcast_invalidation(self, key):
        """Broadcast invalidation to all services"""
        message = json.dumps({'action': 'invalidate', 'key': key})
        self.channel.basic_publish(
            exchange='',
            routing_key='cache_invalidations',
            body=message
        )
    
    def _on_invalidation(self, ch, method, properties, body):
        """Handle invalidation message"""
        message = json.loads(body)
        key = message['key']
        
        # Invalidate local cache
        if key in self.local_cache:
            del self.local_cache[key]
            print(f"Invalidated local cache for {key}")

# ✅ Pros: Fast local cache + eventual consistency
# ❌ Cons: Message delay, complexity
```

**3. Cache Versioning:**

```python
class VersionedDistributedCache:
    def __init__(self):
        self.redis = redis.Redis()
        self.version_key = 'cache_version'
        self.local_cache = {}
        self.local_version = self._get_version()
    
    def _get_version(self):
        """Get current cache version"""
        version = self.redis.get(self.version_key)
        return int(version) if version else 0
    
    def get(self, key):
        """Get with version check"""
        # Check if local cache is stale
        current_version = self._get_version()
        if current_version != self.local_version:
            # Version changed, clear local cache
            self.local_cache.clear()
            self.local_version = current_version
            print("Local cache invalidated due to version change")
        
        # Try local cache
        if key in self.local_cache:
            return self.local_cache[key]
        
        # Try Redis
        value = self.redis.get(key)
        if value:
            self.local_cache[key] = value
        
        return value
    
    def set(self, key, value, ttl=3600):
        """Set value"""
        self.redis.setex(key, ttl, value)
        self.local_cache[key] = value
    
    def invalidate_all(self):
        """Invalidate all caches (increment version)"""
        self.redis.incr(self.version_key)
        print(f"Cache version incremented to {self._get_version()}")

# ✅ Pros: Simple, effective for global invalidation
# ❌ Cons: Invalidates entire cache, not granular
```

**Best Practice for Microservices:**

```python
"""
RECOMMENDED ARCHITECTURE:

1. Shared Redis Cluster (L1 Cache)
   - Central source of truth
   - Fast access (1-5ms)
   - Consistent across services

2. Optional Local Cache (L2 Cache)
   - For very hot data
   - Very fast (microseconds)
   - Short TTL (30-60 seconds)
   - With invalidation messaging

3. Strategy:
   - Critical data: Only use Redis (always consistent)
   - Hot read data: Local cache + Redis (faster, eventual consistency OK)
   - Write-heavy data: Skip cache, write to DB directly
"""

class TwoLevelCache:
    def __init__(self, enable_local=False):
        self.redis = redis.Redis(host='redis-cluster')
        self.enable_local = enable_local
        self.local = LRUCache(maxsize=1000) if enable_local else None
        self.local_ttl = 60  # 1 minute local cache
    
    def get(self, key, consistency='eventual'):
        """
        Get with consistency control
        
        consistency: 'strong' (skip local) or 'eventual' (use local)
        """
        if consistency == 'strong' or not self.enable_local:
            # Skip local cache for strong consistency
            return self.redis.get(key)
        
        # Try local cache
        if self.local:
            local_value = self.local.get(key)
            if local_value:
                return local_value
        
        # Try Redis
        value = self.redis.get(key)
        
        # Populate local cache
        if value and self.local:
            self.local.set(key, value)
        
        return value
    
    def set(self, key, value, ttl=3600):
        """Set in both caches"""
        self.redis.setex(key, ttl, value)
        if self.local:
            self.local.set(key, value)
```

**Decision Matrix:**

| Data Type | Consistency Need | Strategy |
|-----------|-----------------|----------|
| User profile | Strong | Redis only |
| Product catalog | Eventual | Local + Redis |
| Recommendations | Eventual | Local + Redis |
| Financial data | Strong | Redis only |
| Analytics | Eventual | Local + Redis |
| Session data | Strong | Redis only |

---

## Summary

### Key Takeaways

**1. Cache Types:**
- **Memory**: Fastest (Redis, Memcached, local dict)
- **Disk**: Persistent (SQLite, diskcache, joblib)
- **Distributed**: Scalable (Redis Cluster, Hazelcast)

**2. Eviction Policies:**
- **LRU**: General purpose, good for temporal locality
- **LFU**: Best for skewed access patterns (80/20 rule)
- **TTL**: Prevents stale data, simple

**3. Invalidation:**
- **Time-based**: Simple but may serve stale data
- **Event-based**: Always fresh but complex
- **Versioned**: Easy global invalidation

**4. ML-Specific:**
- **Model caching**: Load once, reuse (2-5 second savings)
- **Feature caching**: Avoid recomputation
- **Prediction caching**: Cache similar inputs

**5. Best Practices:**
- Choose right cache type for use case
- Monitor hit rates (target: >80%)
- Handle cache failures gracefully
- Warm up cache on deployment
- Use appropriate TTLs

**6. Trade-offs:**
- **Memory vs Persistence**: Fast vs survives restart
- **Local vs Distributed**: Speed vs scalability
- **Consistency vs Performance**: Strong vs eventual
- **Simple vs Complex**: Easy to maintain vs optimized

### Decision Flowchart

```
Need Caching?
│
├─ Single Server?
│  ├─ Yes → Local Memory (LRU, dict)
│  └─ No → Distributed Cache (Redis, Memcached)
│
├─ Need Persistence?
│  ├─ Yes → Disk Cache (SQLite, diskcache)
│  └─ No → Memory Cache
│
├─ Data Size?
│  ├─ Small (<1GB) → Memory Cache
│  ├─ Medium (1-100GB) → Redis
│  └─ Large (>100GB) → Redis Cluster
│
└─ Consistency Need?
   ├─ Strong → Centralized Cache only
   └─ Eventual → Local + Distributed
```

---

**End of Caching Strategies Guide** 🚀

**Key Numbers to Remember:**
- Memory cache: ~1ms access time
- Redis: ~1-5ms access time
- Disk cache: ~10-100ms access time
- Database: ~50-200ms query time
- Target hit rate: >80%
- Typical cache size: 10-30% of data
- TTL: 5-60 minutes for hot data, 1-24 hours for cold data

Good luck optimizing your ML/AI systems with caching! 💾⚡