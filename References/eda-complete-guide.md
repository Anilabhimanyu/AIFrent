# Exploratory Data Analysis (EDA) - Complete Guide

> **Complete reference for EDA, data preprocessing, feature scaling, and data analysis for machine learning interviews (3 YOE)**

---

## Table of Contents

1. [Introduction to EDA](#introduction-to-eda)
2. [Initial Data Understanding](#initial-data-understanding)
3. [Data Quality Checks](#data-quality-checks)
4. [Univariate Analysis](#univariate-analysis)
5. [Bivariate Analysis](#bivariate-analysis)
6. [Multivariate Analysis](#multivariate-analysis)
7. [Handling Missing Values](#handling-missing-values)
8. [Handling Outliers](#handling-outliers)
9. [Feature Scaling](#feature-scaling)
10. [Feature Encoding](#feature-encoding)
11. [Feature Engineering](#feature-engineering)
12. [Data Transformation](#data-transformation)
13. [Common Mistakes](#common-mistakes)
14. [Interview Questions](#interview-questions)

---

## Introduction to EDA

### What is EDA?

**Exploratory Data Analysis (EDA)** is the process of analyzing and understanding datasets before building machine learning models.

**Goals of EDA:**
- ✅ Understand data structure and characteristics
- ✅ Identify patterns and relationships
- ✅ Detect anomalies and outliers
- ✅ Check data quality issues
- ✅ Formulate hypotheses
- ✅ Guide feature engineering
- ✅ Select appropriate models

**Why EDA is Critical:**
- Garbage In = Garbage Out
- Prevents building models on bad data
- Reveals insights for feature engineering
- Helps choose right algorithms
- Saves time debugging later

### EDA Workflow

```
1. Initial Data Loading
   ↓
2. Basic Information (shape, types, memory)
   ↓
3. Statistical Summary
   ↓
4. Missing Values Analysis
   ↓
5. Univariate Analysis (single features)
   ↓
6. Bivariate Analysis (feature pairs)
   ↓
7. Multivariate Analysis (multiple features)
   ↓
8. Outlier Detection
   ↓
9. Correlation Analysis
   ↓
10. Feature Engineering
   ↓
11. Data Preprocessing
   ↓
12. Ready for Modeling
```

### Essential Libraries

```python
# Data manipulation
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Statistical analysis
from scipy import stats
from scipy.stats import skew, kurtosis

# Machine learning preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.model_selection import train_test_split

# Warnings
import warnings
warnings.filterwarnings('ignore')

# Display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
plt.style.use('seaborn-v0_8-darkgrid')
```

---

## Initial Data Understanding

### Step 1: Load Data

```python
# Load data
df = pd.read_csv('data.csv')

# Alternative formats
df = pd.read_excel('data.xlsx')
df = pd.read_json('data.json')
df = pd.read_sql('SELECT * FROM table', connection)

# Load sample for large datasets
df = pd.read_csv('large_data.csv', nrows=10000)
```

### Step 2: First Look at Data

```python
# Display first rows
print("First 5 rows:")
print(df.head())

print("\nLast 5 rows:")
print(df.tail())

# Random sample
print("\nRandom 5 rows:")
print(df.sample(5))
```

### Step 3: Basic Information

```python
# Dataset shape
print(f"Dataset shape: {df.shape}")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

# Column names
print(f"\nColumn names: {df.columns.tolist()}")

# Data types
print("\nData types:")
print(df.dtypes)

# Memory usage
print(f"\nMemory usage:")
print(df.memory_usage(deep=True))
print(f"Total memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Concise summary
print("\nDataset info:")
df.info()
```

### Step 4: Statistical Summary

```python
# Numerical features
print("Numerical features summary:")
print(df.describe())

# Include all percentiles
print("\nDetailed percentiles:")
print(df.describe(percentiles=[.01, .05, .25, .50, .75, .95, .99]))

# Categorical features
print("\nCategorical features summary:")
print(df.describe(include=['object']))

# All features
print("\nAll features summary:")
print(df.describe(include='all'))
```

### Step 5: Identify Feature Types

```python
# Separate numerical and categorical
numerical_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = df.select_dtypes(include=['object', 'category']).columns.tolist()
datetime_features = df.select_dtypes(include=['datetime64']).columns.tolist()

print(f"Numerical features ({len(numerical_features)}): {numerical_features}")
print(f"Categorical features ({len(categorical_features)}): {categorical_features}")
print(f"Datetime features ({len(datetime_features)}): {datetime_features}")

# Check for boolean features
boolean_features = [col for col in df.columns if df[col].nunique() == 2]
print(f"Boolean features ({len(boolean_features)}): {boolean_features}")
```

---

## Data Quality Checks

### Check 1: Missing Values

```python
# Count missing values
missing = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100

missing_df = pd.DataFrame({
    'Feature': df.columns,
    'Missing_Count': missing.values,
    'Missing_Percent': missing_percent.values
}).sort_values('Missing_Percent', ascending=False)

print("Missing values:")
print(missing_df[missing_df['Missing_Count'] > 0])

# Visualize missing values
plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap='viridis')
plt.title('Missing Values Heatmap')
plt.tight_layout()
plt.show()

# Missing value patterns
import missingno as mno
mno.matrix(df)
plt.show()
```

### Check 2: Duplicate Rows

```python
# Check duplicates
duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}")

if duplicates > 0:
    print("\nDuplicate rows:")
    print(df[df.duplicated(keep=False)])
    
    # Remove duplicates
    df_clean = df.drop_duplicates()
    print(f"Rows after removing duplicates: {len(df_clean)}")
```

### Check 3: Data Types Consistency

```python
# Check for mixed types
for col in df.columns:
    # Check if column has mixed types
    types = df[col].apply(type).unique()
    if len(types) > 1:
        print(f"Column '{col}' has mixed types: {types}")

# Check numeric columns stored as object
for col in df.select_dtypes(include=['object']).columns:
    try:
        pd.to_numeric(df[col])
        print(f"Column '{col}' can be converted to numeric")
    except:
        pass
```

### Check 4: Unique Values

```python
# Check unique values for each column
print("Unique values per column:")
for col in df.columns:
    n_unique = df[col].nunique()
    print(f"{col}: {n_unique} unique values")
    
    # Show values if few unique
    if n_unique <= 10:
        print(f"  Values: {df[col].unique()}")
```

### Check 5: Constant and Quasi-Constant Features

```python
# Constant features (same value for all rows)
constant_features = [col for col in df.columns if df[col].nunique() == 1]
print(f"Constant features: {constant_features}")

# Quasi-constant features (>99% same value)
quasi_constant_features = []
for col in df.columns:
    if df[col].value_counts().iloc[0] / len(df) > 0.99:
        quasi_constant_features.append(col)

print(f"Quasi-constant features (>99% same): {quasi_constant_features}")
```

### Check 6: Target Variable Distribution

```python
# For classification
target = 'target_column'

print("Target distribution:")
print(df[target].value_counts())
print("\nTarget distribution (%):")
print(df[target].value_counts(normalize=True) * 100)

# Visualize
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
df[target].value_counts().plot(kind='bar')
plt.title('Target Distribution (Count)')
plt.xlabel('Class')
plt.ylabel('Count')

plt.subplot(1, 2, 2)
df[target].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Target Distribution (%)')
plt.ylabel('')

plt.tight_layout()
plt.show()

# Check for class imbalance
class_distribution = df[target].value_counts()
imbalance_ratio = class_distribution.max() / class_distribution.min()
print(f"\nClass imbalance ratio: {imbalance_ratio:.2f}")

if imbalance_ratio > 3:
    print("⚠️ WARNING: Significant class imbalance detected!")
```

---

## Univariate Analysis

### Analysis 1: Numerical Features

```python
# Distribution analysis
def analyze_numerical_feature(df, column):
    """Comprehensive analysis of numerical feature"""
    
    print(f"\n{'='*60}")
    print(f"Analysis of: {column}")
    print(f"{'='*60}")
    
    # Basic statistics
    print("\nBasic Statistics:")
    print(f"  Count: {df[column].count()}")
    print(f"  Mean: {df[column].mean():.2f}")
    print(f"  Median: {df[column].median():.2f}")
    print(f"  Std: {df[column].std():.2f}")
    print(f"  Min: {df[column].min():.2f}")
    print(f"  Max: {df[column].max():.2f}")
    print(f"  Range: {df[column].max() - df[column].min():.2f}")
    print(f"  Skewness: {df[column].skew():.2f}")
    print(f"  Kurtosis: {df[column].kurtosis():.2f}")
    
    # Missing values
    missing = df[column].isnull().sum()
    print(f"  Missing: {missing} ({missing/len(df)*100:.2f}%)")
    
    # Zeros
    zeros = (df[column] == 0).sum()
    print(f"  Zeros: {zeros} ({zeros/len(df)*100:.2f}%)")
    
    # Unique values
    print(f"  Unique values: {df[column].nunique()}")
    
    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Histogram
    axes[0, 0].hist(df[column].dropna(), bins=50, edgecolor='black')
    axes[0, 0].axvline(df[column].mean(), color='red', linestyle='--', label='Mean')
    axes[0, 0].axvline(df[column].median(), color='green', linestyle='--', label='Median')
    axes[0, 0].set_title(f'{column} - Histogram')
    axes[0, 0].set_xlabel(column)
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].legend()
    
    # Box plot
    axes[0, 1].boxplot(df[column].dropna())
    axes[0, 1].set_title(f'{column} - Box Plot')
    axes[0, 1].set_ylabel(column)
    
    # Q-Q plot (normality check)
    stats.probplot(df[column].dropna(), dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title(f'{column} - Q-Q Plot')
    
    # Violin plot
    axes[1, 1].violinplot(df[column].dropna(), vert=True)
    axes[1, 1].set_title(f'{column} - Violin Plot')
    axes[1, 1].set_ylabel(column)
    
    plt.tight_layout()
    plt.show()
    
    # Interpretation
    print("\nInterpretation:")
    
    # Skewness
    skewness = df[column].skew()
    if abs(skewness) < 0.5:
        print("  ✅ Distribution is fairly symmetric")
    elif skewness > 0.5:
        print(f"  ⚠️ Right-skewed (positive skew: {skewness:.2f})")
        print("     → Consider log transformation")
    else:
        print(f"  ⚠️ Left-skewed (negative skew: {skewness:.2f})")
    
    # Kurtosis
    kurt = df[column].kurtosis()
    if abs(kurt) < 1:
        print("  ✅ Normal tail weight")
    elif kurt > 1:
        print(f"  ⚠️ Heavy tails (kurtosis: {kurt:.2f})")
        print("     → Possible outliers")
    else:
        print(f"  ⚠️ Light tails (kurtosis: {kurt:.2f})")

# Analyze all numerical features
for col in numerical_features[:3]:  # First 3 as example
    analyze_numerical_feature(df, col)
```

### Analysis 2: Categorical Features

```python
def analyze_categorical_feature(df, column):
    """Comprehensive analysis of categorical feature"""
    
    print(f"\n{'='*60}")
    print(f"Analysis of: {column}")
    print(f"{'='*60}")
    
    # Basic statistics
    print("\nBasic Statistics:")
    print(f"  Count: {df[column].count()}")
    print(f"  Unique values: {df[column].nunique()}")
    print(f"  Most common: {df[column].mode()[0]}")
    print(f"  Missing: {df[column].isnull().sum()} ({df[column].isnull().sum()/len(df)*100:.2f}%)")
    
    # Value counts
    print("\nValue Counts:")
    value_counts = df[column].value_counts()
    value_percent = df[column].value_counts(normalize=True) * 100
    
    for val, count, pct in zip(value_counts.index[:10], value_counts.values[:10], value_percent.values[:10]):
        print(f"  {val}: {count} ({pct:.2f}%)")
    
    if len(value_counts) > 10:
        print(f"  ... and {len(value_counts) - 10} more categories")
    
    # Visualizations
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Bar plot (top 20)
    top_categories = value_counts.head(20)
    axes[0].barh(range(len(top_categories)), top_categories.values)
    axes[0].set_yticks(range(len(top_categories)))
    axes[0].set_yticklabels(top_categories.index)
    axes[0].set_xlabel('Count')
    axes[0].set_title(f'{column} - Top 20 Categories')
    axes[0].invert_yaxis()
    
    # Pie chart (top 10)
    if len(value_counts) <= 10:
        axes[1].pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
    else:
        top_10 = value_counts.head(10)
        other = value_counts.iloc[10:].sum()
        values = list(top_10.values) + [other]
        labels = list(top_10.index) + ['Others']
        axes[1].pie(values, labels=labels, autopct='%1.1f%%')
    
    axes[1].set_title(f'{column} - Distribution')
    
    plt.tight_layout()
    plt.show()
    
    # Interpretation
    print("\nInterpretation:")
    
    # High cardinality
    if df[column].nunique() > 50:
        print(f"  ⚠️ High cardinality ({df[column].nunique()} categories)")
        print("     → Consider grouping or target encoding")
    
    # Dominant category
    dominant_pct = value_percent.iloc[0]
    if dominant_pct > 90:
        print(f"  ⚠️ Dominant category: {dominant_pct:.1f}%")
        print("     → Feature may not be useful")
    
    # Rare categories
    rare_categories = (value_counts < 10).sum()
    if rare_categories > 0:
        print(f"  ⚠️ {rare_categories} rare categories (<10 occurrences)")
        print("     → Consider grouping into 'Other'")

# Analyze all categorical features
for col in categorical_features[:2]:  # First 2 as example
    analyze_categorical_feature(df, col)
```

### Distribution Shapes

```python
# Plot all numerical distributions
n_cols = 3
n_rows = (len(numerical_features) + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
axes = axes.flatten()

for idx, col in enumerate(numerical_features):
    df[col].hist(bins=50, ax=axes[idx], edgecolor='black')
    axes[idx].set_title(f'{col}')
    axes[idx].set_xlabel('Value')
    axes[idx].set_ylabel('Frequency')
    
    # Add mean and median lines
    axes[idx].axvline(df[col].mean(), color='red', linestyle='--', alpha=0.7, label='Mean')
    axes[idx].axvline(df[col].median(), color='green', linestyle='--', alpha=0.7, label='Median')
    axes[idx].legend()

# Hide empty subplots
for idx in range(len(numerical_features), len(axes)):
    axes[idx].axis('off')

plt.tight_layout()
plt.show()
```

---

## Bivariate Analysis

### Analysis 1: Numerical vs Numerical

```python
# Scatter plots
def scatter_with_regression(df, x, y, hue=None):
    """Scatter plot with regression line"""
    plt.figure(figsize=(10, 6))
    
    if hue:
        for category in df[hue].unique():
            mask = df[hue] == category
            plt.scatter(df[mask][x], df[mask][y], label=category, alpha=0.6)
    else:
        plt.scatter(df[x], df[y], alpha=0.6)
    
    # Regression line
    z = np.polyfit(df[x].dropna(), df[y].dropna(), 1)
    p = np.poly1d(z)
    plt.plot(df[x], p(df[x]), "r--", alpha=0.8, label='Regression line')
    
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f'{x} vs {y}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Correlation
    corr = df[x].corr(df[y])
    print(f"Correlation between {x} and {y}: {corr:.3f}")

# Example
scatter_with_regression(df, 'feature1', 'feature2', hue='target')
```

### Analysis 2: Numerical vs Categorical

```python
# Box plots by category
def boxplot_by_category(df, numerical_col, categorical_col):
    """Box plot for numerical feature grouped by category"""
    
    plt.figure(figsize=(12, 6))
    
    # Sort by median
    order = df.groupby(categorical_col)[numerical_col].median().sort_values().index
    
    sns.boxplot(data=df, x=categorical_col, y=numerical_col, order=order)
    plt.xticks(rotation=45, ha='right')
    plt.title(f'{numerical_col} by {categorical_col}')
    plt.tight_layout()
    plt.show()
    
    # Statistical test (ANOVA)
    categories = df[categorical_col].unique()
    groups = [df[df[categorical_col] == cat][numerical_col].dropna() for cat in categories]
    
    from scipy.stats import f_oneway
    statistic, p_value = f_oneway(*groups)
    
    print(f"\nANOVA Test:")
    print(f"  F-statistic: {statistic:.4f}")
    print(f"  P-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("  ✅ Significant difference between groups")
    else:
        print("  ❌ No significant difference between groups")

# Example
boxplot_by_category(df, 'numerical_feature', 'categorical_feature')
```

### Analysis 3: Categorical vs Categorical

```python
# Contingency table and chi-square test
def categorical_relationship(df, col1, col2):
    """Analyze relationship between two categorical features"""
    
    # Contingency table
    contingency = pd.crosstab(df[col1], df[col2])
    print("Contingency Table:")
    print(contingency)
    
    # Normalized
    print("\nNormalized (%):")
    print(pd.crosstab(df[col1], df[col2], normalize='index') * 100)
    
    # Chi-square test
    from scipy.stats import chi2_contingency
    chi2, p_value, dof, expected = chi2_contingency(contingency)
    
    print(f"\nChi-Square Test:")
    print(f"  Chi2 statistic: {chi2:.4f}")
    print(f"  P-value: {p_value:.4f}")
    print(f"  Degrees of freedom: {dof}")
    
    if p_value < 0.05:
        print("  ✅ Features are dependent (related)")
    else:
        print("  ❌ Features are independent (not related)")
    
    # Heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(contingency, annot=True, fmt='d', cmap='YlOrRd')
    plt.title(f'{col1} vs {col2}')
    plt.tight_layout()
    plt.show()

# Example
categorical_relationship(df, 'category1', 'category2')
```

### Analysis 4: Feature vs Target

```python
# For classification target
def feature_target_analysis(df, feature, target):
    """Analyze relationship between feature and target"""
    
    if df[feature].dtype in ['int64', 'float64']:
        # Numerical feature
        plt.figure(figsize=(15, 5))
        
        # Distribution by target
        plt.subplot(1, 3, 1)
        for target_class in df[target].unique():
            df[df[target] == target_class][feature].hist(bins=30, alpha=0.5, label=f'Class {target_class}')
        plt.xlabel(feature)
        plt.ylabel('Frequency')
        plt.title(f'{feature} Distribution by Target')
        plt.legend()
        
        # Box plot by target
        plt.subplot(1, 3, 2)
        df.boxplot(column=feature, by=target)
        plt.suptitle('')
        plt.title(f'{feature} by Target')
        
        # Violin plot
        plt.subplot(1, 3, 3)
        sns.violinplot(data=df, x=target, y=feature)
        plt.title(f'{feature} by Target')
        
        plt.tight_layout()
        plt.show()
        
        # Statistical test
        groups = [df[df[target] == cls][feature].dropna() for cls in df[target].unique()]
        statistic, p_value = f_oneway(*groups)
        
        print(f"ANOVA p-value: {p_value:.4f}")
        if p_value < 0.05:
            print("✅ Feature is significantly different across target classes")
        else:
            print("❌ No significant difference")
    
    else:
        # Categorical feature
        contingency = pd.crosstab(df[feature], df[target], normalize='index') * 100
        
        plt.figure(figsize=(12, 6))
        contingency.plot(kind='bar', stacked=False)
        plt.xlabel(feature)
        plt.ylabel('Percentage')
        plt.title(f'{feature} vs Target')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title=target)
        plt.tight_layout()
        plt.show()

# Analyze all features vs target
for feature in df.columns:
    if feature != 'target':
        feature_target_analysis(df, feature, 'target')
```

---

## Multivariate Analysis

### Correlation Analysis

```python
# Correlation matrix for numerical features
correlation_matrix = df[numerical_features].corr()

# Heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()

# Find highly correlated pairs
def find_high_correlations(df, threshold=0.8):
    """Find feature pairs with high correlation"""
    corr_matrix = df.corr().abs()
    
    # Upper triangle (avoid duplicates)
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    # Find features with correlation > threshold
    high_corr = [(column, row, corr_matrix.loc[row, column]) 
                 for column in upper.columns 
                 for row in upper.index 
                 if upper.loc[row, column] > threshold]
    
    if high_corr:
        print(f"\nHighly correlated pairs (|r| > {threshold}):")
        for feat1, feat2, corr in sorted(high_corr, key=lambda x: abs(x[2]), reverse=True):
            print(f"  {feat1} <-> {feat2}: {corr:.3f}")
            print("    → Consider removing one feature")
    else:
        print(f"\nNo highly correlated pairs found (threshold = {threshold})")

find_high_correlations(df[numerical_features], threshold=0.8)
```

### Pair Plot

```python
# Pair plot for subset of features
selected_features = numerical_features[:5]  # First 5 features

sns.pairplot(df[selected_features + ['target']], hue='target', diag_kind='kde')
plt.suptitle('Pair Plot', y=1.01)
plt.tight_layout()
plt.show()
```

### Principal Component Analysis (PCA)

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[numerical_features])

# Apply PCA
pca = PCA()
pca.fit(X_scaled)

# Explained variance
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Scree plot
axes[0].bar(range(1, len(explained_variance) + 1), explained_variance)
axes[0].set_xlabel('Principal Component')
axes[0].set_ylabel('Explained Variance Ratio')
axes[0].set_title('Scree Plot')

# Cumulative variance
axes[1].plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o')
axes[1].axhline(y=0.95, color='r', linestyle='--', label='95% variance')
axes[1].set_xlabel('Number of Components')
axes[1].set_ylabel('Cumulative Explained Variance')
axes[1].set_title('Cumulative Explained Variance')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.show()

# Number of components for 95% variance
n_components_95 = np.argmax(cumulative_variance >= 0.95) + 1
print(f"\nComponents needed for 95% variance: {n_components_95}/{len(numerical_features)}")
```

---

## Handling Missing Values

### Missing Value Strategies

```python
# Analyze missing patterns
def analyze_missing_patterns(df):
    """Analyze patterns in missing data"""
    
    missing_counts = df.isnull().sum()
    missing_cols = missing_counts[missing_counts > 0].index
    
    if len(missing_cols) == 0:
        print("✅ No missing values found")
        return
    
    print(f"Features with missing values: {len(missing_cols)}")
    
    # Missing value correlation
    missing_matrix = df[missing_cols].isnull().astype(int)
    missing_corr = missing_matrix.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(missing_corr, annot=True, fmt='.2f', cmap='coolwarm', center=0)
    plt.title('Correlation Between Missing Values')
    plt.tight_layout()
    plt.show()
    
    # Check if missing values are related to target
    if 'target' in df.columns:
        for col in missing_cols:
            df_copy = df.copy()
            df_copy[f'{col}_missing'] = df_copy[col].isnull().astype(int)
            
            print(f"\n{col} - Missing vs Target:")
            print(df_copy.groupby(f'{col}_missing')['target'].mean())

analyze_missing_patterns(df)
```

### Strategy 1: Deletion

```python
# 1. Remove rows with missing values
df_dropped_rows = df.dropna()
print(f"Rows before: {len(df)}, after: {len(df_dropped_rows)}")

# 2. Remove columns with too many missing values
threshold = 0.5  # 50%
df_dropped_cols = df.loc[:, df.isnull().mean() < threshold]
print(f"Columns before: {len(df.columns)}, after: {len(df_dropped_cols.columns)}")

# When to use deletion:
# ✅ < 5% missing values
# ✅ Missing completely at random (MCAR)
# ✅ Large dataset
# ❌ Small dataset
# ❌ Missing not at random (MNAR)
```

### Strategy 2: Simple Imputation

```python
from sklearn.impute import SimpleImputer

# Mean imputation (numerical)
imputer_mean = SimpleImputer(strategy='mean')
df_mean = df.copy()
df_mean[numerical_features] = imputer_mean.fit_transform(df[numerical_features])

# Median imputation (numerical, robust to outliers)
imputer_median = SimpleImputer(strategy='median')
df_median = df.copy()
df_median[numerical_features] = imputer_median.fit_transform(df[numerical_features])

# Mode imputation (categorical)
imputer_mode = SimpleImputer(strategy='most_frequent')
df_mode = df.copy()
df_mode[categorical_features] = imputer_mode.fit_transform(df[categorical_features])

# Constant imputation
imputer_constant = SimpleImputer(strategy='constant', fill_value=0)

# When to use:
# Mean: Normal distribution, no outliers
# Median: Skewed distribution, outliers present
# Mode: Categorical features
# Constant: When 0 or specific value makes sense
```

### Strategy 3: Advanced Imputation

```python
# KNN Imputation
from sklearn.impute import KNNImputer

knn_imputer = KNNImputer(n_neighbors=5)
df_knn = df.copy()
df_knn[numerical_features] = knn_imputer.fit_transform(df[numerical_features])

# Iterative Imputation (MICE)
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

iter_imputer = IterativeImputer(max_iter=10, random_state=42)
df_iter = df.copy()
df_iter[numerical_features] = iter_imputer.fit_transform(df[numerical_features])

# Forward/Backward fill (time series)
df_ffill = df.fillna(method='ffill')  # Forward fill
df_bfill = df.fillna(method='bfill')  # Backward fill

# Interpolation (time series)
df_interp = df.interpolate(method='linear')

# When to use:
# KNN: Features are related, moderate missing %
# Iterative: Multiple related features with missing
# Forward/Backward fill: Time series data
# Interpolation: Time series with smooth trends
```

### Strategy 4: Create Missing Indicator

```python
# Add indicator column for missing values
for col in df.columns:
    if df[col].isnull().sum() > 0:
        df[f'{col}_missing'] = df[col].isnull().astype(int)

# This preserves information that value was missing
# Useful when missingness is informative
```

### Comparison of Imputation Methods

```python
def compare_imputation_methods(df, target_col, feature_col):
    """Compare different imputation methods"""
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score
    
    # Create datasets with different imputations
    methods = {
        'Drop': df.dropna(subset=[feature_col]),
        'Mean': df.copy(),
        'Median': df.copy(),
        'KNN': df.copy()
    }
    
    # Impute
    methods['Mean'][feature_col] = methods['Mean'][feature_col].fillna(methods['Mean'][feature_col].mean())
    methods['Median'][feature_col] = methods['Median'][feature_col].fillna(methods['Median'][feature_col].median())
    
    knn_imp = KNNImputer()
    methods['KNN'][[feature_col]] = knn_imp.fit_transform(methods['KNN'][[feature_col]])
    
    # Evaluate with simple model
    results = {}
    for method_name, data in methods.items():
        X = data[[feature_col]]
        y = data[target_col]
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        scores = cross_val_score(model, X, y, cv=5)
        results[method_name] = scores.mean()
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.bar(results.keys(), results.values())
    plt.xlabel('Imputation Method')
    plt.ylabel('Cross-Validation Score')
    plt.title(f'Comparison of Imputation Methods for {feature_col}')
    plt.ylim([0, 1])
    plt.tight_layout()
    plt.show()
    
    print("\nImputation Method Scores:")
    for method, score in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f"  {method}: {score:.4f}")

# Example usage
# compare_imputation_methods(df, 'target', 'feature_with_missing')
```

---

## Handling Outliers

### Outlier Detection Methods

```python
def detect_outliers_comprehensive(df, column):
    """Detect outliers using multiple methods"""
    
    data = df[column].dropna()
    
    print(f"\n{'='*60}")
    print(f"Outlier Detection for: {column}")
    print(f"{'='*60}")
    
    # Method 1: Z-Score
    z_scores = np.abs(stats.zscore(data))
    outliers_zscore = data[z_scores > 3]
    print(f"\n1. Z-Score Method (|z| > 3):")
    print(f"   Outliers: {len(outliers_zscore)} ({len(outliers_zscore)/len(data)*100:.2f}%)")
    
    # Method 2: IQR
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_iqr = data[(data < lower_bound) | (data > upper_bound)]
    print(f"\n2. IQR Method (1.5 * IQR):")
    print(f"   Lower bound: {lower_bound:.2f}")
    print(f"   Upper bound: {upper_bound:.2f}")
    print(f"   Outliers: {len(outliers_iqr)} ({len(outliers_iqr)/len(data)*100:.2f}%)")
    
    # Method 3: Modified Z-Score (robust)
    median = data.median()
    mad = np.median(np.abs(data - median))
    modified_z_scores = 0.6745 * (data - median) / mad
    outliers_modified_z = data[np.abs(modified_z_scores) > 3.5]
    print(f"\n3. Modified Z-Score Method (MAD):")
    print(f"   Outliers: {len(outliers_modified_z)} ({len(outliers_modified_z)/len(data)*100:.2f}%)")
    
    # Method 4: Isolation Forest
    from sklearn.ensemble import IsolationForest
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    outliers_iso = iso_forest.fit_predict(data.values.reshape(-1, 1))
    outliers_iso_count = (outliers_iso == -1).sum()
    print(f"\n4. Isolation Forest:")
    print(f"   Outliers: {outliers_iso_count} ({outliers_iso_count/len(data)*100:.2f}%)")
    
    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Box plot with outliers
    axes[0, 0].boxplot(data)
    axes[0, 0].set_title(f'{column} - Box Plot')
    axes[0, 0].set_ylabel('Value')
    
    # Histogram with bounds
    axes[0, 1].hist(data, bins=50, edgecolor='black')
    axes[0, 1].axvline(lower_bound, color='red', linestyle='--', label='IQR Lower')
    axes[0, 1].axvline(upper_bound, color='red', linestyle='--', label='IQR Upper')
    axes[0, 1].set_title(f'{column} - Histogram')
    axes[0, 1].legend()
    
    # Scatter plot with index
    axes[1, 0].scatter(range(len(data)), data, alpha=0.5)
    axes[1, 0].axhline(lower_bound, color='red', linestyle='--', alpha=0.7)
    axes[1, 0].axhline(upper_bound, color='red', linestyle='--', alpha=0.7)
    axes[1, 0].set_title(f'{column} - Scatter Plot')
    axes[1, 0].set_xlabel('Index')
    axes[1, 0].set_ylabel('Value')
    
    # Z-score plot
    axes[1, 1].scatter(range(len(z_scores)), z_scores, alpha=0.5)
    axes[1, 1].axhline(3, color='red', linestyle='--', label='Threshold')
    axes[1, 1].set_title(f'{column} - Z-Scores')
    axes[1, 1].set_xlabel('Index')
    axes[1, 1].set_ylabel('|Z-Score|')
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.show()
    
    return {
        'zscore': outliers_zscore,
        'iqr': outliers_iqr,
        'modified_z': outliers_modified_z,
        'bounds': (lower_bound, upper_bound)
    }

# Detect outliers for all numerical features
for col in numerical_features[:2]:  # Example
    outliers = detect_outliers_comprehensive(df, col)
```

### Outlier Treatment Methods

```python
# Method 1: Remove outliers
def remove_outliers_iqr(df, columns):
    """Remove outliers using IQR method"""
    df_clean = df.copy()
    
    for col in columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        outliers_before = len(df_clean[(df_clean[col] < lower) | (df_clean[col] > upper)])
        df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]
        
        print(f"{col}: Removed {outliers_before} outliers")
    
    print(f"\nRows before: {len(df)}, after: {len(df_clean)}")
    return df_clean

# Method 2: Cap outliers (Winsorization)
def cap_outliers(df, columns, lower_percentile=1, upper_percentile=99):
    """Cap outliers at specified percentiles"""
    df_capped = df.copy()
    
    for col in columns:
        lower = df_capped[col].quantile(lower_percentile/100)
        upper = df_capped[col].quantile(upper_percentile/100)
        
        df_capped[col] = df_capped[col].clip(lower, upper)
        
        print(f"{col}: Capped at [{lower:.2f}, {upper:.2f}]")
    
    return df_capped

# Method 3: Transform outliers
def transform_outliers(df, columns, method='log'):
    """Transform data to reduce outlier impact"""
    df_transformed = df.copy()
    
    for col in columns:
        if method == 'log':
            # Log transformation (requires positive values)
            df_transformed[col] = np.log1p(df_transformed[col])
        elif method == 'sqrt':
            # Square root transformation
            df_transformed[col] = np.sqrt(df_transformed[col])
        elif method == 'boxcox':
            # Box-Cox transformation
            df_transformed[col], _ = stats.boxcox(df_transformed[col] + 1)
    
    return df_transformed

# Method 4: Replace with statistics
def replace_outliers(df, columns, method='median'):
    """Replace outliers with mean/median"""
    df_replaced = df.copy()
    
    for col in columns:
        Q1 = df_replaced[col].quantile(0.25)
        Q3 = df_replaced[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        if method == 'median':
            replacement = df_replaced[col].median()
        elif method == 'mean':
            replacement = df_replaced[col].mean()
        
        outlier_mask = (df_replaced[col] < lower) | (df_replaced[col] > upper)
        df_replaced.loc[outlier_mask, col] = replacement
        
        print(f"{col}: Replaced {outlier_mask.sum()} outliers with {method}")
    
    return df_replaced

# Comparison
print("Original data:")
print(df[numerical_features].describe())

print("\n1. After removing outliers:")
df_removed = remove_outliers_iqr(df, numerical_features)

print("\n2. After capping outliers:")
df_capped = cap_outliers(df, numerical_features)
print(df_capped[numerical_features].describe())

print("\n3. After log transformation:")
df_transformed = transform_outliers(df, numerical_features, method='log')
print(df_transformed[numerical_features].describe())
```

### When to Keep vs Remove Outliers

```python
"""
KEEP OUTLIERS when:
✅ They are valid data points (e.g., CEO salary in salary data)
✅ Using tree-based models (Random Forest, XGBoost)
✅ Outliers are important for the problem (e.g., fraud detection)
✅ Small dataset (removing would lose too much data)

REMOVE/TREAT OUTLIERS when:
✅ They are data errors
✅ Using distance-based models (KNN, SVM, Linear models)
✅ Outliers distort statistics (mean, std)
✅ Large dataset (can afford to lose some data)
✅ Outliers are not relevant to problem
"""
```

---

## Feature Scaling

### Why Feature Scaling?

```python
"""
Feature Scaling is REQUIRED for:
✅ Distance-based algorithms: KNN, K-Means, SVM
✅ Gradient-based algorithms: Linear/Logistic Regression, Neural Networks
✅ Algorithms using regularization: Ridge, Lasso, ElasticNet
✅ PCA and other dimensionality reduction

Feature Scaling is NOT required for:
❌ Tree-based algorithms: Decision Tree, Random Forest, XGBoost, LightGBM
❌ Naive Bayes

Example showing why:
Feature 1: Age (range: 18-65)
Feature 2: Income (range: 20000-200000)

Without scaling:
- Income dominates in distance calculations
- Gradient descent takes longer to converge
- Model weights are on different scales
"""
```

### Scaling Method 1: StandardScaler (Z-Score Normalization)

```python
from sklearn.preprocessing import StandardScaler

# StandardScaler: (x - mean) / std
# Result: mean = 0, std = 1

scaler = StandardScaler()

# Fit on training data ONLY
X_train_scaled = scaler.fit_transform(X_train)

# Transform test data using training statistics
X_test_scaled = scaler.transform(X_test)

# Example
data = pd.DataFrame({
    'age': [25, 30, 35, 40, 45],
    'income': [30000, 45000, 60000, 75000, 90000]
})

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

print("Original data:")
print(data)
print("\nScaled data (mean=0, std=1):")
print(pd.DataFrame(data_scaled, columns=data.columns))
print("\nMean:", data_scaled.mean(axis=0))
print("Std:", data_scaled.std(axis=0))
```

**When to use StandardScaler:**
- ✅ Data is approximately normally distributed
- ✅ Contains outliers (they're scaled but not removed)
- ✅ Need features on same scale
- ✅ Using Linear/Logistic Regression, SVM, KNN
- ✅ Most common choice

**Advantages:**
- ✅ Preserves outlier information
- ✅ Works well with many algorithms
- ✅ Less affected by outliers than MinMaxScaler

**Disadvantages:**
- ❌ Outliers affect mean and std
- ❌ Scaled data can be negative
- ❌ Doesn't guarantee bounded range

### Scaling Method 2: MinMaxScaler

```python
from sklearn.preprocessing import MinMaxScaler

# MinMaxScaler: (x - min) / (max - min)
# Result: range [0, 1]

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_train)

# Custom range [a, b]
scaler = MinMaxScaler(feature_range=(0, 10))
X_scaled = scaler.fit_transform(X_train)

# Example
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

print("Original data:")
print(data)
print("\nScaled data [0, 1]:")
print(pd.DataFrame(data_scaled, columns=data.columns))
print("\nMin:", data_scaled.min(axis=0))
print("Max:", data_scaled.max(axis=0))
```

**When to use MinMaxScaler:**
- ✅ Need bounded range [0, 1]
- ✅ Neural networks (bounded activation functions)
- ✅ Image processing (pixel values 0-255 → 0-1)
- ✅ No significant outliers
- ✅ When zero means something (e.g., no purchase)

**Advantages:**
- ✅ Bounded range
- ✅ Preserves zero values
- ✅ Good for neural networks

**Disadvantages:**
- ❌ Very sensitive to outliers
- ❌ Outliers compress most values to small range
- ❌ New data may fall outside [0, 1]

### Scaling Method 3: RobustScaler

```python
from sklearn.preprocessing import RobustScaler

# RobustScaler: (x - median) / IQR
# Uses median and IQR instead of mean and std
# IQR = Q3 - Q1 (Interquartile Range)

scaler = RobustScaler()
X_scaled = scaler.fit_transform(X_train)

# Example with outliers
data_with_outliers = pd.DataFrame({
    'age': [25, 30, 35, 40, 45, 100],  # 100 is outlier
    'income': [30000, 45000, 60000, 75000, 90000, 500000]  # 500000 is outlier
})

# Compare scalers
standard_scaler = StandardScaler()
minmax_scaler = MinMaxScaler()
robust_scaler = RobustScaler()

print("Original data:")
print(data_with_outliers)

print("\nStandardScaler:")
print(pd.DataFrame(standard_scaler.fit_transform(data_with_outliers), 
                   columns=data_with_outliers.columns))

print("\nMinMaxScaler:")
print(pd.DataFrame(minmax_scaler.fit_transform(data_with_outliers), 
                   columns=data_with_outliers.columns))

print("\nRobustScaler:")
print(pd.DataFrame(robust_scaler.fit_transform(data_with_outliers), 
                   columns=data_with_outliers.columns))
```

**When to use RobustScaler:**
- ✅ Data has many outliers
- ✅ Want to reduce outlier impact
- ✅ Median and IQR are better representatives
- ✅ Skewed distributions

**Advantages:**
- ✅ Robust to outliers
- ✅ Uses median (not affected by extremes)
- ✅ Good for skewed data

**Disadvantages:**
- ❌ Doesn't guarantee bounded range
- ❌ May not perform as well without outliers
- ❌ Less commonly used

### Scaling Method 4: MaxAbsScaler

```python
from sklearn.preprocessing import MaxAbsScaler

# MaxAbsScaler: x / |max|
# Result: range [-1, 1]
# Preserves sparsity (zeros remain zeros)

scaler = MaxAbsScaler()
X_scaled = scaler.fit_transform(X_train)

# Example
scaler = MaxAbsScaler()
data_scaled = scaler.fit_transform(data)

print("Scaled data [-1, 1]:")
print(pd.DataFrame(data_scaled, columns=data.columns))
```

**When to use MaxAbsScaler:**
- ✅ Sparse data (many zeros)
- ✅ Want to preserve sparsity
- ✅ Data is already centered at zero

**Advantages:**
- ✅ Preserves sparsity
- ✅ Simple and fast

**Disadvantages:**
- ❌ Sensitive to outliers
- ❌ Not commonly used

### Scaling Method 5: Normalizer

```python
from sklearn.preprocessing import Normalizer

# Normalizer: Scale each sample to unit norm
# L1 norm: sum(|x|) = 1
# L2 norm: sqrt(sum(x²)) = 1

# L2 normalization (default)
scaler = Normalizer(norm='l2')
X_scaled = scaler.fit_transform(X_train)

# L1 normalization
scaler = Normalizer(norm='l1')
X_scaled = scaler.fit_transform(X_train)

# Example
data_sample = np.array([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]])

# L2 normalization
scaler_l2 = Normalizer(norm='l2')
data_l2 = scaler_l2.fit_transform(data_sample)

print("Original:")
print(data_sample)
print("\nL2 Normalized:")
print(data_l2)
print("L2 norms:", np.sqrt((data_l2**2).sum(axis=1)))  # Should be all 1.0
```

**When to use Normalizer:**
- ✅ Text data (TF-IDF vectors)
- ✅ Want unit-length vectors
- ✅ Cosine similarity comparisons
- ✅ Neural network inputs

**Advantages:**
- ✅ Each sample has unit length
- ✅ Good for direction-based comparisons

**Disadvantages:**
- ❌ Different purpose than other scalers
- ❌ Scales rows, not columns

### Scaling Comparison

```python
# Visual comparison of scalers
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=200, n_features=2, 
                          n_informative=2, n_redundant=0,
                          random_state=42)

# Add outliers
X[0] = [10, 10]
X[1] = [-10, -10]

scalers = {
    'Original': None,
    'StandardScaler': StandardScaler(),
    'MinMaxScaler': MinMaxScaler(),
    'RobustScaler': RobustScaler(),
    'MaxAbsScaler': MaxAbsScaler()
}

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for idx, (name, scaler) in enumerate(scalers.items()):
    if scaler is None:
        X_scaled = X
    else:
        X_scaled = scaler.fit_transform(X)
    
    axes[idx].scatter(X_scaled[:, 0], X_scaled[:, 1], alpha=0.6)
    axes[idx].set_title(name)
    axes[idx].set_xlabel('Feature 1')
    axes[idx].set_ylabel('Feature 2')
    axes[idx].grid(True, alpha=0.3)
    
    # Add statistics
    axes[idx].text(0.05, 0.95, 
                   f'Range: [{X_scaled[:, 0].min():.2f}, {X_scaled[:, 0].max():.2f}]',
                   transform=axes[idx].transAxes,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

axes[-1].axis('off')
plt.tight_layout()
plt.show()
```

### Scaling Decision Guide

```python
"""
DECISION TREE FOR CHOOSING SCALER:

1. Is your algorithm tree-based (RF, XGBoost, etc.)?
   → NO SCALING NEEDED

2. Do you have many outliers?
   → YES: RobustScaler
   → NO: Continue

3. Do you need bounded range [0, 1]?
   → YES: MinMaxScaler (if no outliers)
   → NO: Continue

4. Is data approximately normal?
   → YES: StandardScaler (most common)
   → NO: RobustScaler or log transformation first

5. Is data sparse (many zeros)?
   → YES: MaxAbsScaler
   → NO: StandardScaler

6. Working with text/vectors?
   → YES: Normalizer
   → NO: StandardScaler

DEFAULT CHOICE: StandardScaler (works well in most cases)
"""
```

### Scaling Best Practices

```python
# ✅ CORRECT: Fit on train, transform both train and test
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit and transform
X_test_scaled = scaler.transform(X_test)         # Only transform

# ❌ WRONG: Fitting on entire dataset (DATA LEAKAGE!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # WRONG!
X_train, X_test = train_test_split(X_scaled)

# ❌ WRONG: Fitting separately on train and test
scaler_train = StandardScaler()
scaler_test = StandardScaler()
X_train_scaled = scaler_train.fit_transform(X_train)
X_test_scaled = scaler_test.fit_transform(X_test)  # WRONG!

# ✅ Use Pipeline to avoid mistakes
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])

# Pipeline automatically fits scaler only on training data
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

### Scaling in Cross-Validation

```python
# ✅ CORRECT: Scaling inside cross-validation
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])

# Each fold scales using only training folds
scores = cross_val_score(pipeline, X, y, cv=5)

# ❌ WRONG: Scaling before cross-validation
X_scaled = StandardScaler().fit_transform(X)  # Data leakage!
scores = cross_val_score(LogisticRegression(), X_scaled, y, cv=5)
```

---

## Feature Encoding

### Encoding Method 1: Label Encoding

```python
from sklearn.preprocessing import LabelEncoder

# For ordinal categorical variables
# Example: Size (Small < Medium < Large)

df['size'] = ['Small', 'Medium', 'Large', 'Medium', 'Small', 'Large']

le = LabelEncoder()
df['size_encoded'] = le.fit_transform(df['size'])

print("Label Encoding:")
print(df[['size', 'size_encoded']])
# Small → 0, Medium → 1, Large → 2

# Inverse transform
df['size_decoded'] = le.inverse_transform(df['size_encoded'])

# When to use:
# ✅ Ordinal variables (natural ordering)
# ✅ Tree-based models (can handle encoded values)
# ❌ Nominal variables (introduces false ordering)
# ❌ Linear models (implies numeric relationship)
```

**Advantages:**
- ✅ Simple and fast
- ✅ Preserves memory (single column)
- ✅ Works with tree-based models

**Disadvantages:**
- ❌ Introduces false ordering for nominal variables
- ❌ Linear models treat as numeric
- ❌ Distance between categories is arbitrary

### Encoding Method 2: One-Hot Encoding

```python
# For nominal categorical variables (no ordering)
# Example: Color (Red, Blue, Green)

df = pd.DataFrame({
    'color': ['Red', 'Blue', 'Green', 'Red', 'Blue']
})

# Method 1: pandas get_dummies
df_encoded = pd.get_dummies(df, columns=['color'], prefix='color')
print("One-Hot Encoding:")
print(df_encoded)

# Method 2: sklearn OneHotEncoder
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(sparse_output=False, drop='first')  # drop='first' avoids multicollinearity
encoded = ohe.fit_transform(df[['color']])
encoded_df = pd.DataFrame(encoded, columns=ohe.get_feature_names_out())

print("\nOneHotEncoder:")
print(encoded_df)

# When to use:
# ✅ Nominal variables (no natural order)
# ✅ Few unique categories (<10-15)
# ✅ Linear models (Logistic Regression, Linear Regression)
# ❌ High cardinality (too many categories)
# ❌ Tree-based models (prefer label encoding)
```

**Advantages:**
- ✅ No false ordering
- ✅ Works well with linear models
- ✅ Easy to interpret

**Disadvantages:**
- ❌ High cardinality causes curse of dimensionality
- ❌ Increases memory usage
- ❌ Can cause multicollinearity (use drop='first')

### Encoding Method 3: Target Encoding

```python
# Encode categories based on target mean

def target_encode(train_df, test_df, column, target, smoothing=1):
    """
    Target encoding with smoothing
    smoothing: controls weight of global mean
    """
    # Global mean
    global_mean = train_df[target].mean()
    
    # Calculate mean target for each category
    target_means = train_df.groupby(column)[target].agg(['mean', 'count'])
    
    # Smoothing: (count * mean + smoothing * global_mean) / (count + smoothing)
    target_means['smoothed_mean'] = (
        (target_means['count'] * target_means['mean'] + smoothing * global_mean) /
        (target_means['count'] + smoothing)
    )
    
    # Map to train and test
    train_encoded = train_df[column].map(target_means['smoothed_mean'])
    test_encoded = test_df[column].map(target_means['smoothed_mean'])
    
    # Fill unseen categories with global mean
    train_encoded = train_encoded.fillna(global_mean)
    test_encoded = test_encoded.fillna(global_mean)
    
    return train_encoded, test_encoded

# Example
df = pd.DataFrame({
    'city': ['NY', 'LA', 'NY', 'SF', 'LA', 'NY', 'SF', 'LA'],
    'target': [1, 0, 1, 0, 0, 1, 1, 0]
})

train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)

train_df['city_encoded'], test_df['city_encoded'] = target_encode(
    train_df, test_df, 'city', 'target', smoothing=1
)

print("Target Encoding:")
print(train_df)

# When to use:
# ✅ High cardinality (many categories)
# ✅ Tree-based models
# ✅ Categories have relationship with target
# ⚠️ Risk of overfitting (use cross-validation encoding)
# ⚠️ Risk of data leakage (use only training data statistics)
```

**Advantages:**
- ✅ Handles high cardinality well
- ✅ Captures relationship with target
- ✅ Single feature (memory efficient)

**Disadvantages:**
- ❌ Risk of overfitting
- ❌ Risk of data leakage
- ❌ Requires careful implementation

### Encoding Method 4: Frequency Encoding

```python
# Encode based on frequency of each category

def frequency_encode(train_df, test_df, column):
    """Frequency encoding"""
    freq = train_df[column].value_counts(normalize=True)
    
    train_encoded = train_df[column].map(freq)
    test_encoded = test_df[column].map(freq)
    
    # Fill unseen categories with 0
    train_encoded = train_encoded.fillna(0)
    test_encoded = test_encoded.fillna(0)
    
    return train_encoded, test_encoded

# Example
df['city_freq'] = df['city'].map(df['city'].value_counts(normalize=True))

print("Frequency Encoding:")
print(df[['city', 'city_freq']])

# When to use:
# ✅ High cardinality
# ✅ Frequency matters for prediction
# ✅ Simple alternative to target encoding
```

**Advantages:**
- ✅ Simple and fast
- ✅ Handles high cardinality
- ✅ No data leakage risk

**Disadvantages:**
- ❌ Loses category identity
- ❌ Different categories with same frequency get same encoding

### Encoding Method 5: Binary Encoding

```python
# Convert to binary representation
# Good middle ground for high cardinality

from category_encoders import BinaryEncoder

df = pd.DataFrame({
    'city': ['NY', 'LA', 'SF', 'Chicago', 'Boston', 'Seattle', 'Miami', 'Dallas']
})

be = BinaryEncoder(cols=['city'])
df_encoded = be.fit_transform(df)

print("Binary Encoding:")
print(df_encoded)

# NY → 001, LA → 010, SF → 011, etc.

# When to use:
# ✅ High cardinality (middle ground between label and one-hot)
# ✅ Reduces dimensions compared to one-hot
```

### Encoding Comparison

```python
# Compare encoding methods

data = pd.DataFrame({
    'category': ['A', 'B', 'C', 'A', 'B', 'A', 'C', 'B'] * 100,
    'target': [1, 0, 1, 1, 0, 1, 0, 0] * 100
})

print("Original categories:", data['category'].nunique())

# Label Encoding
le = LabelEncoder()
data['label_encoded'] = le.fit_transform(data['category'])
print(f"\nLabel Encoding: {data['label_encoded'].nunique()} unique values")

# One-Hot Encoding
ohe_data = pd.get_dummies(data, columns=['category'])
print(f"One-Hot Encoding: {ohe_data.shape[1]-2} new columns created")

# Target Encoding
target_means = data.groupby('category')['target'].mean()
data['target_encoded'] = data['category'].map(target_means)
print(f"Target Encoding: 1 column with continuous values")

# Frequency Encoding
freq = data['category'].value_counts(normalize=True)
data['freq_encoded'] = data['category'].map(freq)
print(f"Frequency Encoding: 1 column with frequencies")

# Summary
print("\n" + "="*60)
print("ENCODING DECISION GUIDE:")
print("="*60)
print("Ordinal (ordered) → Label Encoding")
print("Nominal + Low cardinality (<10) → One-Hot Encoding")
print("Nominal + High cardinality → Target/Binary/Frequency Encoding")
print("Tree-based models → Label/Target Encoding")
print("Linear models → One-Hot Encoding")
print("="*60)
```

---

## Feature Engineering

### Feature Engineering Techniques

```python
# 1. Polynomial Features
from sklearn.preprocessing import PolynomialFeatures

# Create interaction and polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X[['feature1', 'feature2']])

# Example: [a, b] → [a, b, a², ab, b²]

# 2. Mathematical Transformations
df['log_feature'] = np.log1p(df['feature'])  # log(x + 1)
df['sqrt_feature'] = np.sqrt(df['feature'])
df['square_feature'] = df['feature'] ** 2
df['reciprocal'] = 1 / (df['feature'] + 1)

# 3. Binning (Discretization)
df['age_group'] = pd.cut(df['age'], 
                         bins=[0, 18, 35, 50, 100],
                         labels=['child', 'young', 'middle', 'senior'])

# Equal-frequency binning
df['income_quartile'] = pd.qcut(df['income'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

# 4. Date/Time Features
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['dayofweek'] = df['date'].dt.dayofweek
df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
df['quarter'] = df['date'].dt.quarter
df['days_since'] = (pd.Timestamp.now() - df['date']).dt.days

# 5. Text Features
df['text_length'] = df['text'].str.len()
df['word_count'] = df['text'].str.split().str.len()
df['char_count'] = df['text'].str.replace(' ', '').str.len()
df['uppercase_count'] = df['text'].str.count(r'[A-Z]')
df['digit_count'] = df['text'].str.count(r'\d')

# 6. Aggregation Features
# Group-wise statistics
df['avg_price_by_category'] = df.groupby('category')['price'].transform('mean')
df['max_price_by_category'] = df.groupby('category')['price'].transform('max')
df['count_by_category'] = df.groupby('category')['product_id'].transform('count')

# 7. Ratio Features
df['price_to_avg_ratio'] = df['price'] / df['avg_price_by_category']
df['debt_to_income'] = df['debt'] / (df['income'] + 1)
df['bmi'] = df['weight'] / (df['height'] ** 2)

# 8. Domain-Specific Features
# E-commerce example
df['total_amount'] = df['quantity'] * df['unit_price']
df['discount_percentage'] = (df['original_price'] - df['sale_price']) / df['original_price'] * 100
df['is_first_purchase'] = (df['purchase_count'] == 1).astype(int)

# 9. Lag Features (Time Series)
df['previous_day_sales'] = df['sales'].shift(1)
df['rolling_mean_7d'] = df['sales'].rolling(window=7).mean()
df['rolling_std_7d'] = df['sales'].rolling(window=7).std()

# 10. Feature Combinations
df['age_income'] = df['age'] * df['income']
df['total_bedrooms'] = df['bedrooms'] + df['bathrooms']
```

### Feature Selection Methods

```python
# Method 1: Correlation-based selection
def select_features_correlation(df, target, threshold=0.1):
    """Select features with correlation > threshold with target"""
    correlations = df.corr()[target].abs().sort_values(ascending=False)
    selected = correlations[correlations > threshold].index.tolist()
    selected.remove(target)
    return selected

# Method 2: Feature Importance (Tree-based)
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

feature_importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

# Select top N features
top_features = feature_importance.head(10)['feature'].tolist()

# Method 3: Recursive Feature Elimination (RFE)
from sklearn.feature_selection import RFE

rfe = RFE(estimator=RandomForestClassifier(), n_features_to_select=10)
rfe.fit(X_train, y_train)

selected_features = X_train.columns[rfe.support_].tolist()
print(f"Selected features: {selected_features}")

# Method 4: SelectKBest (statistical tests)
from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(score_func=f_classif, k=10)
selector.fit(X_train, y_train)

selected_features = X_train.columns[selector.get_support()].tolist()

# Method 5: L1 Regularization (Lasso)
from sklearn.linear_model import LassoCV

lasso = LassoCV(cv=5, random_state=42)
lasso.fit(X_train, y_train)

# Features with non-zero coefficients
selected_features = X_train.columns[lasso.coef_ != 0].tolist()
print(f"Lasso selected {len(selected_features)} features")
```

---

## Data Transformation

### Transformation 1: Log Transformation

```python
# For right-skewed data (reduce positive skew)

# Before
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
df['income'].hist(bins=50)
plt.title(f'Original (Skewness: {df["income"].skew():.2f})')
plt.xlabel('Income')

# After log transformation
df['income_log'] = np.log1p(df['income'])  # log(1 + x) to handle zeros

plt.subplot(1, 2, 2)
df['income_log'].hist(bins=50)
plt.title(f'Log Transformed (Skewness: {df["income_log"].skew():.2f})')
plt.xlabel('Log(Income)')

plt.tight_layout()
plt.show()

# When to use:
# ✅ Right-skewed data (long tail on right)
# ✅ Data spans several orders of magnitude
# ✅ Multiplicative relationships
# ❌ Data contains zeros or negative values (use log1p)
```

### Transformation 2: Square Root Transformation

```python
# For moderate right-skewed data

df['feature_sqrt'] = np.sqrt(df['feature'])

# When to use:
# ✅ Moderate right-skew (less aggressive than log)
# ✅ Count data
# ✅ Data is non-negative
```

### Transformation 3: Box-Cox Transformation

```python
# Finds optimal power transformation

from scipy.stats import boxcox

# Box-Cox requires positive values
df_positive = df[df['feature'] > 0]

transformed, lambda_param = boxcox(df_positive['feature'])

print(f"Optimal lambda: {lambda_param:.4f}")

# Lambda interpretation:
# -1: Reciprocal
#  0: Log
# 0.5: Square root
#  1: No transformation
#  2: Square

# Plot
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].hist(df_positive['feature'], bins=50)
axes[0].set_title('Original')

axes[1].hist(transformed, bins=50)
axes[1].set_title(f'Box-Cox (λ={lambda_param:.2f})')

plt.tight_layout()
plt.show()

# When to use:
# ✅ Automatic selection of best transformation
# ✅ Need to normalize distribution
# ❌ Data has zeros or negative values (use Yeo-Johnson instead)
```

### Transformation 4: Yeo-Johnson Transformation

```python
# Like Box-Cox but handles negative values

from sklearn.preprocessing import PowerTransformer

pt = PowerTransformer(method='yeo-johnson')
df['feature_transformed'] = pt.fit_transform(df[['feature']])

# When to use:
# ✅ Data has zeros or negative values
# ✅ Need to normalize distribution
# ✅ Works with all real numbers
```

### Transformation 5: Quantile Transformation

```python
# Transform to uniform or normal distribution

from sklearn.preprocessing import QuantileTransformer

# Uniform distribution
qt_uniform = QuantileTransformer(output_distribution='uniform')
df['feature_uniform'] = qt_uniform.fit_transform(df[['feature']])

# Normal distribution
qt_normal = QuantileTransformer(output_distribution='normal')
df['feature_normal'] = qt_normal.fit_transform(df[['feature']])

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].hist(df['feature'], bins=50)
axes[0].set_title('Original')

axes[1].hist(df['feature_uniform'], bins=50)
axes[1].set_title('Uniform')

axes[2].hist(df['feature_normal'], bins=50)
axes[2].set_title('Normal')

plt.tight_layout()
plt.show()

# When to use:
# ✅ Heavy outliers
# ✅ Complex distributions
# ✅ Need specific distribution shape
# ⚠️ Can distort relationships between features
```

---

## Common Mistakes

### Mistake 1: Data Leakage

```python
# ❌ WRONG: Scaling before train-test split
X_scaled = StandardScaler().fit_transform(X)
X_train, X_test = train_test_split(X_scaled, y)
# Problem: Test data influenced training statistics

# ✅ CORRECT: Split first, then scale
X_train, X_test, y_train, y_test = train_test_split(X, y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### Mistake 2: Not Checking Data Types

```python
# ❌ WRONG: Assuming correct data types
model.fit(X_train, y_train)
# Problem: Numerical columns stored as strings

# ✅ CORRECT: Check and convert
print(df.dtypes)
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['date'] = pd.to_datetime(df['date'])
```

### Mistake 3: Ignoring Missing Values

```python
# ❌ WRONG: Fitting model with missing values
model.fit(X_train, y_train)
# Problem: Most models can't handle NaN

# ✅ CORRECT: Handle missing values explicitly
print(X_train.isnull().sum())
imputer = SimpleImputer(strategy='median')
X_train_imputed = imputer.fit_transform(X_train)
```

### Mistake 4: Feature Scaling Tree-Based Models

```python
# ❌ WRONG: Scaling for Random Forest
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
RandomForestClassifier().fit(X_scaled, y)
# Problem: Unnecessary (tree-based models don't need scaling)

# ✅ CORRECT: No scaling for tree-based
RandomForestClassifier().fit(X, y)
```

### Mistake 5: Using One-Hot Encoding with High Cardinality

```python
# ❌ WRONG: One-hot encoding 1000 unique cities
df_encoded = pd.get_dummies(df, columns=['city'])
# Problem: Creates 1000 columns (curse of dimensionality)

# ✅ CORRECT: Use target encoding or frequency encoding
target_means = df.groupby('city')['target'].mean()
df['city_encoded'] = df['city'].map(target_means)
```

### Mistake 6: Not Handling Outliers

```python
# ❌ WRONG: Ignoring extreme outliers
model.fit(X_train, y_train)
# Problem: Outliers distort linear models

# ✅ CORRECT: Detect and handle
Q1 = df['feature'].quantile(0.25)
Q3 = df['feature'].quantile(0.75)
IQR = Q3 - Q1
df_clean = df[(df['feature'] >= Q1 - 1.5*IQR) & (df['feature'] <= Q3 + 1.5*IQR)]
```

### Mistake 7: Not Checking Class Balance

```python
# ❌ WRONG: Training on imbalanced data without handling
model.fit(X_train, y_train)
# Problem: Model biased toward majority class

# ✅ CORRECT: Check and handle imbalance
print(y_train.value_counts())
model = RandomForestClassifier(class_weight='balanced')
```

### Mistake 8: Dropping Highly Correlated Features Too Early

```python
# ❌ WRONG: Removing all correlated features
corr_matrix = df.corr().abs()
high_corr = (corr_matrix > 0.8).sum()
df_dropped = df.drop(columns=high_corr[high_corr > 1].index)
# Problem: May remove useful features

# ✅ CORRECT: Check feature importance first, then decide
# Some models handle correlation well (tree-based)
# Linear models more affected by multicollinearity
```

### Mistake 9: Not Handling Date/Time Properly

```python
# ❌ WRONG: Using date as string or dropping it
df = df.drop('date', axis=1)

# ✅ CORRECT: Extract useful features
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
```

### Mistake 10: Not Using Pipelines

```python
# ❌ WRONG: Manual preprocessing steps (error-prone)
X_train_imputed = imputer.fit_transform(X_train)
X_train_scaled = scaler.fit_transform(X_train_imputed)
model.fit(X_train_scaled, y_train)

X_test_imputed = imputer.transform(X_test)
X_test_scaled = scaler.transform(X_test_imputed)
predictions = model.predict(X_test_scaled)

# ✅ CORRECT: Use Pipeline
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier())
])

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

---

## Interview Questions

### Question 1: EDA Process

**Q: Walk me through your EDA process for a new dataset.**

**A:**
1. **Initial Understanding:**
   - Load data and check shape (rows, columns)
   - View first/last rows
   - Check data types and memory usage
   - Identify numerical vs categorical features

2. **Data Quality:**
   - Missing values (count, percentage, patterns)
   - Duplicate rows
   - Constant/quasi-constant features
   - Data type inconsistencies

3. **Statistical Summary:**
   - Describe() for numerical features
   - Value counts for categorical features
   - Distribution shapes (skewness, kurtosis)

4. **Univariate Analysis:**
   - Histograms for numerical features
   - Bar plots for categorical features
   - Check for outliers

5. **Bivariate Analysis:**
   - Feature vs target relationships
   - Correlation analysis
   - Scatter plots for numerical pairs

6. **Multivariate Analysis:**
   - Correlation matrix
   - Pair plots
   - PCA for dimensionality understanding

7. **Preprocessing Decisions:**
   - How to handle missing values
   - Outlier treatment strategy
   - Scaling requirements
   - Encoding strategy

---

### Question 2: Feature Scaling

**Q: When and why do we need feature scaling? Which scaler would you choose and why?**

**A:**

**When Needed:**
- Distance-based algorithms: KNN, K-Means, SVM
- Gradient-based: Linear/Logistic Regression, Neural Networks
- Regularization: Ridge, Lasso, ElasticNet
- PCA

**Not Needed:**
- Tree-based: Decision Tree, Random Forest, XGBoost

**Scaler Choice:**
- **StandardScaler (default):** Normally distributed data, works with most algorithms
- **MinMaxScaler:** Need bounded range [0,1], neural networks
- **RobustScaler:** Many outliers, skewed distribution
- **MaxAbsScaler:** Sparse data, preserve zeros

**Example:** For house price prediction with income, age, and square footage:
- Income (20K-200K) and square footage (500-5000) have different scales
- Use StandardScaler before Logistic Regression
- Don't scale for Random Forest

---

### Question 3: Handling Missing Values

**Q: How do you decide which imputation method to use?**

**A:**

**Decision Factors:**
1. **Amount of missing data:**
   - <5%: Can drop rows
   - 5-20%: Imputation
   - >20%: Consider dropping feature or advanced imputation

2. **Data type:**
   - Numerical: Mean (normal), Median (skewed), KNN (related features)
   - Categorical: Mode, New category "Missing"

3. **Missingness mechanism:**
   - MCAR (Missing Completely At Random): Simple imputation OK
   - MAR (Missing At Random): Advanced imputation
   - MNAR (Missing Not At Random): Create missing indicator

4. **Feature relationships:**
   - Independent features: Simple imputation
   - Related features: KNN or Iterative Imputation

5. **Model type:**
   - Tree-based: Can handle some missing (XGBoost)
   - Linear models: Must impute

**Example:** 
- Age with 10% missing, related to income → KNN Imputation
- Survey response with 30% missing → Consider missing as separate category

---

### Question 4: Outlier Detection and Treatment

**Q: How do you detect and handle outliers? When would you keep vs remove them?**

**A:**

**Detection Methods:**
1. **Statistical:**
   - Z-score: |z| > 3
   - IQR: Q1 - 1.5×IQR to Q3 + 1.5×IQR
   - Modified Z-score (robust)

2. **Visual:**
   - Box plots
   - Scatter plots
   - Histograms

3. **Machine Learning:**
   - Isolation Forest
   - DBSCAN

**Treatment:**
1. **Remove:** Data errors, using distance-based models
2. **Cap (Winsorize):** Valid but extreme values
3. **Transform:** Log transformation to reduce impact
4. **Keep:** Valid data points, tree-based models, fraud detection

**Example:**
- CEO salary in salary dataset → Keep (valid outlier)
- Age = 200 → Remove (data error)
- Income in Linear Regression → Cap or transform

**Decision Guide:**
- Small dataset → Keep (can't afford to lose data)
- Large dataset + data errors → Remove
- Linear models → More sensitive, treat outliers
- Tree-based models → Less sensitive, can keep

---

### Question 5: Feature Encoding

**Q: Compare Label Encoding vs One-Hot Encoding. When would you use each?**

**A:**

**Label Encoding:**
- Converts categories to integers: {Red:0, Blue:1, Green:2}
- **Use when:**
  - Ordinal variables (Small < Medium < Large)
  - Tree-based models (can handle encoded values)
  - High cardinality with limited memory
- **Avoid when:**
  - Nominal variables with linear models (implies ordering)

**One-Hot Encoding:**
- Creates binary column for each category
- **Use when:**
  - Nominal variables (no natural order)
  - Linear models (Logistic Regression, SVM)
  - Low cardinality (<10 categories)
- **Avoid when:**
  - High cardinality (curse of dimensionality)
  - Tree-based models (less efficient)

**Example:**
```
Education: ["High School", "Bachelor", "Master", "PhD"]
→ Label Encoding (ordinal)

Color: ["Red", "Blue", "Green"]
→ One-Hot Encoding for Linear Regression
→ Label Encoding for Random Forest
```

**Alternative for High Cardinality:**
- Target Encoding
- Frequency Encoding
- Binary Encoding

---

### Question 6: Data Leakage

**Q: What is data leakage and how do you prevent it?**

**A:**

**Data Leakage:** When information from test set leaks into training process, causing overly optimistic performance.

**Types:**

1. **Train-Test Contamination:**
```python
# ❌ WRONG
X_scaled = scaler.fit_transform(X)  # Uses all data!
X_train, X_test = train_test_split(X_scaled)

# ✅ CORRECT
X_train, X_test = train_test_split(X)
scaler.fit(X_train)  # Only training data
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

2. **Target Leakage:**
- Features that wouldn't be available at prediction time
- Example: Using "total_amount_paid" to predict "will_pay"

3. **Temporal Leakage:**
- Using future information in time series
- Example: Using next month's price to predict current demand

**Prevention:**
- ✅ Split data before preprocessing
- ✅ Use pipelines
- ✅ Fit only on training data
- ✅ Check feature availability at prediction time
- ✅ Time-based splitting for time series

---

### Question 7: Correlation Analysis

**Q: You found two features with 0.95 correlation. What would you do?**

**A:**

**High Correlation (Multicollinearity) Impact:**
- Linear models: Unstable coefficients, difficult interpretation
- Tree-based models: Less affected, can use both

**Analysis Steps:**

1. **Check correlation with target:**
```python
corr_with_target = df[['feature1', 'feature2', 'target']].corr()['target']
```

2. **Feature importance:**
```python
rf = RandomForestRegressor()
rf.fit(X_train, y_train)
importance = rf.feature_importances_
```

3. **Domain knowledge:**
- Which feature is easier to collect?
- Which makes more business sense?

**Decision:**
- **Linear models:** Remove one feature (keep one with higher correlation to target)
- **Tree-based:** Can keep both (model handles it)
- **Alternative:** PCA to combine correlated features

**Example:**
- House price prediction: bedrooms and total_rooms (0.95 correlation)
- Check importance, keep most relevant
- Or create ratio: rooms_per_bedroom

---

### Question 8: Imbalanced Data

**Q: You have a binary classification dataset with 98% negative and 2% positive class. How would you handle this?**

**A:**

**Problems:**
- Model predicts majority class for everything (98% accuracy but useless)
- Minority class (often more important) poorly predicted

**Solutions:**

1. **Evaluation Metrics:**
   - Don't use accuracy
   - Use: Precision, Recall, F1-Score, ROC-AUC, PR-AUC

2. **Resampling:**
   - **Oversample minority:** SMOTE (creates synthetic samples)
   - **Undersample majority:** Remove majority samples
   - **Combination:** SMOTEENN, SMOTETomek

3. **Algorithm Level:**
   - **Class weights:** 
   ```python
   RandomForestClassifier(class_weight='balanced')
   ```
   - Penalize misclassification of minority class more

4. **Ensemble Methods:**
   - BalancedRandomForest
   - EasyEnsemble

5. **Threshold Adjustment:**
   - Lower classification threshold for minority class

6. **Anomaly Detection:**
   - Treat minority as anomaly (Isolation Forest, One-Class SVM)

**Example Approach:**
```python
# 1. Check class distribution
print(y_train.value_counts())

# 2. Use SMOTE
from imblearn.over_sampling import SMOTE
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# 3. Use class weights
model = RandomForestClassifier(class_weight='balanced')

# 4. Evaluate with appropriate metrics
from sklearn.metrics import classification_report, roc_auc_score
print(classification_report(y_test, y_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba)}")
```

---

### Question 9: Feature Engineering

**Q: What feature engineering techniques would you apply to a datetime column?**

**A:**

**Temporal Features:**
```python
df['date'] = pd.to_datetime(df['date'])

# Basic
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['dayofweek'] = df['date'].dt.dayofweek  # 0=Monday
df['hour'] = df['date'].dt.hour

# Cyclical encoding (for periodic features)
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

# Binary flags
df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
df['is_month_start'] = df['date'].dt.is_month_start.astype(int)
df['is_month_end'] = df['date'].dt.is_month_end.astype(int)
df['is_quarter_start'] = df['date'].dt.is_quarter_start.astype(int)

# Relative time
df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
df['days_until_end'] = (df['date'].max() - df['date']).dt.days

# Business context
df['quarter'] = df['date'].dt.quarter
df['is_holiday'] = df['date'].isin(holidays).astype(int)
df['is_payday'] = df['day'].isin([15, 30]).astype(int)
```

**Why Cyclical Encoding:**
- Month 12 and Month 1 are adjacent but numerically far
- Sin/Cos encoding preserves circular nature

**Domain-Specific:**
- E-commerce: Black Friday, Cyber Monday flags
- Finance: End of quarter, fiscal year
- Retail: Back-to-school season, holiday season

---

### Question 10: Train-Test Split Strategy

**Q: How do you decide train-test split ratio and ensure no data leakage?**

**A:**

**Split Ratio:**
- **70-30 or 80-20:** Standard for most cases
- **60-20-20:** Train-Validation-Test for hyperparameter tuning
- **90-10:** Small datasets
- **Time-based:** Time series data

**Factors:**
1. **Dataset size:**
   - Large (>100K): 80-20 or even 90-10
   - Small (<1K): 70-30 or cross-validation

2. **Problem type:**
   - Time series: Chronological split (no shuffle)
   - Classification: Stratified split (maintain class distribution)
   - Regular: Random split

3. **Model complexity:**
   - Complex models need more training data
   - Simple models need less

**Implementation:**

```python
# 1. Regular split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. Stratified (classification)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 3. Time series (no shuffle)
train_size = int(0.8 * len(df))
train_df = df[:train_size]
test_df = df[train_size:]

# 4. Train-Val-Test
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5)
```

**Preventing Leakage:**
1. Split BEFORE any preprocessing
2. Fit scalers/imputers ONLY on training data
3. Use pipelines
4. Never use test data in any training decision

---

## Summary

### EDA Checklist

**✅ Initial Understanding:**
- [ ] Load data and check shape
- [ ] View first/last rows  
- [ ] Check data types
- [ ] Identify feature types

**✅ Data Quality:**
- [ ] Check missing values
- [ ] Check duplicates
- [ ] Check constant features
- [ ] Verify target distribution

**✅ Analysis:**
- [ ] Univariate analysis (distributions)
- [ ] Bivariate analysis (relationships)
- [ ] Correlation matrix
- [ ] Outlier detection

**✅ Preprocessing:**
- [ ] Handle missing values
- [ ] Handle outliers
- [ ] Feature scaling (if needed)
- [ ] Feature encoding
- [ ] Feature engineering

**✅ Validation:**
- [ ] No data leakage
- [ ] Proper train-test split
- [ ] Use pipelines
- [ ] Document decisions

---

**End of EDA Complete Guide** 📊

**Covered Topics:**
- ✅ Complete EDA workflow
- ✅ Data quality checks
- ✅ Univariate, Bivariate, Multivariate analysis
- ✅ Missing value strategies (6 methods)
- ✅ Outlier detection and treatment (4 methods)
- ✅ Feature scaling (5 methods with comparison)
- ✅ Feature encoding (5 methods)
- ✅ Feature engineering techniques
- ✅ Data transformations
- ✅ Common mistakes and best practices
- ✅ 10 interview questions with detailed answers

**Key Takeaways:**
1. Always split data BEFORE preprocessing
2. Choose appropriate scaling based on algorithm and data
3. Handle missing values thoughtfully
4. Be careful with data leakage
5. Use pipelines for reproducibility
6. Document all preprocessing decisions

Good luck with your interviews! 🚀