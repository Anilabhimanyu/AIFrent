# Data Management for ML/Data Science Engineers - Complete Guide

> **Comprehensive reference for data types, storage, calculations, costs, and optimization strategies for ML/DS engineering**

---

## Table of Contents

1. [Data Types and Storage](#data-types-and-storage)
2. [Data Size Calculations](#data-size-calculations)
3. [Storage Costs and Optimization](#storage-costs-and-optimization)
4. [Data Types in Programming](#data-types-in-programming)
5. [Database Storage Considerations](#database-storage-considerations)
6. [Cloud Storage Costs](#cloud-storage-costs)
7. [Data Compression Techniques](#data-compression-techniques)
8. [Real-World Cost Examples](#real-world-cost-examples)
9. [Data Optimization Strategies](#data-optimization-strategies)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## Data Types and Storage

### Fundamental Data Units

```
BIT (b) = Binary Digit (0 or 1)

BYTE (B) = 8 bits

Storage Hierarchy:
1 Byte (B)        = 8 bits
1 Kilobyte (KB)   = 1,024 Bytes        = 2^10 Bytes
1 Megabyte (MB)   = 1,024 KB           = 2^20 Bytes = 1,048,576 Bytes
1 Gigabyte (GB)   = 1,024 MB           = 2^30 Bytes
1 Terabyte (TB)   = 1,024 GB           = 2^40 Bytes
1 Petabyte (PB)   = 1,024 TB           = 2^50 Bytes
1 Exabyte (EB)    = 1,024 PB           = 2^60 Bytes

Note: Marketing often uses 1000 instead of 1024 (decimal vs binary)
```

### Numeric Data Types - Storage Size

| Data Type | Size | Range | Use Case |
|-----------|------|-------|----------|
| **int8** | 1 byte | -128 to 127 | Small integers, flags |
| **uint8** | 1 byte | 0 to 255 | Pixel values, small counts |
| **int16** | 2 bytes | -32,768 to 32,767 | Medium integers |
| **int32** | 4 bytes | -2.1B to 2.1B | Default integer |
| **int64** | 8 bytes | -9.2E18 to 9.2E18 | Large integers, IDs |
| **float16** | 2 bytes | ±65,504 (low precision) | Deep learning weights |
| **float32** | 4 bytes | ±3.4E38 (7 digits) | Scientific computing |
| **float64** | 8 bytes | ±1.7E308 (15 digits) | Default Python float |
| **bool** | 1 byte | True/False | Boolean flags |

### Example: Memory Impact

```python
import numpy as np
import pandas as pd

# Create 1 million integers
n = 1_000_000

# Different data types
data_int64 = np.arange(n, dtype=np.int64)
data_int32 = np.arange(n, dtype=np.int32)
data_int16 = np.arange(n, dtype=np.int16)
data_int8 = np.arange(n, dtype=np.int8)

print("Memory Usage for 1 Million Integers:")
print(f"int64:  {data_int64.nbytes / 1024**2:.2f} MB")  # 7.63 MB
print(f"int32:  {data_int32.nbytes / 1024**2:.2f} MB")  # 3.81 MB
print(f"int16:  {data_int16.nbytes / 1024**2:.2f} MB")  # 1.91 MB
print(f"int8:   {data_int8.nbytes / 1024**2:.2f} MB")   # 0.95 MB

# Savings
print(f"\nUsing int32 instead of int64 saves: 50% memory")
print(f"Using int8 instead of int64 saves: 87.5% memory")
```

**Output:**
```
Memory Usage for 1 Million Integers:
int64:  7.63 MB
int32:  3.81 MB
int16:  1.91 MB
int8:   0.95 MB

Using int32 instead of int64 saves: 50% memory
Using int8 instead of int64 saves: 87.5% memory
```

---

## Data Size Calculations

### Python Objects Size

```python
import sys

# Basic types
print("Basic Python Objects:")
print(f"int:        {sys.getsizeof(42)} bytes")           # 28 bytes
print(f"float:      {sys.getsizeof(3.14)} bytes")         # 24 bytes
print(f"bool:       {sys.getsizeof(True)} bytes")         # 28 bytes
print(f"string:     {sys.getsizeof('hello')} bytes")      # 54 bytes
print(f"empty list: {sys.getsizeof([])} bytes")           # 56 bytes
print(f"empty dict: {sys.getsizeof({})} bytes")           # 64 bytes

# String size grows with content
strings = ['a', 'hello', 'hello world' * 10]
for s in strings:
    print(f"'{s[:20]}...': {sys.getsizeof(s)} bytes")
```

**Key Insight:** Python objects have overhead!
- Simple integer: 28 bytes (not 8!)
- This matters at scale

### Pandas DataFrame Memory

```python
import pandas as pd
import numpy as np

# Create sample DataFrame
df = pd.DataFrame({
    'id': range(1_000_000),                    # int64
    'value': np.random.randn(1_000_000),       # float64
    'category': ['A', 'B', 'C'] * 333334,      # object (string)
    'flag': np.random.choice([True, False], 1_000_000)  # bool
})

print("DataFrame Memory Usage:")
print(df.memory_usage(deep=True))
print(f"\nTotal: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Optimize
df_optimized = df.copy()
df_optimized['id'] = df_optimized['id'].astype('int32')
df_optimized['category'] = df_optimized['category'].astype('category')
df_optimized['flag'] = df_optimized['flag'].astype('bool')

print("\nOptimized DataFrame Memory Usage:")
print(df_optimized.memory_usage(deep=True))
print(f"\nTotal: {df_optimized.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

reduction = (1 - df_optimized.memory_usage(deep=True).sum() / df.memory_usage(deep=True).sum()) * 100
print(f"\nMemory Reduction: {reduction:.1f}%")
```

### Memory Profiling Function

```python
def memory_usage_by_dtype(df):
    """Analyze memory usage by data type"""
    memory_by_dtype = df.memory_usage(deep=True).sum()
    
    dtypes = {}
    for dtype in df.dtypes.unique():
        cols = df.select_dtypes(include=[dtype]).columns
        memory = df[cols].memory_usage(deep=True).sum()
        dtypes[str(dtype)] = {
            'columns': len(cols),
            'memory_mb': memory / 1024**2,
            'percentage': memory / memory_by_dtype * 100
        }
    
    return pd.DataFrame(dtypes).T.sort_values('memory_mb', ascending=False)

# Usage
print(memory_usage_by_dtype(df))
```

### Calculate Dataset Size

```python
def calculate_dataset_size(rows, columns_config):
    """
    Calculate dataset size
    
    columns_config: dict mapping column name to (dtype, bytes_per_value)
    """
    total_bytes = 0
    
    for col, (dtype, bytes_per_val) in columns_config.items():
        total_bytes += rows * bytes_per_val
    
    # Convert to readable format
    size_kb = total_bytes / 1024
    size_mb = size_kb / 1024
    size_gb = size_mb / 1024
    
    return {
        'rows': rows,
        'columns': len(columns_config),
        'total_bytes': total_bytes,
        'size_kb': size_kb,
        'size_mb': size_mb,
        'size_gb': size_gb
    }

# Example: E-commerce dataset
config = {
    'user_id': ('int64', 8),
    'product_id': ('int64', 8),
    'price': ('float64', 8),
    'quantity': ('int32', 4),
    'timestamp': ('datetime64', 8),
    'category': ('object', 50),  # Average string length
    'is_premium': ('bool', 1)
}

# Calculate for different scales
for scale in [1_000, 10_000, 100_000, 1_000_000, 10_000_000]:
    result = calculate_dataset_size(scale, config)
    print(f"\n{scale:,} rows:")
    print(f"  Size: {result['size_mb']:.2f} MB ({result['size_gb']:.4f} GB)")
```

---

## Storage Costs and Optimization

### The "Small Data" Problem

**What Seems Small But Costs More:**

#### 1. Repetitive Small Files

```python
# Scenario: Storing user events
# BAD: 1 file per event

# 1 million users, 100 events per day
# = 100 million files per day

# File system overhead:
# - Each file: ~4KB minimum (file system block size)
# - Even if data is 10 bytes

# Calculation:
events_per_day = 100_000_000
data_per_event = 10  # bytes
block_size = 4096    # bytes (4KB)

actual_data = events_per_day * data_per_event / 1024**2
storage_used = events_per_day * block_size / 1024**2

print(f"Actual data: {actual_data:.2f} MB")
print(f"Storage used: {storage_used:.2f} MB")
print(f"Waste: {(storage_used - actual_data) / actual_data * 100:.1f}% overhead")

# Output:
# Actual data: 953.67 MB
# Storage used: 390625.00 MB (381 GB!)
# Waste: 40857.6% overhead
```

**Solution: Batch/Aggregate**
```python
# GOOD: Store in batches

# Group events by hour or user
# Result: ~24 files per day instead of 100M
# Compression: 50-90% size reduction
```

#### 2. Uncompressed Text Data

```python
import gzip
import json

# Example: JSON logs
data = {
    'timestamp': '2026-01-23T10:30:00',
    'user_id': 12345,
    'action': 'click',
    'page': '/products/12345',
    'session': 'abc123xyz789'
}

# Uncompressed
json_str = json.dumps(data)
uncompressed_size = len(json_str.encode('utf-8'))

# Compressed
compressed = gzip.compress(json_str.encode('utf-8'))
compressed_size = len(compressed)

print(f"Uncompressed: {uncompressed_size} bytes")
print(f"Compressed:   {compressed_size} bytes")
print(f"Savings:      {(1 - compressed_size/uncompressed_size)*100:.1f}%")

# For 1 million records
print(f"\n1M records:")
print(f"Uncompressed: {uncompressed_size * 1_000_000 / 1024**2:.2f} MB")
print(f"Compressed:   {compressed_size * 1_000_000 / 1024**2:.2f} MB")
```

#### 3. Storing Redundant Data

```python
# BAD: Storing full address in each row
df_bad = pd.DataFrame({
    'user_id': [1, 1, 1, 2, 2, 2],
    'purchase_date': ['2026-01-01', '2026-01-15', '2026-02-01',
                      '2026-01-10', '2026-01-20', '2026-02-05'],
    'user_name': ['John Doe', 'John Doe', 'John Doe',
                  'Jane Smith', 'Jane Smith', 'Jane Smith'],
    'user_email': ['john@example.com'] * 3 + ['jane@example.com'] * 3,
    'user_address': ['123 Main St, City, State'] * 3 + 
                    ['456 Oak Ave, Town, State'] * 3,
    'amount': [100, 200, 150, 300, 250, 400]
})

# For 1M users with 10 purchases each = 10M rows
# Each address: ~30 bytes
# Redundant storage: 10M * 30 = 300 MB
# Repeated 10 times = 3 GB of redundant data!

print(f"Bad design memory: {df_bad.memory_usage(deep=True).sum() / 1024:.2f} KB")

# GOOD: Normalize (separate tables)
users = pd.DataFrame({
    'user_id': [1, 2],
    'user_name': ['John Doe', 'Jane Smith'],
    'user_email': ['john@example.com', 'jane@example.com'],
    'user_address': ['123 Main St, City, State', '456 Oak Ave, Town, State']
})

purchases = pd.DataFrame({
    'purchase_id': range(6),
    'user_id': [1, 1, 1, 2, 2, 2],
    'purchase_date': ['2026-01-01', '2026-01-15', '2026-02-01',
                      '2026-01-10', '2026-01-20', '2026-02-05'],
    'amount': [100, 200, 150, 300, 250, 400]
})

print(f"Good design memory: {(users.memory_usage(deep=True).sum() + purchases.memory_usage(deep=True).sum()) / 1024:.2f} KB")
```

#### 4. Poor Column Type Choices

```python
# Dataset: Product catalog with prices $0-$10,000

# BAD: Using float64 for prices
df_bad = pd.DataFrame({
    'product_id': range(1_000_000),
    'price': np.random.uniform(0, 10000, 1_000_000)  # float64
})

# Prices stored in dollars: 125.99
# But float64 uses 8 bytes
print(f"float64 storage: {df_bad['price'].nbytes / 1024**2:.2f} MB")

# GOOD: Store as integer cents
df_good = pd.DataFrame({
    'product_id': range(1_000_000),
    'price_cents': (np.random.uniform(0, 10000, 1_000_000) * 100).astype('int32')
})

# 12599 cents = $125.99
# int32 uses 4 bytes (50% savings)
print(f"int32 storage: {df_good['price_cents'].nbytes / 1024**2:.2f} MB")
print(f"Savings: 50%")

# For 100M products:
# float64: 763 MB
# int32:   381 MB
# Savings: 382 MB
```

#### 5. Storing Images Without Optimization

```python
# Image storage calculations

# Unoptimized image
width, height = 1920, 1080  # Full HD
channels = 3  # RGB
bytes_per_pixel = 1

unoptimized_size = width * height * channels * bytes_per_pixel
print(f"Unoptimized image: {unoptimized_size / 1024**2:.2f} MB")

# For 1 million images
print(f"1M images: {unoptimized_size * 1_000_000 / 1024**3:.2f} GB")

# Optimizations:
# 1. Resize for ML models (224x224 is common)
optimized_width, optimized_height = 224, 224
optimized_size = optimized_width * optimized_height * channels
print(f"\nResized (224x224): {optimized_size / 1024:.2f} KB")

# 2. JPEG compression (80-95% reduction)
jpeg_size = optimized_size * 0.1  # ~90% compression
print(f"After JPEG compression: {jpeg_size / 1024:.2f} KB")

# 3. For 1M images
print(f"\n1M images optimized: {jpeg_size * 1_000_000 / 1024**2:.2f} GB")

# Comparison
print(f"\nSavings: {(1 - (jpeg_size * 1_000_000) / (unoptimized_size * 1_000_000)) * 100:.1f}%")
```

---

## Data Types in Programming

### Python Built-in Types

```python
import sys
import numpy as np

print("Python Built-in Types:")
print(f"int:     {sys.getsizeof(0)} bytes (base overhead)")
print(f"float:   {sys.getsizeof(0.0)} bytes")
print(f"bool:    {sys.getsizeof(True)} bytes")
print(f"None:    {sys.getsizeof(None)} bytes")
print(f"str:     {sys.getsizeof('')} bytes (empty)")
print(f"list:    {sys.getsizeof([])} bytes (empty)")
print(f"dict:    {sys.getsizeof({})} bytes (empty)")
print(f"set:     {sys.getsizeof(set())} bytes (empty)")
print(f"tuple:   {sys.getsizeof(())} bytes (empty)")

# Integer size grows with value (arbitrary precision)
for i in [1, 100, 10000, 10**20, 10**100]:
    print(f"int({i}): {sys.getsizeof(i)} bytes")
```

### NumPy Data Types

```python
# NumPy fixed-size types (more efficient)
print("\nNumPy Array Types:")

# Integer types
int_types = [np.int8, np.int16, np.int32, np.int64,
             np.uint8, np.uint16, np.uint32, np.uint64]

for dtype in int_types:
    arr = np.array([1], dtype=dtype)
    print(f"{dtype.__name__:8s}: {arr.itemsize} bytes")

# Float types
float_types = [np.float16, np.float32, np.float64]

for dtype in float_types:
    arr = np.array([1.0], dtype=dtype)
    print(f"{dtype.__name__:8s}: {arr.itemsize} bytes")

# Complex types
print(f"complex64: {np.array([1+1j], dtype=np.complex64).itemsize} bytes")
print(f"complex128: {np.array([1+1j], dtype=np.complex128).itemsize} bytes")
```

### Pandas Data Types

```python
# Pandas dtype comparison
df = pd.DataFrame({
    'int64': pd.array([1, 2, 3], dtype='int64'),
    'int32': pd.array([1, 2, 3], dtype='int32'),
    'float64': pd.array([1.0, 2.0, 3.0], dtype='float64'),
    'float32': pd.array([1.0, 2.0, 3.0], dtype='float32'),
    'category': pd.Categorical(['A', 'B', 'C']),
    'object': ['A', 'B', 'C'],
    'bool': [True, False, True],
    'datetime': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03']),
})

print("\nPandas Column Memory Usage:")
for col in df.columns:
    memory = df[col].memory_usage(deep=True)
    print(f"{col:12s} ({df[col].dtype}): {memory} bytes")
```

### String Storage

```python
# String encoding matters
text = "Hello, World! 你好世界"

# Different encodings
encodings = ['utf-8', 'utf-16', 'utf-32', 'ascii']

print("\nString Encoding Sizes:")
for encoding in encodings:
    try:
        encoded = text.encode(encoding)
        print(f"{encoding:8s}: {len(encoded)} bytes")
    except:
        print(f"{encoding:8s}: Cannot encode")

# For large text datasets:
# - ASCII: 1 byte per character (English only)
# - UTF-8: 1-4 bytes per character (variable, efficient for English)
# - UTF-16: 2-4 bytes per character (fixed for most languages)
# - UTF-32: 4 bytes per character (fixed, inefficient)

# Best practice: Use UTF-8 for storage
```

---

## Database Storage Considerations

### SQL Data Types and Sizes

```sql
-- MySQL / PostgreSQL Data Types

-- Integer Types
TINYINT          -- 1 byte  (-128 to 127)
SMALLINT         -- 2 bytes (-32,768 to 32,767)
MEDIUMINT        -- 3 bytes (-8M to 8M) [MySQL only]
INT / INTEGER    -- 4 bytes (-2.1B to 2.1B)
BIGINT           -- 8 bytes (-9.2E18 to 9.2E18)

-- Unsigned variants (positive only, doubles range)
UNSIGNED TINYINT   -- 0 to 255
UNSIGNED SMALLINT  -- 0 to 65,535
UNSIGNED INT       -- 0 to 4.2B
UNSIGNED BIGINT    -- 0 to 18.4E18

-- Decimal / Numeric
DECIMAL(P, S)    -- Variable (P = precision, S = scale)
FLOAT            -- 4 bytes (7 significant digits)
DOUBLE           -- 8 bytes (15 significant digits)

-- String Types
CHAR(N)          -- Fixed N bytes (padded)
VARCHAR(N)       -- Variable up to N bytes + 1-2 bytes overhead
TEXT             -- Up to 65,535 bytes
MEDIUMTEXT       -- Up to 16 MB
LONGTEXT         -- Up to 4 GB

-- Binary Types
BLOB             -- Up to 65,535 bytes
MEDIUMBLOB       -- Up to 16 MB
LONGBLOB         -- Up to 4 GB

-- Date/Time Types
DATE             -- 3 bytes (YYYY-MM-DD)
TIME             -- 3 bytes (HH:MM:SS)
DATETIME         -- 8 bytes (YYYY-MM-DD HH:MM:SS)
TIMESTAMP        -- 4 bytes (UNIX timestamp)
YEAR             -- 1 byte (YYYY)

-- Boolean
BOOLEAN / BOOL   -- 1 byte (actually TINYINT(1))
```

### Database Storage Calculation Example

```python
# E-commerce database calculation

# Users table (10 million users)
users_schema = {
    'user_id': ('BIGINT', 8),           # 8 bytes
    'email': ('VARCHAR(255)', 50),       # Avg 50 bytes
    'name': ('VARCHAR(100)', 30),        # Avg 30 bytes
    'password_hash': ('CHAR(64)', 64),   # 64 bytes
    'created_at': ('TIMESTAMP', 4),      # 4 bytes
    'is_active': ('BOOLEAN', 1),         # 1 byte
}

# Calculate row size
users_row_size = sum(size for _, size in users_schema.values())
users_count = 10_000_000

print("Users Table:")
print(f"Row size: {users_row_size} bytes")
print(f"Total rows: {users_count:,}")
print(f"Data size: {users_row_size * users_count / 1024**3:.2f} GB")

# Add indexes (typically 20-30% overhead)
index_overhead = 0.25
total_with_indexes = users_row_size * users_count * (1 + index_overhead)
print(f"With indexes: {total_with_indexes / 1024**3:.2f} GB")

# Orders table (100 million orders)
orders_schema = {
    'order_id': ('BIGINT', 8),
    'user_id': ('BIGINT', 8),
    'total': ('DECIMAL(10,2)', 5),
    'status': ('VARCHAR(20)', 10),
    'created_at': ('TIMESTAMP', 4),
}

orders_row_size = sum(size for _, size in orders_schema.values())
orders_count = 100_000_000

print(f"\nOrders Table:")
print(f"Row size: {orders_row_size} bytes")
print(f"Total rows: {orders_count:,}")
print(f"Data size: {orders_row_size * orders_count / 1024**3:.2f} GB")
print(f"With indexes: {orders_row_size * orders_count * 1.25 / 1024**3:.2f} GB")

# Total database size
total_db_size = (total_with_indexes + orders_row_size * orders_count * 1.25) / 1024**3
print(f"\nTotal Database Size: {total_db_size:.2f} GB")
```

### Index Overhead

```python
def calculate_index_size(rows, key_size, pointer_size=6):
    """
    Calculate B-tree index size
    
    key_size: Size of indexed column(s) in bytes
    pointer_size: Pointer to row (typically 6 bytes)
    """
    entry_size = key_size + pointer_size
    index_size = rows * entry_size
    
    # B-tree overhead (~30%)
    btree_overhead = 1.3
    total_size = index_size * btree_overhead
    
    return total_size / 1024**2  # MB

# Example: Index on email (50 bytes) for 10M users
email_index_size = calculate_index_size(10_000_000, 50)
print(f"Email index size: {email_index_size:.2f} MB")

# Composite index (user_id + created_at)
composite_index_size = calculate_index_size(10_000_000, 8 + 4)
print(f"Composite index size: {composite_index_size:.2f} MB")

# Multiple indexes add up!
# 5 indexes = 5x the storage
```

---

## Cloud Storage Costs

### AWS S3 Pricing (January 2026)

```python
# AWS S3 Standard Storage Pricing (US East)
# Source: https://aws.amazon.com/s3/pricing/

class S3PricingCalculator:
    # Storage costs (per GB per month)
    STORAGE_FIRST_50TB = 0.023    # $0.023/GB
    STORAGE_NEXT_450TB = 0.022    # $0.022/GB
    STORAGE_OVER_500TB = 0.021    # $0.021/GB
    
    # Request costs
    PUT_POST_COPY = 0.005 / 1000   # $0.005 per 1,000 requests
    GET_SELECT = 0.0004 / 1000     # $0.0004 per 1,000 requests
    
    # Data transfer (out to internet)
    TRANSFER_FIRST_1GB = 0.00       # Free
    TRANSFER_NEXT_9TB = 0.09        # $0.09/GB
    TRANSFER_NEXT_40TB = 0.085      # $0.085/GB
    TRANSFER_OVER_150TB = 0.05      # $0.05/GB
    
    @staticmethod
    def calculate_storage_cost(gb_per_month):
        """Calculate monthly storage cost"""
        if gb_per_month <= 50 * 1024:  # 50 TB
            return gb_per_month * S3PricingCalculator.STORAGE_FIRST_50TB
        elif gb_per_month <= 500 * 1024:  # 500 TB
            cost = 50 * 1024 * S3PricingCalculator.STORAGE_FIRST_50TB
            cost += (gb_per_month - 50 * 1024) * S3PricingCalculator.STORAGE_NEXT_450TB
            return cost
        else:
            cost = 50 * 1024 * S3PricingCalculator.STORAGE_FIRST_50TB
            cost += 450 * 1024 * S3PricingCalculator.STORAGE_NEXT_450TB
            cost += (gb_per_month - 500 * 1024) * S3PricingCalculator.STORAGE_OVER_500TB
            return cost
    
    @staticmethod
    def calculate_request_cost(puts, gets):
        """Calculate request costs"""
        put_cost = puts * S3PricingCalculator.PUT_POST_COPY
        get_cost = gets * S3PricingCalculator.GET_SELECT
        return put_cost + get_cost
    
    @staticmethod
    def calculate_transfer_cost(gb_transferred):
        """Calculate data transfer out cost"""
        if gb_transferred <= 1:
            return 0
        elif gb_transferred <= 10 * 1024:  # 10 TB
            return (gb_transferred - 1) * S3PricingCalculator.TRANSFER_NEXT_9TB
        elif gb_transferred <= 50 * 1024:  # 50 TB
            cost = 10 * 1024 * S3PricingCalculator.TRANSFER_NEXT_9TB
            cost += (gb_transferred - 10 * 1024) * S3PricingCalculator.TRANSFER_NEXT_40TB
            return cost
        else:
            cost = 10 * 1024 * S3PricingCalculator.TRANSFER_NEXT_9TB
            cost += 40 * 1024 * S3PricingCalculator.TRANSFER_NEXT_40TB
            cost += (gb_transferred - 50 * 1024) * S3PricingCalculator.TRANSFER_OVER_150TB
            return cost

# Example: ML Training Data Storage
print("=== AWS S3 Cost Example ===")
print("\nScenario: ML training dataset")

# Dataset: 1 TB of training data
storage_gb = 1024  # 1 TB
storage_cost = S3PricingCalculator.calculate_storage_cost(storage_gb)
print(f"\nStorage: {storage_gb} GB")
print(f"Monthly storage cost: ${storage_cost:.2f}")

# Uploads: 100,000 images uploaded once
put_requests = 100_000
# Training: 10 epochs, each reads all data
get_requests = 100_000 * 10
request_cost = S3PricingCalculator.calculate_request_cost(put_requests, get_requests)
print(f"\nRequests:")
print(f"  PUT: {put_requests:,}")
print(f"  GET: {get_requests:,}")
print(f"  Request cost: ${request_cost:.2f}")

# Data transfer: Download for local training
transfer_gb = storage_gb
transfer_cost = S3PricingCalculator.calculate_transfer_cost(transfer_gb)
print(f"\nData transfer out: {transfer_gb} GB")
print(f"Transfer cost: ${transfer_cost:.2f}")

# Total
total_cost = storage_cost + request_cost + transfer_cost
print(f"\n{'='*40}")
print(f"TOTAL MONTHLY COST: ${total_cost:.2f}")
print(f"{'='*40}")

# Annual cost
print(f"Annual cost: ${total_cost * 12:.2f}")
```

### Google Cloud Storage Pricing

```python
class GCSPricingCalculator:
    # Storage costs (per GB per month)
    STANDARD = 0.020    # $0.020/GB
    NEARLINE = 0.010    # $0.010/GB (30 day minimum)
    COLDLINE = 0.004    # $0.004/GB (90 day minimum)
    ARCHIVE = 0.0012    # $0.0012/GB (365 day minimum)
    
    # Operation costs
    CLASS_A_OPS = 0.05 / 10000   # $0.05 per 10,000 ops (writes)
    CLASS_B_OPS = 0.004 / 10000  # $0.004 per 10,000 ops (reads)
    
    # Network egress (per GB)
    EGRESS_WORLDWIDE = 0.12  # $0.12/GB
    
    @staticmethod
    def calculate_cost(storage_gb, class_a_ops, class_b_ops, egress_gb, 
                       storage_class='STANDARD'):
        """Calculate GCS costs"""
        storage_rates = {
            'STANDARD': GCSPricingCalculator.STANDARD,
            'NEARLINE': GCSPricingCalculator.NEARLINE,
            'COLDLINE': GCSPricingCalculator.COLDLINE,
            'ARCHIVE': GCSPricingCalculator.ARCHIVE,
        }
        
        storage_cost = storage_gb * storage_rates[storage_class]
        ops_cost = (class_a_ops * GCSPricingCalculator.CLASS_A_OPS + 
                   class_b_ops * GCSPricingCalculator.CLASS_B_OPS)
        egress_cost = egress_gb * GCSPricingCalculator.EGRESS_WORLDWIDE
        
        return {
            'storage': storage_cost,
            'operations': ops_cost,
            'egress': egress_cost,
            'total': storage_cost + ops_cost + egress_cost
        }

# Example: Compare storage classes
storage_gb = 1024
class_a_ops = 100_000
class_b_ops = 1_000_000
egress_gb = 100

print("\n=== Google Cloud Storage Cost Comparison ===")
for storage_class in ['STANDARD', 'NEARLINE', 'COLDLINE', 'ARCHIVE']:
    costs = GCSPricingCalculator.calculate_cost(
        storage_gb, class_a_ops, class_b_ops, egress_gb, storage_class
    )
    print(f"\n{storage_class}:")
    print(f"  Storage:    ${costs['storage']:.2f}")
    print(f"  Operations: ${costs['operations']:.2f}")
    print(f"  Egress:     ${costs['egress']:.2f}")
    print(f"  TOTAL:      ${costs['total']:.2f}/month")
```

### Azure Blob Storage Pricing

```python
class AzureBlobPricingCalculator:
    # Hot tier (frequently accessed)
    HOT_STORAGE_FIRST_50TB = 0.018  # $0.018/GB
    HOT_WRITE_OPS = 0.05 / 10000    # $0.05 per 10,000
    HOT_READ_OPS = 0.004 / 10000    # $0.004 per 10,000
    
    # Cool tier (infrequently accessed, 30 day minimum)
    COOL_STORAGE_FIRST_50TB = 0.01  # $0.01/GB
    COOL_WRITE_OPS = 0.10 / 10000   # $0.10 per 10,000
    COOL_READ_OPS = 0.01 / 10000    # $0.01 per 10,000
    
    # Archive tier (rarely accessed, 180 day minimum)
    ARCHIVE_STORAGE = 0.00099       # $0.00099/GB
    
    # Data transfer out
    EGRESS_FIRST_5GB = 0.00         # Free
    EGRESS_NEXT_10TB = 0.087        # $0.087/GB
    
    @staticmethod
    def calculate_cost(storage_gb, write_ops, read_ops, egress_gb, tier='HOT'):
        """Calculate Azure Blob costs"""
        if tier == 'HOT':
            storage_cost = storage_gb * AzureBlobPricingCalculator.HOT_STORAGE_FIRST_50TB
            ops_cost = (write_ops * AzureBlobPricingCalculator.HOT_WRITE_OPS + 
                       read_ops * AzureBlobPricingCalculator.HOT_READ_OPS)
        elif tier == 'COOL':
            storage_cost = storage_gb * AzureBlobPricingCalculator.COOL_STORAGE_FIRST_50TB
            ops_cost = (write_ops * AzureBlobPricingCalculator.COOL_WRITE_OPS + 
                       read_ops * AzureBlobPricingCalculator.COOL_READ_OPS)
        elif tier == 'ARCHIVE':
            storage_cost = storage_gb * AzureBlobPricingCalculator.ARCHIVE_STORAGE
            ops_cost = 0  # Archive operations priced differently
        
        if egress_gb <= 5:
            egress_cost = 0
        else:
            egress_cost = (egress_gb - 5) * AzureBlobPricingCalculator.EGRESS_NEXT_10TB
        
        return {
            'storage': storage_cost,
            'operations': ops_cost,
            'egress': egress_cost,
            'total': storage_cost + ops_cost + egress_cost
        }

# Example comparison
print("\n=== Azure Blob Storage Cost Comparison ===")
for tier in ['HOT', 'COOL', 'ARCHIVE']:
    costs = AzureBlobPricingCalculator.calculate_cost(
        1024, 100_000, 1_000_000, 100, tier
    )
    print(f"\n{tier} Tier:")
    print(f"  Storage:    ${costs['storage']:.2f}")
    print(f"  Operations: ${costs['operations']:.2f}")
    print(f"  Egress:     ${costs['egress']:.2f}")
    print(f"  TOTAL:      ${costs['total']:.2f}/month")
```

### Cloud Cost Comparison Summary

```python
def compare_cloud_storage(storage_gb, monthly_reads, monthly_writes, egress_gb):
    """Compare costs across cloud providers"""
    
    print(f"\n{'='*60}")
    print(f"Storage Comparison: {storage_gb} GB")
    print(f"Monthly Reads: {monthly_reads:,}")
    print(f"Monthly Writes: {monthly_writes:,}")
    print(f"Egress: {egress_gb} GB")
    print(f"{'='*60}")
    
    # AWS S3
    aws_storage = S3PricingCalculator.calculate_storage_cost(storage_gb)
    aws_requests = S3PricingCalculator.calculate_request_cost(monthly_writes, monthly_reads)
    aws_egress = S3PricingCalculator.calculate_transfer_cost(egress_gb)
    aws_total = aws_storage + aws_requests + aws_egress
    
    # GCS
    gcs_costs = GCSPricingCalculator.calculate_cost(
        storage_gb, monthly_writes, monthly_reads, egress_gb, 'STANDARD'
    )
    
    # Azure
    azure_costs = AzureBlobPricingCalculator.calculate_cost(
        storage_gb, monthly_writes, monthly_reads, egress_gb, 'HOT'
    )
    
    # Print comparison
    providers = {
        'AWS S3': aws_total,
        'Google Cloud Storage': gcs_costs['total'],
        'Azure Blob (Hot)': azure_costs['total']
    }
    
    print("\nMonthly Costs:")
    for provider, cost in sorted(providers.items(), key=lambda x: x[1]):
        print(f"  {provider:25s}: ${cost:8.2f}")
    
    print("\nAnnual Costs:")
    for provider, cost in sorted(providers.items(), key=lambda x: x[1]):
        print(f"  {provider:25s}: ${cost*12:8.2f}")
    
    # Cheapest option
    cheapest = min(providers.items(), key=lambda x: x[1])
    print(f"\nCheapest: {cheapest[0]} at ${cheapest[1]:.2f}/month")

# Example: Image dataset for ML
compare_cloud_storage(
    storage_gb=5000,      # 5 TB of images
    monthly_reads=10_000_000,  # 10M reads for training
    monthly_writes=500_000,    # 500K new images
    egress_gb=1000        # 1 TB download for local training
)
```

---

## Data Compression Techniques

### Text Compression

```python
import gzip
import bz2
import lzma
import pickle
import json

# Sample data
data = {
    'user_id': 12345,
    'timestamp': '2026-01-23T10:30:00Z',
    'event': 'page_view',
    'page': '/products/laptop-xyz-123',
    'session_id': 'abc123def456ghi789',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'ip_address': '192.168.1.100'
}

# Serialize to JSON
json_data = json.dumps(data).encode('utf-8')
original_size = len(json_data)

print("Compression Comparison:")
print(f"Original (JSON): {original_size} bytes")

# GZIP compression
gzipped = gzip.compress(json_data)
print(f"GZIP:            {len(gzipped)} bytes ({len(gzipped)/original_size*100:.1f}%)")

# BZIP2 compression (better ratio, slower)
bzipped = bz2.compress(json_data)
print(f"BZIP2:           {len(bzipped)} bytes ({len(bzipped)/original_size*100:.1f}%)")

# LZMA compression (best ratio, slowest)
lzmaed = lzma.compress(json_data)
print(f"LZMA:            {len(lzmaed)} bytes ({len(lzmaed)/original_size*100:.1f}%)")

# For 1 million records
print(f"\nFor 1M records:")
print(f"Original: {original_size * 1_000_000 / 1024**2:.2f} MB")
print(f"GZIP:     {len(gzipped) * 1_000_000 / 1024**2:.2f} MB")
print(f"BZIP2:    {len(bzipped) * 1_000_000 / 1024**2:.2f} MB")
print(f"LZMA:     {len(lzmaed) * 1_000_000 / 1024**2:.2f} MB")
```

### Parquet vs CSV

```python
import pandas as pd
import os

# Create sample dataset
df = pd.DataFrame({
    'id': range(1_000_000),
    'timestamp': pd.date_range('2026-01-01', periods=1_000_000, freq='s'),
    'value': np.random.randn(1_000_000),
    'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 1_000_000),
    'description': ['Some description text ' * 5] * 1_000_000
})

print("Dataset size in memory:")
print(f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Save as CSV
df.to_csv('data.csv', index=False)
csv_size = os.path.getsize('data.csv')
print(f"\nCSV size: {csv_size / 1024**2:.2f} MB")

# Save as Parquet (default compression)
df.to_parquet('data.parquet', engine='pyarrow', compression='snappy')
parquet_size = os.path.getsize('data.parquet')
print(f"Parquet (snappy): {parquet_size / 1024**2:.2f} MB")

# Save as Parquet (GZIP compression)
df.to_parquet('data_gzip.parquet', engine='pyarrow', compression='gzip')
parquet_gzip_size = os.path.getsize('data_gzip.parquet')
print(f"Parquet (gzip): {parquet_gzip_size / 1024**2:.2f} MB")

# Comparison
print(f"\nParquet vs CSV savings: {(1 - parquet_size/csv_size)*100:.1f}%")

# Read speed comparison
import time

# CSV read
start = time.time()
df_csv = pd.read_csv('data.csv')
csv_time = time.time() - start

# Parquet read
start = time.time()
df_parquet = pd.read_parquet('data.parquet')
parquet_time = time.time() - start

print(f"\nRead Performance:")
print(f"CSV:     {csv_time:.2f} seconds")
print(f"Parquet: {parquet_time:.2f} seconds")
print(f"Parquet is {csv_time/parquet_time:.1f}x faster")

# Cleanup
os.remove('data.csv')
os.remove('data.parquet')
os.remove('data_gzip.parquet')
```

### Image Compression for ML

```python
from PIL import Image
import io

def compress_image(image_path, quality=85):
    """Compress image for storage"""
    img = Image.open(image_path)
    
    # Original size
    original_size = os.path.getsize(image_path)
    
    # Resize if too large (maintain aspect ratio)
    max_size = (1024, 1024)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Save as JPEG with compression
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality, optimize=True)
    compressed_size = buffer.tell()
    
    return {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': original_size / compressed_size,
        'savings_percent': (1 - compressed_size/original_size) * 100
    }

# For ML training, typical compression:
# - Resize to 224x224 or 299x299
# - JPEG quality 85-95
# - Result: 70-90% size reduction
```

### Columnar Format Benefits

```python
"""
Why Parquet/Arrow for ML:

1. COLUMNAR STORAGE:
   - Read only needed columns
   - Better compression (similar values together)
   - Faster for analytics

2. TYPE-AWARE:
   - Stores data type information
   - No parsing needed
   - Preserves precision

3. COMPRESSION:
   - Column-level compression
   - Better compression ratios
   - Multiple compression algorithms

4. METADATA:
   - Schema stored in file
   - Statistics for query optimization
   - Partitioning information

Example:
Dataset with 100 columns, 1M rows
Task: Analyze 3 columns

CSV:
- Must read entire file: 1 GB
- Parse all columns
- Time: 10 seconds

Parquet:
- Read only 3 columns: 30 MB
- No parsing needed
- Time: 0.5 seconds

20x faster, 97% less data read!
"""
```

---

## Real-World Cost Examples

### Example 1: Startup ML Platform

```python
print("="*60)
print("STARTUP ML PLATFORM COSTS")
print("="*60)

# Company: ML-powered analytics for e-commerce
# Stage: Early startup, 1000 customers, growing fast

# Data generated per customer per month
events_per_customer = 100_000  # page views, clicks, purchases
bytes_per_event = 500          # JSON event data
customers = 1_000

# Monthly data
monthly_data_gb = (events_per_customer * bytes_per_event * customers) / 1024**3
print(f"\nMonthly data generated: {monthly_data_gb:.2f} GB")

# Storage requirements (keep 2 years)
storage_months = 24
total_storage_gb = monthly_data_gb * storage_months
print(f"Total storage (2 years): {total_storage_gb:.2f} GB ({total_storage_gb/1024:.2f} TB)")

# AWS S3 costs
storage_cost = S3PricingCalculator.calculate_storage_cost(total_storage_gb)

# Requests: 
# - Writes: 100M events/month
# - Reads: 10x for analysis
monthly_writes = events_per_customer * customers
monthly_reads = monthly_writes * 10
request_cost = S3PricingCalculator.calculate_request_cost(monthly_writes, monthly_reads)

# Transfer: 10% of data downloaded for model training
transfer_gb = total_storage_gb * 0.1
transfer_cost = S3PricingCalculator.calculate_transfer_cost(transfer_gb)

print(f"\nMonthly AWS Costs:")
print(f"  Storage:  ${storage_cost:.2f}")
print(f"  Requests: ${request_cost:.2f}")
print(f"  Transfer: ${transfer_cost:.2f}")
print(f"  TOTAL:    ${storage_cost + request_cost + transfer_cost:.2f}")

# Annual cost
annual_cost = (storage_cost + request_cost + transfer_cost) * 12
print(f"\nAnnual cost: ${annual_cost:.2f}")

# Optimization potential
print(f"\n{'='*60}")
print("OPTIMIZATION STRATEGIES:")
print(f"{'='*60}")

# 1. Compression (50% reduction)
compressed_storage = total_storage_gb * 0.5
compressed_cost = S3PricingCalculator.calculate_storage_cost(compressed_storage)
print(f"\n1. Enable compression (50% reduction):")
print(f"   Storage: ${compressed_cost:.2f}/month")
print(f"   Savings: ${(storage_cost - compressed_cost)*12:.2f}/year")

# 2. Lifecycle policies (move old data to cheaper tier)
# Keep 6 months in standard, move rest to Glacier
standard_storage = monthly_data_gb * 6
glacier_storage = total_storage_gb - standard_storage
standard_cost = S3PricingCalculator.calculate_storage_cost(standard_storage)
glacier_cost = glacier_storage * 0.004  # Glacier Deep Archive
lifecycle_cost = standard_cost + glacier_cost
print(f"\n2. Lifecycle policy (6 months standard, rest archive):")
print(f"   Storage: ${lifecycle_cost:.2f}/month")
print(f"   Savings: ${(storage_cost - lifecycle_cost)*12:.2f}/year")

# 3. Optimize data types
# Current: JSON strings (inefficient)
# Optimized: Parquet with proper types (70% reduction)
optimized_data_gb = total_storage_gb * 0.3
optimized_cost = S3PricingCalculator.calculate_storage_cost(optimized_data_gb)
print(f"\n3. Use Parquet instead of JSON (70% reduction):")
print(f"   Storage: ${optimized_cost:.2f}/month")
print(f"   Savings: ${(storage_cost - optimized_cost)*12:.2f}/year")

# Combined optimization
combined_storage = optimized_data_gb  # Already includes best practices
combined_cost = S3PricingCalculator.calculate_storage_cost(combined_storage)
print(f"\n4. COMBINED (all optimizations):")
print(f"   Storage: ${combined_cost:.2f}/month")
print(f"   Savings: ${(storage_cost - combined_cost)*12:.2f}/year")
print(f"   Reduction: {(1 - combined_cost/storage_cost)*100:.1f}%")
```

### Example 2: Image Dataset for Computer Vision

```python
print("\n" + "="*60)
print("COMPUTER VISION DATASET COSTS")
print("="*60)

# Project: Object detection model training
# Dataset: 10 million images

images_count = 10_000_000

# Scenario 1: Poor optimization
# - Store raw 1920x1080 images
# - PNG format (lossless)
# - No resizing

width, height = 1920, 1080
channels = 3
bytes_per_pixel = 1

unoptimized_per_image = width * height * channels * bytes_per_pixel
unoptimized_total = (unoptimized_per_image * images_count) / 1024**3

print(f"\nScenario 1: UNOPTIMIZED")
print(f"  Resolution: {width}x{height}")
print(f"  Format: PNG")
print(f"  Per image: {unoptimized_per_image / 1024**2:.2f} MB")
print(f"  Total: {unoptimized_total:.2f} GB ({unoptimized_total/1024:.2f} TB)")

unoptimized_cost = S3PricingCalculator.calculate_storage_cost(unoptimized_total)
print(f"  Monthly S3 cost: ${unoptimized_cost:.2f}")
print(f"  Annual cost: ${unoptimized_cost*12:.2f}")

# Scenario 2: Optimized for ML
# - Resize to 224x224 (common for transfer learning)
# - JPEG format with quality=90
# - 90% compression

opt_width, opt_height = 224, 224
jpeg_compression = 0.1  # JPEG reduces to ~10% of raw size

optimized_per_image = opt_width * opt_height * channels * bytes_per_pixel * jpeg_compression
optimized_total = (optimized_per_image * images_count) / 1024**3

print(f"\nScenario 2: OPTIMIZED FOR ML")
print(f"  Resolution: {opt_width}x{opt_height}")
print(f"  Format: JPEG (quality=90)")
print(f"  Per image: {optimized_per_image / 1024:.2f} KB")
print(f"  Total: {optimized_total:.2f} GB")

optimized_cost = S3PricingCalculator.calculate_storage_cost(optimized_total)
print(f"  Monthly S3 cost: ${optimized_cost:.2f}")
print(f"  Annual cost: ${optimized_cost*12:.2f}")

# Savings
savings = unoptimized_cost - optimized_cost
savings_percent = (1 - optimized_total/unoptimized_total) * 100

print(f"\n{'='*60}")
print(f"SAVINGS:")
print(f"  Storage: {unoptimized_total - optimized_total:.2f} GB saved")
print(f"  Reduction: {savings_percent:.1f}%")
print(f"  Monthly: ${savings:.2f}")
print(f"  Annual: ${savings*12:.2f}")
print(f"{'='*60}")

# Additional considerations
print(f"\nADDITIONAL BENEFITS:")
print(f"  - Faster downloads (less data)")
print(f"  - Faster training (smaller I/O)")
print(f"  - Lower egress costs")
print(f"  - Sufficient for most ML models")
```

### Example 3: Time Series IoT Data

```python
print("\n" + "="*60)
print("IOT TIME SERIES DATA COSTS")
print("="*60)

# Project: Smart home sensor data
# 100,000 homes, each with 10 sensors
# Sensors report every minute

homes = 100_000
sensors_per_home = 10
readings_per_day = 24 * 60  # Every minute
days_per_year = 365

# Data per reading
reading_schema = {
    'home_id': 8,        # BIGINT
    'sensor_id': 4,      # INT
    'timestamp': 8,      # DATETIME
    'value': 4,          # FLOAT32
    'status': 1,         # TINYINT
}
bytes_per_reading = sum(reading_schema.values())

# Calculate yearly data
total_readings = homes * sensors_per_home * readings_per_day * days_per_year
yearly_data_gb = (total_readings * bytes_per_reading) / 1024**3

print(f"\nData Generation:")
print(f"  Homes: {homes:,}")
print(f"  Sensors per home: {sensors_per_home}")
print(f"  Readings per day: {readings_per_day:,}")
print(f"  Total readings/year: {total_readings:,}")
print(f"  Bytes per reading: {bytes_per_reading}")
print(f"  Yearly data: {yearly_data_gb:.2f} GB")

# Storage strategy 1: Store all raw data
raw_storage_gb = yearly_data_gb * 3  # Keep 3 years
raw_cost = S3PricingCalculator.calculate_storage_cost(raw_storage_gb)

print(f"\nStrategy 1: Store all raw data (3 years)")
print(f"  Storage: {raw_storage_gb:.2f} GB")
print(f"  Monthly cost: ${raw_cost:.2f}")
print(f"  Annual cost: ${raw_cost*12:.2f}")

# Storage strategy 2: Aggregate + raw
# - Keep raw data for 30 days
# - Aggregate to 5-minute intervals for 1 year
# - Aggregate to hourly for 2 years

raw_30days = yearly_data_gb * (30/365)
aggregated_5min = yearly_data_gb * (1/5) * 1  # 1 year, 5x reduction
aggregated_hourly = yearly_data_gb * (1/60) * 2  # 2 years, 60x reduction

smart_storage_gb = raw_30days + aggregated_5min + aggregated_hourly
smart_cost = S3PricingCalculator.calculate_storage_cost(smart_storage_gb)

print(f"\nStrategy 2: Smart aggregation")
print(f"  Raw (30 days): {raw_30days:.2f} GB")
print(f"  5-min aggregates (1 year): {aggregated_5min:.2f} GB")
print(f"  Hourly aggregates (2 years): {aggregated_hourly:.2f} GB")
print(f"  Total storage: {smart_storage_gb:.2f} GB")
print(f"  Monthly cost: ${smart_cost:.2f}")
print(f"  Annual cost: ${smart_cost*12:.2f}")

# Savings
savings = raw_cost - smart_cost
savings_percent = (1 - smart_storage_gb/raw_storage_gb) * 100

print(f"\n{'='*60}")
print(f"SMART AGGREGATION SAVINGS:")
print(f"  Storage: {raw_storage_gb - smart_storage_gb:.2f} GB saved")
print(f"  Reduction: {savings_percent:.1f}%")
print(f"  Annual savings: ${savings*12:.2f}")
print(f"{'='*60}")
```

---

## Data Optimization Strategies

### Strategy 1: Choose Right Data Types

```python
def optimize_dataframe_dtypes(df):
    """
    Automatically optimize DataFrame data types
    """
    memory_before = df.memory_usage(deep=True).sum()
    
    for col in df.columns:
        col_type = df[col].dtype
        
        # Optimize integers
        if col_type == 'int64':
            c_min = df[col].min()
            c_max = df[col].max()
            if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                df[col] = df[col].astype(np.int8)
            elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                df[col] = df[col].astype(np.int16)
            elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                df[col] = df[col].astype(np.int32)
        
        # Optimize floats
        elif col_type == 'float64':
            c_min = df[col].min()
            c_max = df[col].max()
            if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                df[col] = df[col].astype(np.float32)
        
        # Convert to category if few unique values
        elif col_type == 'object':
            num_unique_values = len(df[col].unique())
            num_total_values = len(df[col])
            if num_unique_values / num_total_values < 0.5:  # Less than 50% unique
                df[col] = df[col].astype('category')
    
    memory_after = df.memory_usage(deep=True).sum()
    reduction = (memory_before - memory_after) / memory_before * 100
    
    print(f"Memory usage before: {memory_before / 1024**2:.2f} MB")
    print(f"Memory usage after:  {memory_after / 1024**2:.2f} MB")
    print(f"Reduction: {reduction:.1f}%")
    
    return df

# Example usage
df = pd.DataFrame({
    'id': range(1_000_000),
    'value': np.random.randint(0, 100, 1_000_000),
    'price': np.random.uniform(0, 1000, 1_000_000),
    'category': np.random.choice(['A', 'B', 'C'], 1_000_000)
})

df_optimized = optimize_dataframe_dtypes(df.copy())
```

### Strategy 2: Data Partitioning

```python
"""
DATA PARTITIONING STRATEGIES

1. TIME-BASED PARTITIONING:
   /data/year=2026/month=01/day=23/data.parquet
   
   Benefits:
   - Query only relevant time periods
   - Easy to archive old data
   - Efficient for time-series analysis
   
   Example:
   SELECT * FROM data WHERE year=2026 AND month=01
   → Only scans January 2026 partition

2. CATEGORY-BASED PARTITIONING:
   /data/country=US/state=CA/data.parquet
   
   Benefits:
   - Isolate by region/category
   - Parallel processing
   - Compliance (data locality)
   
   Example:
   SELECT * FROM data WHERE country='US'
   → Only scans US partition

3. HASH-BASED PARTITIONING:
   /data/hash=0/data.parquet
   /data/hash=1/data.parquet
   ...
   /data/hash=255/data.parquet
   
   Benefits:
   - Uniform distribution
   - Load balancing
   - Parallel writes
   
   Example:
   hash(user_id) % 256 = partition_number
"""

# Example: Partition by date
def partition_by_date(df, output_dir):
    """Partition DataFrame by date"""
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    
    # Save partitioned
    df.to_parquet(
        output_dir,
        partition_cols=['year', 'month', 'day'],
        engine='pyarrow'
    )
    
    # Query specific partition
    # df = pd.read_parquet(output_dir, 
    #                      filters=[('year', '=', 2026), 
    #                              ('month', '=', 1)])
```

### Strategy 3: Compression Selection

```python
"""
COMPRESSION ALGORITHM SELECTION

1. SNAPPY (Default for Parquet):
   - Compression ratio: 2-3x
   - Speed: Very fast
   - CPU: Low
   - Use case: Real-time data, frequent access
   
2. GZIP:
   - Compression ratio: 4-6x
   - Speed: Medium
   - CPU: Medium
   - Use case: Archived data, infrequent access
   
3. ZSTD (Zstandard):
   - Compression ratio: 3-5x
   - Speed: Fast
   - CPU: Low-Medium
   - Use case: Best balance, modern default
   
4. BROTLI:
   - Compression ratio: 5-7x
   - Speed: Slow
   - CPU: High
   - Use case: Text, JSON, maximum compression
   
5. LZ4:
   - Compression ratio: 2x
   - Speed: Very fast (fastest)
   - CPU: Very low
   - Use case: Real-time streaming

SELECTION GUIDE:
┌─────────────────────────────────────────────┐
│ Need fastest speed? → LZ4 or Snappy         │
│ Need best compression? → GZIP or Brotli     │
│ Need balance? → ZSTD                        │
│ Text/JSON? → Brotli                         │
│ Time series numbers? → Delta + Snappy       │
└─────────────────────────────────────────────┘
"""

# Example: Compare compression for your data
def compare_compression(df, filename_base):
    """Compare different compression methods"""
    compressions = ['snappy', 'gzip', 'brotli', 'zstd']
    results = {}
    
    for comp in compressions:
        try:
            import time
            
            # Write
            start = time.time()
            filepath = f"{filename_base}_{comp}.parquet"
            df.to_parquet(filepath, compression=comp, engine='pyarrow')
            write_time = time.time() - start
            
            # Size
            size = os.path.getsize(filepath) / 1024**2  # MB
            
            # Read
            start = time.time()
            pd.read_parquet(filepath)
            read_time = time.time() - start
            
            results[comp] = {
                'size_mb': size,
                'write_time': write_time,
                'read_time': read_time
            }
            
            os.remove(filepath)
        except:
            print(f"Compression {comp} not available")
    
    # Print comparison
    print("\nCompression Comparison:")
    print(f"{'Method':<10} {'Size (MB)':<12} {'Write (s)':<12} {'Read (s)':<12}")
    print("-" * 50)
    for method, metrics in sorted(results.items(), key=lambda x: x[1]['size_mb']):
        print(f"{method:<10} {metrics['size_mb']:<12.2f} {metrics['write_time']:<12.2f} {metrics['read_time']:<12.2f}")
    
    return results
```

### Strategy 4: Incremental Processing

```python
"""
INCREMENTAL PROCESSING

Instead of reprocessing entire dataset:
1. Track what's been processed
2. Process only new/changed data
3. Merge results

Benefits:
- Faster processing
- Lower compute costs
- Lower storage I/O costs
"""

def incremental_processing_example():
    """Example of incremental processing"""
    
    # Track last processed timestamp
    last_processed = load_checkpoint('last_processed_timestamp')
    
    # Query only new data
    new_data_query = f"""
        SELECT * FROM events
        WHERE timestamp > '{last_processed}'
        ORDER BY timestamp
    """
    
    new_data = execute_query(new_data_query)
    
    # Process new data
    processed = process_data(new_data)
    
    # Append to existing results (not overwrite!)
    append_to_results(processed)
    
    # Update checkpoint
    if len(new_data) > 0:
        save_checkpoint('last_processed_timestamp', new_data['timestamp'].max())
    
    # Cost comparison:
    # Full reprocessing: Scan 1 TB every day
    # Incremental: Scan 10 GB per day (100x less)
    # Savings: 99% of processing costs
```

### Strategy 5: Data Lifecycle Management

```python
"""
DATA LIFECYCLE MANAGEMENT

Define rules for data retention and migration:

HOT TIER (Frequent access):
- Recent data (last 30 days)
- Active projects
- Cost: Highest storage, lowest access

WARM TIER (Occasional access):
- Older data (30-365 days)
- Historical analysis
- Cost: Medium storage, medium access

COLD TIER (Rare access):
- Archive (1-7 years)
- Compliance
- Cost: Low storage, high access

GLACIER/ARCHIVE (Almost never):
- Long-term retention (7+ years)
- Legal requirements
- Cost: Lowest storage, very high access

Example AWS S3 Lifecycle Policy:
"""

aws_lifecycle_policy = {
    "Rules": [
        {
            "Id": "MoveToIA",
            "Status": "Enabled",
            "Transitions": [
                {
                    "Days": 30,
                    "StorageClass": "STANDARD_IA"  # Infrequent Access
                },
                {
                    "Days": 90,
                    "StorageClass": "GLACIER"
                },
                {
                    "Days": 365,
                    "StorageClass": "DEEP_ARCHIVE"
                }
            ],
            "Expiration": {
                "Days": 2555  # 7 years, then delete
            }
        }
    ]
}

# Cost example for 1 TB data over 7 years:
print("\n1 TB Data Lifecycle Cost Comparison:")
print("\nOption 1: Keep all in S3 Standard")
print("  Monthly: $23.00")
print("  7 years: $1,932.00")

print("\nOption 2: Lifecycle management")
print("  30 days Standard: $23.00")
print("  60 days IA: $12.50")
print("  275 days Glacier: $4.00")
print("  ~6 years Deep Archive: $8.40")
print("  Total 7 years: ~$750.00")

print("\nSavings: $1,182.00 (61%)")
```

---

## Best Practices

### 1. Data Type Selection Checklist

```python
"""
CHOOSING DATA TYPES - CHECKLIST

INTEGER COLUMNS:
□ What's the range? (determines int8/16/32/64)
□ Are negatives possible? (signed vs unsigned)
□ Is it an ID? (consider string if alphanumeric)
□ Is it a count? (unsigned int is safer)

FLOAT COLUMNS:
□ How much precision needed? (float32 often enough)
□ Is it money? (use integer cents, not float)
□ Is it a ratio? (0-1 range, float32 sufficient)
□ Is it a measurement? (consider units and precision)

STRING COLUMNS:
□ How many unique values? (<50% → category)
□ Is it free text? (consider text analysis needs)
□ Is it an enum? (definitely category)
□ Is encoding important? (UTF-8 for flexibility)

DATETIME COLUMNS:
□ Need timezone? (datetime64[ns, tz])
□ Just date? (date type, 3 bytes vs 8)
□ Just time? (time type, 3 bytes vs 8)
□ Need milliseconds? (datetime64[ms] vs [ns])

BOOLEAN COLUMNS:
□ Really just True/False? (bool)
□ Nullable? (use Int8 with -1/0/1)
□ Part of flags? (consider bit packing)
"""

# Example implementation
def choose_optimal_dtype(series):
    """Recommend optimal dtype for a pandas Series"""
    
    if series.dtype == 'object':
        # Try to convert to numeric
        try:
            numeric = pd.to_numeric(series)
            return choose_optimal_dtype(numeric)
        except:
            pass
        
        # Check if categorical
        unique_ratio = series.nunique() / len(series)
        if unique_ratio < 0.5:
            return 'category'
        return 'object'
    
    elif series.dtype in ['int64', 'int32', 'int16', 'int8']:
        c_min = series.min()
        c_max = series.max()
        
        # Check if unsigned works
        if c_min >= 0:
            if c_max < 256:
                return 'uint8'
            elif c_max < 65536:
                return 'uint16'
            elif c_max < 4294967296:
                return 'uint32'
            else:
                return 'uint64'
        else:
            if c_min > -128 and c_max < 128:
                return 'int8'
            elif c_min > -32768 and c_max < 32768:
                return 'int16'
            elif c_min > -2147483648 and c_max < 2147483648:
                return 'int32'
            else:
                return 'int64'
    
    elif series.dtype == 'float64':
        c_min = series.min()
        c_max = series.max()
        if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
            return 'float32'
        return 'float64'
    
    return series.dtype

# Example usage
df = pd.DataFrame({
    'age': [25, 30, 35, 40],  # Can be uint8
    'income': [50000, 60000, 70000, 80000],  # Can be uint32
    'score': [0.85, 0.92, 0.78, 0.95],  # Can be float32
})

print("Recommended dtypes:")
for col in df.columns:
    optimal = choose_optimal_dtype(df[col])
    current = df[col].dtype
    print(f"{col}: {current} → {optimal}")
```

### 2. Storage Format Selection

```python
"""
STORAGE FORMAT SELECTION GUIDE

CSV:
✅ Use when: Human-readable needed, small datasets, simple data
❌ Avoid when: Large datasets, complex types, performance matters
Size: Large (no compression)
Speed: Slow (parsing required)

PARQUET:
✅ Use when: Large datasets, analytics, ML training data
❌ Avoid when: Need streaming writes, small files
Size: Small (columnar + compression)
Speed: Fast (no parsing, columnar reads)

FEATHER:
✅ Use when: Temporary storage, data exchange between Python/R
❌ Avoid when: Long-term storage, need compression
Size: Medium (minimal compression)
Speed: Very fast (memory-mapped)

HDF5:
✅ Use when: Scientific data, complex hierarchies, need partial reads
❌ Avoid when: Distributed systems, cloud storage
Size: Medium-Small
Speed: Fast (indexed access)

AVRO:
✅ Use when: Schema evolution needed, Kafka/Hadoop ecosystem
❌ Avoid when: Not in big data ecosystem
Size: Medium (row-based but compressed)
Speed: Medium

ORC:
✅ Use when: Hive/Hadoop ecosystem, heavy compression needed
❌ Avoid when: Outside Hadoop ecosystem
Size: Very small (best compression)
Speed: Fast (optimized for Hive)

RECOMMENDATION FOR ML:
Training data: PARQUET (best balance)
Inference data: FEATHER (fastest)
Logs: PARQUET or compressed JSON
Models: pickle/joblib or ONNX
"""

# Example: Save in different formats and compare
formats = {
    'csv': lambda df, path: df.to_csv(path, index=False),
    'parquet': lambda df, path: df.to_parquet(path),
    'feather': lambda df, path: df.to_feather(path),
    'pickle': lambda df, path: df.to_pickle(path),
}

def compare_formats(df, formats):
    """Compare different storage formats"""
    results = {}
    
    for format_name, save_func in formats.items():
        filepath = f'test.{format_name}'
        
        # Write
        import time
        start = time.time()
        save_func(df, filepath)
        write_time = time.time() - start
        
        # Size
        size = os.path.getsize(filepath) / 1024**2  # MB
        
        # Read
        start = time.time()
        if format_name == 'csv':
            pd.read_csv(filepath)
        elif format_name == 'parquet':
            pd.read_parquet(filepath)
        elif format_name == 'feather':
            pd.read_feather(filepath)
        elif format_name == 'pickle':
            pd.read_pickle(filepath)
        read_time = time.time() - start
        
        results[format_name] = {
            'size_mb': size,
            'write_time': write_time,
            'read_time': read_time
        }
        
        os.remove(filepath)
    
    return pd.DataFrame(results).T
```

### 3. Query Optimization

```python
"""
QUERY OPTIMIZATION FOR DATA COSTS

1. COLUMN SELECTION:
   ❌ Bad:  SELECT * FROM large_table
   ✅ Good: SELECT id, name FROM large_table
   
   For 1 TB table with 100 columns:
   SELECT *: Scan 1 TB
   SELECT 5 cols: Scan 50 GB
   Savings: 95% data scanned, 95% cost saved

2. PARTITIONING:
   ❌ Bad:  SELECT * FROM events
   ✅ Good: SELECT * FROM events WHERE date='2026-01-23'
   
   For 1 TB table partitioned by date (365 days):
   No filter: Scan 1 TB
   Date filter: Scan 2.7 GB
   Savings: 99.7% data scanned

3. FILTERING:
   ❌ Bad:  SELECT * FROM users WHERE UPPER(email) LIKE '%@GMAIL.COM'
   ✅ Good: SELECT * FROM users WHERE email LIKE '%@gmail.com'
   
   Function on column prevents index use!

4. AGGREGATION PUSHDOWN:
   ❌ Bad:  Read all data, then aggregate in Python
   ✅ Good: SELECT user_id, COUNT(*) FROM events GROUP BY user_id
   
   Let database do aggregation (faster, cheaper)

5. LIMIT EARLY:
   ❌ Bad:  SELECT * FROM large_table ORDER BY date DESC LIMIT 10
   ✅ Good: Use database LIMIT (don't fetch all then limit in code)
"""

# Example: Efficient querying with Pandas
def efficient_data_loading():
    """Examples of efficient data loading"""
    
    # BAD: Load everything
    # df = pd.read_parquet('large_dataset.parquet')
    # df = df[df['date'] >= '2026-01-01']
    
    # GOOD: Filter at load time
    df = pd.read_parquet(
        'large_dataset.parquet',
        filters=[('date', '>=', '2026-01-01')],
        columns=['id', 'date', 'value']  # Only needed columns
    )
    
    # BAD: Load all, then sample
    # df = pd.read_csv('huge.csv')
    # df = df.sample(10000)
    
    # GOOD: Sample at load time
    df = pd.read_csv('huge.csv', nrows=10000)
    
    # BAD: Load compressed file fully
    # import gzip
    # with gzip.open('data.gz', 'rt') as f:
    #     df = pd.read_csv(f)
    
    # GOOD: Let pandas handle compression
    df = pd.read_csv('data.csv.gz')  # Pandas auto-detects compression
```

### 4. Monitoring and Alerting

```python
"""
DATA COST MONITORING

Set up alerts for:
1. Storage growth rate
2. Query costs
3. Data transfer costs
4. Inefficient queries

Example AWS CloudWatch metrics to monitor:
- BucketSizeBytes (S3)
- NumberOfObjects (S3)
- AllRequests (S3)
- BytesDownloaded (S3)

Alert thresholds:
- Storage > expected by 20%
- Transfer > expected by 50%
- Large queries (> 1 TB scanned)
"""

# Example: Track storage growth
def track_storage_growth(storage_history):
    """Monitor storage growth and predict costs"""
    
    # Calculate growth rate
    df = pd.DataFrame(storage_history)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Daily growth
    df['growth_gb'] = df['size_gb'].diff()
    
    # Average daily growth
    avg_daily_growth = df['growth_gb'].mean()
    
    # Predict 30 days
    current_size = df['size_gb'].iloc[-1]
    predicted_size = current_size + (avg_daily_growth * 30)
    
    # Estimate cost
    predicted_cost = S3PricingCalculator.calculate_storage_cost(predicted_size)
    
    print(f"Current storage: {current_size:.2f} GB")
    print(f"Average daily growth: {avg_daily_growth:.2f} GB")
    print(f"Predicted in 30 days: {predicted_size:.2f} GB")
    print(f"Predicted monthly cost: ${predicted_cost:.2f}")
    
    # Alert if growth is concerning
    if avg_daily_growth > 10:  # More than 10 GB/day
        print("⚠️ WARNING: High storage growth rate!")
    
    return predicted_size, predicted_cost
```

---

## Interview Questions

### Question 1: Data Types and Memory

**Q: Why does Python's int take 28 bytes instead of 8?**

**A:**
Python integers are **objects** with significant overhead:
- Object header: 16 bytes (reference count, type pointer)
- Size info: 8 bytes (for arbitrary precision)
- Actual value: 4+ bytes

Python integers can be arbitrarily large (no overflow), which requires this overhead.

**For ML/DS work:**
- Use NumPy arrays instead of Python lists
- NumPy int64: exactly 8 bytes
- 1M integers: Python list = 28 MB, NumPy array = 7.6 MB

**Example:**
```python
# Python list
python_list = [1] * 1_000_000  # ~28 MB

# NumPy array
numpy_array = np.array([1] * 1_000_000, dtype=np.int64)  # 7.6 MB

# Savings: 73%
```

---

### Question 2: Storage Costs

**Q: Your company stores 10 million user images (average 2MB each). How would you optimize storage costs?**

**A:**

**Current situation:**
- 10M images × 2MB = 20 TB
- S3 cost: ~$460/month

**Optimization strategy:**

1. **Image Compression (Priority 1):**
   - Resize to max 1920x1080 (if not already)
   - Convert to WebP or JPEG (quality=90)
   - Expected: 70% size reduction
   - New size: 6 TB
   - New cost: $138/month
   - **Savings: $322/month ($3,864/year)**

2. **Lifecycle Policy (Priority 2):**
   - Identify access patterns
   - Move images not accessed in 90 days to S3 Infrequent Access
   - Move images not accessed in 365 days to Glacier
   - Expected: 40% of images rarely accessed
   - Additional savings: ~$50/month

3. **CDN Integration (Priority 3):**
   - Use CloudFront CDN
   - Cache frequently accessed images
   - Reduces S3 GET requests
   - Reduces data transfer costs
   - Expected: 80% reduction in S3 requests

4. **Deduplication (If applicable):**
   - Check for duplicate images
   - Store hash of each image
   - Use references instead of duplicates
   - Expected: 5-10% reduction (if duplicates exist)

**Total potential savings:**
- Storage: $322/month
- Lifecycle: $50/month
- Requests: $20/month
- **Total: ~$392/month ($4,704/year)**

---

### Question 3: Data Type Selection

**Q: You're designing a database for e-commerce. How would you store prices?**

**A:**

**❌ WRONG: Use FLOAT or DOUBLE**
```sql
CREATE TABLE products (
    id INT,
    price FLOAT  -- WRONG!
);
```

**Problems:**
- Floating point imprecision
- 0.1 + 0.2 = 0.30000000000000004
- Can't represent $0.10 exactly
- Rounding errors accumulate

**✅ CORRECT: Use DECIMAL or INTEGER cents**

**Option 1: DECIMAL**
```sql
CREATE TABLE products (
    id INT,
    price DECIMAL(10, 2)  -- 10 digits total, 2 after decimal
);
```
- Exact representation
- Max: $99,999,999.99
- Standard for financial data

**Option 2: INTEGER cents**
```sql
CREATE TABLE products (
    id INT,
    price_cents INT  -- Store in cents
);
```
- 12599 = $125.99
- Faster computations
- No decimal arithmetic
- More storage efficient
- Must remember to divide by 100 for display

**Recommendation:** 
- Use DECIMAL for clarity
- Use INTEGER cents for performance at scale
- Never use FLOAT for money!

---

### Question 4: Compression

**Q: When would you use compression? What are the tradeoffs?**

**A:**

**Use compression when:**
1. **Storage costs matter** (almost always in production)
2. **I/O is bottleneck** (compression reduces I/O)
3. **Network transfer needed** (compress before sending)
4. **Data is compressible** (text, logs, not already compressed)

**Don't use compression when:**
1. **CPU is bottleneck** (compression uses CPU)
2. **Need random access** (compressed data must be decompressed)
3. **Data already compressed** (images, videos, already compressed files)
4. **Real-time requirements** (decompression adds latency)

**Tradeoffs:**

| Aspect | Uncompressed | Compressed |
|--------|-------------|------------|
| Storage | High | Low |
| I/O Speed | Slower (more data) | Faster (less data) |
| CPU | Lower | Higher |
| Random Access | Fast | Slow |

**Example scenario:**
```
Dataset: 1 TB of JSON logs
Access pattern: Sequential reads for analysis

Uncompressed:
- Storage: 1 TB @ $23/month = $23
- Read time: 100 seconds @ 10 GB/s = 100s
- CPU: Low

Compressed (GZIP 5:1 ratio):
- Storage: 200 GB @ $23/month = $4.60
- Read time: 20s transfer + 15s decompress = 35s
- CPU: Medium
- Savings: $18.40/month, 65% faster

Recommendation: Compress (saves money AND time)
```

**Modern best practice:**
- Use column-oriented formats (Parquet) with compression
- Compression is built-in and efficient
- Usually win-win (storage + speed)

---

### Question 5: Query Optimization

**Q: How do you optimize queries to reduce cloud storage costs?**

**A:**

**Key principles:**

1. **Column Pruning**
   ```python
   # BAD: Scan 1 TB
   df = pd.read_parquet('data/')
   
   # GOOD: Scan 100 GB (if 10 of 100 columns)
   df = pd.read_parquet('data/', columns=['id', 'date', 'value'])
   ```
   **Cost impact:** Google BigQuery, AWS Athena charge per TB scanned

2. **Partition Filtering**
   ```python
   # BAD: Scan all data
   df = pd.read_parquet('data/')
   df = df[df['date'] == '2026-01-23']
   
   # GOOD: Only scan relevant partition
   df = pd.read_parquet('data/', 
                        filters=[('date', '=', '2026-01-23')])
   ```
   **Cost impact:** 365x reduction for daily partitions

3. **Aggregation Pushdown**
   ```sql
   -- BAD: Transfer all data, then aggregate
   SELECT * FROM events;  -- In application: group by user_id
   
   -- GOOD: Aggregate in database
   SELECT user_id, COUNT(*) 
   FROM events 
   GROUP BY user_id;
   ```
   **Cost impact:** Reduce data transfer by 1000x+

4. **Query Result Caching**
   - Cache frequently run queries
   - Many cloud services offer automatic caching
   - Subsequent runs: free!

**Real example:**
```
BigQuery query:
SELECT user_id, date, SUM(amount) 
FROM transactions
WHERE date >= '2026-01-01'
GROUP BY user_id, date

Without optimization:
- Scans: 10 TB
- Cost: $50 (BigQuery $5/TB)

With optimization:
- Partition filter: Only scan Q1 data (2.5 TB)
- Column selection: Only needed columns (1.25 TB)
- Cost: $6.25
- Savings: $43.75 per query

If run 100 times/month: $4,375/month savings!
```

---

## Summary

### Key Takeaways

**1. Data Types Matter**
- int8 vs int64: 8x memory difference
- float32 vs float64: 2x memory difference
- category vs object: 10-100x memory difference
- Choose smallest type that fits your data

**2. Small Inefficiencies Scale**
- 10 bytes per user × 10M users = 100 MB
- But with overhead: can become 1 GB+
- Repeated data: multiplies the problem
- File system overhead: minimum block size

**3. Cloud Storage Costs**
- Storage: ~$0.02/GB/month (standard)
- Requests: $0.0004-0.005 per 1,000
- Transfer: $0.05-0.12/GB
- Different tiers offer 50-95% savings

**4. Optimization Strategies**
- Compression: 50-90% reduction
- Right data types: 50-87% reduction
- Partitioning: Query only what's needed
- Lifecycle policies: 60-95% savings
- **Combined: 95%+ total reduction possible**

**5. Cost vs Performance**
- Best compression: slower, cheaper storage
- No compression: faster, expensive storage
- Modern formats (Parquet): best of both
- Choose based on access patterns

### Decision Matrix

| Scenario | Storage Format | Compression | Data Types | Partitioning |
|----------|---------------|-------------|------------|--------------|
| **ML Training Data** | Parquet | Snappy | float32 | By date |
| **Real-time Logs** | Parquet | LZ4 | Optimized | By hour |
| **Archive Data** | Parquet | GZIP | Any | By month |
| **Time Series** | Parquet | Snappy | int32/float32 | By date |
| **Images** | JPEG/WebP | Quality=85 | uint8 | By category |
| **Text/JSON** | Parquet | GZIP | category | By source |

### Cost Optimization Checklist

**Before going to production:**
- [ ] Analyzed data types (no float64 for integers)
- [ ] Tested compression (found best ratio/speed)
- [ ] Implemented partitioning (by date/category)
- [ ] Set up lifecycle policies (move old data to cheaper tier)
- [ ] Optimized queries (column pruning, filtering)
- [ ] Removed redundant data (normalized where appropriate)
- [ ] Compressed images (resized, appropriate format)
- [ ] Set up monitoring (track growth and costs)
- [ ] Documented decisions (why each choice was made)
- [ ] Load tested (verified performance meets requirements)

---

**End of Data Management Guide** 💾

**Key Numbers to Remember:**
- 1 MB = 1,048,576 bytes
- int64: 8 bytes, int32: 4 bytes, int8: 1 byte
- S3 Standard: ~$0.023/GB/month
- Compression: typically 2-10x reduction
- Parquet vs CSV: 5-10x smaller, 10-100x faster reads

Good luck optimizing your data pipelines! 🚀
