# Traditional Machine Learning Complete Guide

## Table of Contents
1. [Introduction to Machine Learning](#introduction-to-machine-learning)
2. [Linear Regression](#linear-regression)
3. [Logistic Regression](#logistic-regression)
4. [Decision Trees](#decision-trees)
5. [Random Forest](#random-forest)
6. [Support Vector Machines (SVM)](#support-vector-machines-svm)
7. [K-Nearest Neighbors (KNN)](#k-nearest-neighbors-knn)
8. [Naive Bayes](#naive-bayes)
9. [K-Means Clustering](#k-means-clustering)
10. [Principal Component Analysis (PCA)](#principal-component-analysis-pca)
11. [Gradient Boosting (XGBoost, LightGBM)](#gradient-boosting-xgboost-lightgbm)
12. [Model Selection Guide](#model-selection-guide)
13. [Interview Questions (3 YOE)](#interview-questions-3-years-experience)

---

## Introduction to Machine Learning

### What is Machine Learning?

Machine Learning is a subset of Artificial Intelligence that enables computers to learn from data without being explicitly programmed.

**Key Concepts:**
- **Training:** Learning patterns from historical data
- **Testing:** Evaluating model on unseen data
- **Features:** Input variables (X)
- **Target:** Output variable (y)
- **Model:** Mathematical function that maps features to target

### Types of Machine Learning

```
Machine Learning
│
├── Supervised Learning (Labeled data)
│   ├── Regression (Continuous output)
│   │   ├── Linear Regression
│   │   ├── Polynomial Regression
│   │   ├── Ridge/Lasso Regression
│   │   └── SVR
│   │
│   └── Classification (Discrete output)
│       ├── Logistic Regression
│       ├── Decision Trees
│       ├── Random Forest
│       ├── SVM
│       ├── KNN
│       ├── Naive Bayes
│       └── Gradient Boosting
│
├── Unsupervised Learning (Unlabeled data)
│   ├── Clustering
│   │   ├── K-Means
│   │   ├── DBSCAN
│   │   └── Hierarchical Clustering
│   │
│   └── Dimensionality Reduction
│       ├── PCA
│       ├── t-SNE
│       └── LDA
│
└── Reinforcement Learning (Reward-based)
    ├── Q-Learning
    ├── Deep Q-Network
    └── Policy Gradient
```

### Machine Learning Workflow

```python
# 1. Import Libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# 2. Load Data
data = pd.read_csv('data.csv')

# 3. Exploratory Data Analysis (EDA)
print(data.head())
print(data.info())
print(data.describe())

# 4. Data Preprocessing
# Handle missing values
data = data.dropna()  # or data.fillna(data.mean())

# Encode categorical variables
data = pd.get_dummies(data, columns=['category'])

# Split features and target
X = data.drop('target', axis=1)
y = data['target']

# 5. Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 7. Train Model
model = LogisticRegression()
model.fit(X_train, y_train)

# 8. Make Predictions
y_pred = model.predict(X_test)

# 9. Evaluate Model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')
print(confusion_matrix(y_test, y_pred))

# 10. Save Model
import joblib
joblib.dump(model, 'model.pkl')
```

### Key Metrics

**Classification Metrics:**
```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# Accuracy: (TP + TN) / Total
accuracy = accuracy_score(y_test, y_pred)

# Precision: TP / (TP + FP) - How many predicted positives are actually positive
precision = precision_score(y_test, y_pred)

# Recall (Sensitivity): TP / (TP + FN) - How many actual positives were found
recall = recall_score(y_test, y_pred)

# F1-Score: Harmonic mean of precision and recall
f1 = f1_score(y_test, y_pred)

# ROC-AUC: Area under ROC curve
roc_auc = roc_auc_score(y_test, y_pred_proba)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
# [[TN, FP],
#  [FN, TP]]
```

**Regression Metrics:**
```python
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error
)

# Mean Absolute Error: Average absolute difference
mae = mean_absolute_error(y_test, y_pred)

# Mean Squared Error: Average squared difference
mse = mean_squared_error(y_test, y_pred)

# Root Mean Squared Error
rmse = np.sqrt(mse)

# R² Score: Proportion of variance explained (0 to 1, higher is better)
r2 = r2_score(y_test, y_pred)

# Mean Absolute Percentage Error
mape = mean_absolute_percentage_error(y_test, y_pred)
```

---

## Linear Regression

### What is Linear Regression?

Linear Regression models the relationship between input features and a continuous target variable using a linear equation.

**Equation:**
$$y = \beta_0 + \beta_1x_1 + \beta_2x_2 + ... + \beta_nx_n + \epsilon$$

Where:
- $y$ = predicted value
- $\beta_0$ = intercept
- $\beta_i$ = coefficients
- $x_i$ = features
- $\epsilon$ = error term

### When to Use Linear Regression?

**Use When:**
- ✅ Relationship between features and target is linear
- ✅ Target variable is continuous
- ✅ Features are independent (no multicollinearity)
- ✅ Need interpretable model
- ✅ Small to medium datasets

**Don't Use When:**
- ❌ Non-linear relationships
- ❌ Target variable is categorical
- ❌ High multicollinearity
- ❌ Outliers heavily affect the model

### Assumptions

1. **Linearity:** Linear relationship between X and y
2. **Independence:** Observations are independent
3. **Homoscedasticity:** Constant variance of errors
4. **Normality:** Errors are normally distributed
5. **No Multicollinearity:** Features are not highly correlated

### Implementation

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Generate sample data
np.random.seed(42)
X = np.random.rand(100, 1) * 10  # 100 samples, 1 feature
y = 2.5 * X.squeeze() + 5 + np.random.randn(100) * 2  # y = 2.5x + 5 + noise

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate
print(f'Coefficient: {model.coef_[0]:.4f}')
print(f'Intercept: {model.intercept_:.4f}')
print(f'R² Score: {r2_score(y_test, y_pred):.4f}')
print(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}')

# Visualize
plt.scatter(X_test, y_test, color='blue', label='Actual')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Predicted')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.title('Linear Regression')
plt.show()
```

### Multiple Linear Regression

```python
# Multiple features
from sklearn.datasets import make_regression

# Generate data with multiple features
X, y = make_regression(n_samples=100, n_features=5, noise=10, random_state=42)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate
print(f'Coefficients: {model.coef_}')
print(f'Intercept: {model.intercept_:.4f}')
print(f'R² Score: {r2_score(y_test, y_pred):.4f}')
```

### Regularization (Ridge & Lasso)

**Ridge Regression (L2 Regularization):**
- Adds penalty: $\lambda \sum \beta_i^2$
- Reduces magnitude of coefficients
- Good when many features are correlated

```python
from sklearn.linear_model import Ridge

# Ridge regression
ridge = Ridge(alpha=1.0)  # alpha = regularization strength
ridge.fit(X_train, y_train)
y_pred_ridge = ridge.predict(X_test)

print(f'Ridge R² Score: {r2_score(y_test, y_pred_ridge):.4f}')
```

**Lasso Regression (L1 Regularization):**
- Adds penalty: $\lambda \sum |\beta_i|$
- Can reduce coefficients to zero (feature selection)
- Good for sparse models

```python
from sklearn.linear_model import Lasso

# Lasso regression
lasso = Lasso(alpha=1.0)
lasso.fit(X_train, y_train)
y_pred_lasso = lasso.predict(X_test)

print(f'Lasso R² Score: {r2_score(y_test, y_pred_lasso):.4f}')
print(f'Non-zero coefficients: {np.sum(lasso.coef_ != 0)}')
```

**ElasticNet (L1 + L2):**
```python
from sklearn.linear_model import ElasticNet

# ElasticNet
elastic = ElasticNet(alpha=1.0, l1_ratio=0.5)  # l1_ratio: mix of L1 and L2
elastic.fit(X_train, y_train)
y_pred_elastic = elastic.predict(X_test)

print(f'ElasticNet R² Score: {r2_score(y_test, y_pred_elastic):.4f}')
```

### Polynomial Regression

```python
from sklearn.preprocessing import PolynomialFeatures

# Generate non-linear data
X = np.random.rand(100, 1) * 10
y = 0.5 * X.squeeze()**2 + 2 * X.squeeze() + 5 + np.random.randn(100) * 5

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create polynomial features (degree=2)
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Train model
model = LinearRegression()
model.fit(X_train_poly, y_train)

# Predictions
y_pred = model.predict(X_test_poly)

print(f'Polynomial R² Score: {r2_score(y_test, y_pred):.4f}')
```

### Real-World Example: House Price Prediction

```python
# Example: Predicting house prices
data = pd.DataFrame({
    'size': [1400, 1600, 1700, 1875, 1100, 1550, 2350, 2450, 1425, 1700],
    'bedrooms': [3, 3, 2, 4, 2, 3, 4, 4, 3, 3],
    'age': [10, 15, 20, 5, 25, 8, 3, 2, 12, 18],
    'price': [245000, 312000, 279000, 308000, 199000, 219000, 405000, 324000, 319000, 255000]
})

# Features and target
X = data[['size', 'bedrooms', 'age']]
y = data['price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Coefficients
print('Coefficients:')
for feature, coef in zip(X.columns, model.coef_):
    print(f'  {feature}: {coef:.2f}')
print(f'Intercept: {model.intercept_:.2f}')

# Prediction for new house
new_house = [[1800, 3, 10]]  # 1800 sqft, 3 bedrooms, 10 years old
predicted_price = model.predict(new_house)
print(f'Predicted price: ${predicted_price[0]:,.2f}')
```

### Pros and Cons

**Pros:**
- ✅ Simple and interpretable
- ✅ Fast to train
- ✅ Works well with linear relationships
- ✅ Low computational cost
- ✅ Good for small datasets

**Cons:**
- ❌ Assumes linearity
- ❌ Sensitive to outliers
- ❌ Poor with non-linear data
- ❌ Assumes feature independence
- ❌ Can't capture complex patterns

---

## Logistic Regression

### What is Logistic Regression?

Logistic Regression is used for **binary classification** (0 or 1, Yes or No). Despite the name "regression", it's a classification algorithm.

**Equation:**
$$P(y=1|x) = \frac{1}{1 + e^{-(\beta_0 + \beta_1x_1 + ... + \beta_nx_n)}}$$

This is the **sigmoid function** that maps any value to a probability between 0 and 1.

### When to Use Logistic Regression?

**Use When:**
- ✅ Binary classification (2 classes)
- ✅ Need probability estimates
- ✅ Linear decision boundary
- ✅ Features are independent
- ✅ Need interpretable model

**Don't Use When:**
- ❌ Multi-class classification (use softmax/multinomial)
- ❌ Non-linear decision boundary
- ❌ High multicollinearity
- ❌ Very large datasets (slower than tree-based)

### Implementation

```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve
)
import matplotlib.pyplot as plt

# Generate binary classification data
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    random_state=42
)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]  # Probability of class 1

# Evaluate
print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print(f'Precision: {precision_score(y_test, y_pred):.4f}')
print(f'Recall: {recall_score(y_test, y_pred):.4f}')
print(f'F1-Score: {f1_score(y_test, y_pred):.4f}')
print(f'ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}')

print('\nConfusion Matrix:')
print(confusion_matrix(y_test, y_pred))

print('\nClassification Report:')
print(classification_report(y_test, y_pred))
```

### Sigmoid Function Visualization

```python
# Visualize sigmoid function
z = np.linspace(-10, 10, 100)
sigmoid = 1 / (1 + np.exp(-z))

plt.figure(figsize=(10, 6))
plt.plot(z, sigmoid)
plt.axhline(y=0.5, color='r', linestyle='--', label='Decision boundary (0.5)')
plt.xlabel('z (linear combination)')
plt.ylabel('Probability')
plt.title('Sigmoid Function')
plt.grid(True)
plt.legend()
plt.show()
```

### ROC Curve

```python
# Plot ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = roc_auc_score(y_test, y_pred_proba)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, 
         label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.grid(True)
plt.show()
```

### Multi-class Classification

```python
from sklearn.datasets import load_iris

# Load iris dataset (3 classes)
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Multinomial logistic regression
model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print('\nClassification Report:')
print(classification_report(y_test, y_pred, target_names=iris.target_names))
```

### Real-World Example: Email Spam Detection

```python
# Example: Email spam classification
data = pd.DataFrame({
    'num_words': [100, 500, 200, 800, 150, 600, 300, 450, 250, 700],
    'num_links': [5, 15, 3, 20, 2, 18, 4, 12, 3, 22],
    'has_urgent': [1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    'num_capitals': [10, 50, 5, 80, 3, 60, 8, 45, 6, 75],
    'spam': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 0 = not spam, 1 = spam
})

# Features and target
X = data[['num_words', 'num_links', 'has_urgent', 'num_capitals']]
y = data['spam']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

# New email
new_email = [[400, 10, 1, 30]]  # 400 words, 10 links, has urgent, 30 capitals
spam_probability = model.predict_proba(new_email)[0, 1]
print(f'Spam probability: {spam_probability:.2%}')

if spam_probability > 0.5:
    print('This email is likely SPAM')
else:
    print('This email is likely NOT SPAM')
```

### Feature Importance

```python
# Get feature coefficients
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'coefficient': model.coef_[0]
}).sort_values('coefficient', ascending=False)

print(feature_importance)

# Visualize
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'], feature_importance['coefficient'])
plt.xlabel('Coefficient')
plt.title('Feature Importance in Logistic Regression')
plt.tight_layout()
plt.show()
```

### Regularization

```python
# L2 regularization (default)
model_l2 = LogisticRegression(penalty='l2', C=1.0)  # C = 1/lambda
model_l2.fit(X_train, y_train)

# L1 regularization (feature selection)
model_l1 = LogisticRegression(penalty='l1', solver='liblinear', C=1.0)
model_l1.fit(X_train, y_train)

# No regularization
model_none = LogisticRegression(penalty=None, max_iter=1000)
model_none.fit(X_train, y_train)

# Compare
print(f'L2 Accuracy: {model_l2.score(X_test, y_test):.4f}')
print(f'L1 Accuracy: {model_l1.score(X_test, y_test):.4f}')
print(f'No regularization Accuracy: {model_none.score(X_test, y_test):.4f}')
```

### Pros and Cons

**Pros:**
- ✅ Simple and interpretable
- ✅ Provides probability estimates
- ✅ Fast to train
- ✅ Works well with linearly separable data
- ✅ Less prone to overfitting with regularization
- ✅ Can handle multi-class (multinomial)

**Cons:**
- ❌ Assumes linear decision boundary
- ❌ Sensitive to outliers
- ❌ Poor with non-linear data
- ❌ Requires feature scaling
- ❌ Assumes feature independence

---

## Decision Trees

### What is a Decision Tree?

A Decision Tree is a tree-like model that makes decisions by splitting data based on feature values. It asks a series of yes/no questions to reach a prediction.

**Example:**
```
                  Age > 30?
                 /         \
              Yes           No
             /               \
       Income > 50K?      Buy = No
        /         \
      Yes         No
      /            \
  Buy = Yes     Buy = No
```

### How It Works

1. **Select best feature** to split (using Gini/Entropy)
2. **Split data** based on threshold
3. **Repeat** for each subset
4. **Stop** when reaching stopping criterion

**Splitting Criteria:**

**Gini Impurity:**
$$Gini = 1 - \sum_{i=1}^{n} p_i^2$$

**Entropy (Information Gain):**
$$Entropy = -\sum_{i=1}^{n} p_i \log_2(p_i)$$

Where $p_i$ is probability of class $i$

### When to Use Decision Trees?

**Use When:**
- ✅ Need interpretable model
- ✅ Non-linear relationships
- ✅ Mixed feature types (categorical + numerical)
- ✅ Don't need feature scaling
- ✅ Can handle missing values
- ✅ Need feature importance

**Don't Use When:**
- ❌ Very small datasets (overfitting)
- ❌ Need high accuracy (use ensemble methods)
- ❌ Linear relationships (use linear models)
- ❌ Production with high stability requirements

### Implementation - Classification

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

# Load data
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Decision Tree Classifier
model = DecisionTreeClassifier(
    criterion='gini',      # or 'entropy'
    max_depth=3,           # Maximum depth of tree
    min_samples_split=2,   # Minimum samples to split
    min_samples_leaf=1,    # Minimum samples in leaf
    random_state=42
)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')

# Visualize tree
plt.figure(figsize=(20, 10))
plot_tree(
    model,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True,
    rounded=True
)
plt.title('Decision Tree Visualization')
plt.show()
```

### Implementation - Regression

```python
from sklearn.tree import DecisionTreeRegressor

# Generate regression data
X = np.sort(5 * np.random.rand(80, 1), axis=0)
y = np.sin(X).ravel() + np.random.randn(80) * 0.1

# Train Decision Tree Regressor
model = DecisionTreeRegressor(max_depth=5, random_state=42)
model.fit(X, y)

# Predictions
X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
y_pred = model.predict(X_test)

# Visualize
plt.figure(figsize=(10, 6))
plt.scatter(X, y, s=20, edgecolor="black", c="darkorange", label="data")
plt.plot(X_test, y_pred, color="cornflowerblue", linewidth=2, label="prediction")
plt.xlabel("X")
plt.ylabel("y")
plt.title("Decision Tree Regression")
plt.legend()
plt.show()
```

### Feature Importance

```python
# Get feature importance
feature_importance = pd.DataFrame({
    'feature': iris.feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance)

# Visualize
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'], feature_importance['importance'])
plt.xlabel('Importance')
plt.title('Feature Importance in Decision Tree')
plt.tight_layout()
plt.show()
```

### Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [3, 5, 7, 10, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Grid search
grid_search = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

print(f'Best parameters: {grid_search.best_params_}')
print(f'Best score: {grid_search.best_score_:.4f}')

# Best model
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
print(f'Test accuracy: {accuracy_score(y_test, y_pred):.4f}')
```

### Real-World Example: Customer Churn Prediction

```python
# Example: Predicting customer churn
data = pd.DataFrame({
    'age': [25, 45, 35, 52, 28, 41, 38, 48, 33, 55],
    'tenure': [2, 10, 5, 15, 3, 8, 6, 12, 4, 18],
    'monthly_charges': [50, 80, 65, 90, 55, 75, 70, 85, 60, 95],
    'total_charges': [100, 800, 325, 1350, 165, 600, 420, 1020, 240, 1710],
    'contract_type': [0, 2, 1, 2, 0, 1, 1, 2, 0, 2],  # 0=Month-to-month, 1=One year, 2=Two year
    'churn': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0]  # 1 = churned, 0 = retained
})

X = data[['age', 'tenure', 'monthly_charges', 'total_charges', 'contract_type']]
y = data['churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Feature importance
print('Feature Importance:')
for feature, importance in zip(X.columns, model.feature_importances_):
    print(f'  {feature}: {importance:.4f}')

# Predict for new customer
new_customer = [[30, 6, 70, 420, 1]]  # 30 years old, 6 months tenure, etc.
churn_prob = model.predict_proba(new_customer)[0, 1]
print(f'\nChurn probability: {churn_prob:.2%}')
```

### Preventing Overfitting

```python
# Overfitting: Too complex tree
model_overfit = DecisionTreeClassifier(random_state=42)  # No constraints
model_overfit.fit(X_train, y_train)

# Regularized: Controlled complexity
model_regularized = DecisionTreeClassifier(
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)
model_regularized.fit(X_train, y_train)

# Compare
print(f'Overfit - Train: {model_overfit.score(X_train, y_train):.4f}, Test: {model_overfit.score(X_test, y_test):.4f}')
print(f'Regularized - Train: {model_regularized.score(X_train, y_train):.4f}, Test: {model_regularized.score(X_test, y_test):.4f}')
```

### Pros and Cons

**Pros:**
- ✅ Easy to understand and interpret
- ✅ Visualizable
- ✅ No feature scaling required
- ✅ Handles non-linear relationships
- ✅ Handles mixed data types
- ✅ Can handle missing values
- ✅ Feature importance

**Cons:**
- ❌ Prone to overfitting
- ❌ Unstable (small data changes → different tree)
- ❌ Biased towards features with more levels
- ❌ Can create overly complex trees
- ❌ Not as accurate as ensemble methods

---

## Random Forest

### What is Random Forest?

Random Forest is an **ensemble learning method** that combines multiple decision trees to create a more powerful and stable model. It's like asking multiple experts and taking the majority vote.

**Key Concept:**
- Builds many decision trees (100-1000)
- Each tree is trained on random subset of data (bootstrapping)
- Each split uses random subset of features
- Final prediction: Average (regression) or Majority vote (classification)

### How It Works

```
Dataset
│
├─→ Bootstrap Sample 1 → Decision Tree 1 → Prediction 1
├─→ Bootstrap Sample 2 → Decision Tree 2 → Prediction 2
├─→ Bootstrap Sample 3 → Decision Tree 3 → Prediction 3
├─→ ...
└─→ Bootstrap Sample N → Decision Tree N → Prediction N
                                              │
                                              ▼
                                    Aggregate Predictions
                                    (Vote or Average)
                                              │
                                              ▼
                                      Final Prediction
```

### When to Use Random Forest?

**Use When:**
- ✅ Need high accuracy
- ✅ Non-linear relationships
- ✅ Mixed feature types
- ✅ Large datasets
- ✅ Need feature importance
- ✅ Robust to outliers
- ✅ Prevent overfitting

**Don't Use When:**
- ❌ Need interpretability (use single decision tree)
- ❌ Real-time predictions (slower than linear models)
- ❌ Very limited computational resources
- ❌ Linear relationships (use linear models)

### Why Random Forest Over Decision Tree?

| Aspect | Decision Tree | Random Forest |
|--------|--------------|---------------|
| **Accuracy** | Lower | Higher |
| **Overfitting** | High | Low |
| **Stability** | Unstable | Stable |
| **Variance** | High | Low |
| **Speed** | Fast | Slower |
| **Interpretability** | High | Low |

### Implementation - Classification

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report

# Generate data
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,       # Number of trees
    max_depth=10,           # Maximum depth of each tree
    min_samples_split=2,    # Minimum samples to split
    min_samples_leaf=1,     # Minimum samples in leaf
    max_features='sqrt',    # Number of features to consider (sqrt(n_features))
    bootstrap=True,         # Use bootstrapping
    oob_score=True,         # Out-of-bag score
    n_jobs=-1,              # Use all CPU cores
    random_state=42
)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate
print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print(f'OOB Score: {model.oob_score_:.4f}')  # Out-of-bag score

# Cross-validation
cv_scores = cross_val_score(model, X_train, y_train, cv=5)
print(f'CV Scores: {cv_scores}')
print(f'Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})')
```

### Implementation - Regression

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression

# Generate regression data
X, y = make_regression(
    n_samples=1000,
    n_features=10,
    noise=10,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest Regressor
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate
print(f'R² Score: {r2_score(y_test, y_pred):.4f}')
print(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}')
```

### Feature Importance

```python
# Get feature importance
feature_importance = pd.DataFrame({
    'feature': [f'feature_{i}' for i in range(X.shape[1])],
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance.head(10))

# Visualize
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'][:10], feature_importance['importance'][:10])
plt.xlabel('Importance')
plt.title('Top 10 Feature Importances')
plt.tight_layout()
plt.show()
```

### Hyperparameter Tuning

```python
from sklearn.model_selection import RandomizedSearchCV

# Define parameter distribution
param_dist = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [5, 10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', None]
}

# Randomized search
random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_distributions=param_dist,
    n_iter=50,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)
random_search.fit(X_train, y_train)

print(f'Best parameters: {random_search.best_params_}')
print(f'Best score: {random_search.best_score_:.4f}')

# Best model
best_model = random_search.best_estimator_
y_pred = best_model.predict(X_test)
print(f'Test accuracy: {accuracy_score(y_test, y_pred):.4f}')
```

### Real-World Example: Credit Card Fraud Detection

```python
# Example: Detecting fraudulent transactions
data = pd.DataFrame({
    'amount': [50.0, 2500.0, 100.0, 5000.0, 75.0, 3000.0, 150.0, 4500.0],
    'hour': [10, 2, 14, 3, 9, 1, 11, 4],
    'distance_from_home': [5, 500, 10, 800, 3, 600, 8, 750],
    'distance_from_last_transaction': [2, 450, 5, 700, 1, 550, 4, 680],
    'is_chip_transaction': [1, 0, 1, 0, 1, 0, 1, 0],
    'fraud': [0, 1, 0, 1, 0, 1, 0, 1]  # 1 = fraud, 0 = legitimate
})

X = data.drop('fraud', axis=1)
y = data['fraud']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    class_weight='balanced',  # Handle imbalanced data
    random_state=42
)
model.fit(X_train, y_train)

# Feature importance
print('Feature Importance:')
for feature, importance in sorted(
    zip(X.columns, model.feature_importances_),
    key=lambda x: x[1],
    reverse=True
):
    print(f'  {feature}: {importance:.4f}')

# Predict fraud probability
new_transaction = [[3000, 3, 500, 450, 0]]
fraud_prob = model.predict_proba(new_transaction)[0, 1]
print(f'\nFraud probability: {fraud_prob:.2%}')

if fraud_prob > 0.7:
    print('HIGH RISK - Flag for review')
elif fraud_prob > 0.3:
    print('MEDIUM RISK - Additional verification needed')
else:
    print('LOW RISK - Approve')
```

### Out-of-Bag (OOB) Score

```python
# OOB score: Estimate test error using out-of-bag samples
model = RandomForestClassifier(
    n_estimators=100,
    oob_score=True,
    random_state=42
)
model.fit(X_train, y_train)

print(f'OOB Score: {model.oob_score_:.4f}')
print(f'Test Score: {model.score(X_test, y_test):.4f}')

# OOB score is a good estimate of test performance
```

### Pros and Cons

**Pros:**
- ✅ High accuracy
- ✅ Reduces overfitting
- ✅ Handles non-linear relationships
- ✅ No feature scaling required
- ✅ Robust to outliers
- ✅ Feature importance
- ✅ Works with mixed data types
- ✅ Parallel training (fast)

**Cons:**
- ❌ Less interpretable than single tree
- ❌ Slower predictions than simple models
- ❌ Larger memory footprint
- ❌ Can overfit on noisy data
- ❌ Biased towards features with many categories

---

## Support Vector Machines (SVM)

### What is SVM?

Support Vector Machine finds the **optimal hyperplane** that best separates classes with maximum margin.

**Key Concepts:**
- **Hyperplane:** Decision boundary that separates classes
- **Support Vectors:** Data points closest to hyperplane
- **Margin:** Distance between hyperplane and support vectors
- **Kernel Trick:** Transform data to higher dimensions for non-linear separation

```
Class A                    Class B
   •                          •
     •                      •
       •    |              •
         •  |  Margin    •
      SV → •|----------|• ← SV
           •|  Hyper-  |•
         •  |  plane   |  •
       •    |            •
     •                      •
   •                          •
```

### When to Use SVM?

**Use When:**
- ✅ Binary or multi-class classification
- ✅ High-dimensional data (many features)
- ✅ Clear margin of separation
- ✅ Small to medium datasets
- ✅ Need robust model (outlier resistant with soft margin)
- ✅ Non-linear relationships (with kernel)

**Don't Use When:**
- ❌ Very large datasets (slow training)
- ❌ Many overlapping classes
- ❌ Need probability estimates (requires calibration)
- ❌ Need interpretability
- ❌ Multi-class with many classes (slower)

### Kernel Types

**1. Linear Kernel:** For linearly separable data
$$K(x, x') = x \cdot x'$$

**2. RBF (Radial Basis Function) Kernel:** Most common for non-linear
$$K(x, x') = e^{-\gamma ||x - x'||^2}$$

**3. Polynomial Kernel:** For polynomial relationships
$$K(x, x') = (\gamma x \cdot x' + r)^d$$

**4. Sigmoid Kernel:** Similar to neural networks
$$K(x, x') = \tanh(\gamma x \cdot x' + r)$$

### Implementation - Linear SVM

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification

# Generate linearly separable data
X, y = make_classification(
    n_samples=200,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_clusters_per_class=1,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Feature scaling (IMPORTANT for SVM!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Linear SVM
model = SVC(kernel='linear', C=1.0, random_state=42)
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)

print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print(f'Number of support vectors: {len(model.support_vectors_)}')
```

### Visualize Decision Boundary

```python
def plot_decision_boundary(model, X, y, title):
    # Create mesh
    h = 0.02  # Step size
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    # Predict on mesh
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.contourf(xx, yy, Z, alpha=0.3)
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k')
    
    # Plot support vectors
    plt.scatter(model.support_vectors_[:, 0],
                model.support_vectors_[:, 1],
                s=200, linewidth=1, facecolors='none',
                edgecolors='red', label='Support Vectors')
    
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(title)
    plt.legend()
    plt.show()

# Visualize
plot_decision_boundary(model, X_train_scaled, y_train, 'Linear SVM Decision Boundary')
```

### Implementation - RBF Kernel (Non-linear)

```python
# Generate non-linearly separable data
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=200, noise=0.15, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train RBF SVM
model_rbf = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
model_rbf.fit(X_train_scaled, y_train)

# Predictions
y_pred = model_rbf.predict(X_test_scaled)

print(f'RBF SVM Accuracy: {accuracy_score(y_test, y_pred):.4f}')

# Visualize
plot_decision_boundary(model_rbf, X_train_scaled, y_train, 'RBF SVM Decision Boundary')
```

### Hyperparameters

**C (Regularization):**
- **Large C:** Small margin, low bias, high variance (may overfit)
- **Small C:** Large margin, high bias, low variance (may underfit)

**Gamma (RBF kernel):**
- **Large gamma:** Close data points influence (may overfit)
- **Small gamma:** Far data points influence (may underfit)

```python
# Compare different C values
for c in [0.1, 1.0, 10.0]:
    model = SVC(kernel='linear', C=c, random_state=42)
    model.fit(X_train_scaled, y_train)
    print(f'C={c}: Accuracy = {model.score(X_test_scaled, y_test):.4f}')

# Compare different gamma values (RBF)
for gamma in [0.1, 1.0, 10.0]:
    model = SVC(kernel='rbf', C=1.0, gamma=gamma, random_state=42)
    model.fit(X_train_scaled, y_train)
    print(f'gamma={gamma}: Accuracy = {model.score(X_test_scaled, y_test):.4f}')
```

### Grid Search for Best Parameters

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [0.001, 0.01, 0.1, 1],
    'kernel': ['rbf', 'poly', 'sigmoid']
}

# Grid search
grid_search = GridSearchCV(
    SVC(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid_search.fit(X_train_scaled, y_train)

print(f'Best parameters: {grid_search.best_params_}')
print(f'Best score: {grid_search.best_score_:.4f}')

# Best model
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test_scaled)
print(f'Test accuracy: {accuracy_score(y_test, y_pred):.4f}')
```

### Real-World Example: Image Classification (Handwritten Digits)

```python
from sklearn.datasets import load_digits

# Load digits dataset
digits = load_digits()
X, y = digits.data, digits.target

# Visualize some digits
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for i, ax in enumerate(axes.flat):
    ax.imshow(digits.images[i], cmap='gray')
    ax.set_title(f'Label: {digits.target[i]}')
    ax.axis('off')
plt.tight_layout()
plt.show()

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train SVM
model = SVC(kernel='rbf', C=10, gamma=0.001, random_state=42)
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)

print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print('\nClassification Report:')
print(classification_report(y_test, y_pred))

# Confusion matrix
from sklearn.metrics import ConfusionMatrixDisplay
ConfusionMatrixDisplay.from_estimator(model, X_test_scaled, y_test)
plt.title('Confusion Matrix')
plt.show()
```

### SVM Regression (SVR)

```python
from sklearn.svm import SVR

# Generate regression data
X = np.sort(5 * np.random.rand(100, 1), axis=0)
y = np.sin(X).ravel() + np.random.randn(100) * 0.1

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale data
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)
y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1)).ravel()

# Train SVR
model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
model.fit(X_train_scaled, y_train_scaled)

# Predictions
y_pred_scaled = model.predict(X_test_scaled)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()

print(f'R² Score: {r2_score(y_test, y_pred):.4f}')

# Visualize
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='blue', label='Actual')
plt.scatter(X_test, y_pred, color='red', label='Predicted')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Support Vector Regression')
plt.legend()
plt.show()
```

### Pros and Cons

**Pros:**
- ✅ Effective in high dimensions
- ✅ Memory efficient (uses support vectors)
- ✅ Works well with clear margin
- ✅ Versatile (different kernels)
- ✅ Robust to outliers (with soft margin)

**Cons:**
- ❌ Slow on large datasets (O(n²) to O(n³))
- ❌ Sensitive to feature scaling
- ❌ No direct probability estimates
- ❌ Hard to interpret
- ❌ Choosing right kernel is tricky
- ❌ Not suitable for multi-class (one-vs-one approach)

---

## K-Nearest Neighbors (KNN)

### What is KNN?

K-Nearest Neighbors is a **lazy learning** algorithm that classifies based on the majority class of K nearest neighbors.

**How it works:**
1. Choose number K of neighbors
2. Calculate distance to all training points
3. Find K nearest neighbors
4. Take majority vote (classification) or average (regression)

```
New Point (?)
   │
   ├─ Find K=5 nearest neighbors
   │
   ├─ 3 are Class A (●)
   └─ 2 are Class B (■)
   
Prediction: Class A (majority)
```

### When to Use KNN?

**Use When:**
- ✅ Small to medium datasets
- ✅ Need simple baseline model
- ✅ Non-linear decision boundaries
- ✅ Multi-class classification
- ✅ Data is not too high-dimensional

**Don't Use When:**
- ❌ Large datasets (slow predictions)
- ❌ High-dimensional data (curse of dimensionality)
- ❌ Imbalanced classes
- ❌ Need fast predictions
- ❌ Features have different scales

### Distance Metrics

**1. Euclidean Distance (default):**
$$d(x, x') = \sqrt{\sum_{i=1}^{n} (x_i - x'_i)^2}$$

**2. Manhattan Distance:**
$$d(x, x') = \sum_{i=1}^{n} |x_i - x'_i|$$

**3. Minkowski Distance:**
$$d(x, x') = \left(\sum_{i=1}^{n} |x_i - x'_i|^p\right)^{1/p}$$

### Implementation - Classification

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification

# Generate data
X, y = make_classification(
    n_samples=200,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_clusters_per_class=1,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Feature scaling (IMPORTANT for KNN!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train KNN
model = KNeighborsClassifier(
    n_neighbors=5,
    weights='uniform',  # or 'distance' (weighted by inverse distance)
    metric='euclidean',
    n_jobs=-1
)
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)

print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
```

### Finding Optimal K

```python
# Test different K values
k_values = range(1, 31)
train_scores = []
test_scores = []

for k in k_values:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train_scaled, y_train)
    
    train_scores.append(model.score(X_train_scaled, y_train))
    test_scores.append(model.score(X_test_scaled, y_test))

# Plot
plt.figure(figsize=(10, 6))
plt.plot(k_values, train_scores, label='Train Score')
plt.plot(k_values, test_scores, label='Test Score')
plt.xlabel('K (Number of Neighbors)')
plt.ylabel('Accuracy')
plt.title('KNN: Finding Optimal K')
plt.legend()
plt.grid(True)
plt.show()

# Best K
best_k = k_values[np.argmax(test_scores)]
print(f'Best K: {best_k}')
print(f'Best Test Score: {max(test_scores):.4f}')
```

### Implementation - Regression

```python
from sklearn.neighbors import KNeighborsRegressor

# Generate regression data
X = np.sort(5 * np.random.rand(80, 1), axis=0)
y = np.sin(X).ravel() + np.random.randn(80) * 0.1

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train KNN Regressor
model = KNeighborsRegressor(n_neighbors=5, weights='distance')
model.fit(X_train, y_train)

# Predictions
X_test_dense = np.linspace(0, 5, 500)[:, np.newaxis]
y_pred = model.predict(X_test_dense)

# Visualize
plt.figure(figsize=(10, 6))
plt.scatter(X_train, y_train, color='blue', label='Train')
plt.plot(X_test_dense, y_pred, color='red', linewidth=2, label='Prediction')
plt.xlabel('X')
plt.ylabel('y')
plt.title('K-Nearest Neighbors Regression')
plt.legend()
plt.show()

# Evaluate
y_test_pred = model.predict(X_test)
print(f'R² Score: {r2_score(y_test, y_test_pred):.4f}')
```

### Weighted KNN

```python
# Uniform weights: All neighbors have equal vote
model_uniform = KNeighborsClassifier(n_neighbors=5, weights='uniform')
model_uniform.fit(X_train_scaled, y_train)

# Distance weights: Closer neighbors have more influence
model_distance = KNeighborsClassifier(n_neighbors=5, weights='distance')
model_distance.fit(X_train_scaled, y_train)

print(f'Uniform weights accuracy: {model_uniform.score(X_test_scaled, y_test):.4f}')
print(f'Distance weights accuracy: {model_distance.score(X_test_scaled, y_test):.4f}')
```

### Real-World Example: Iris Flower Classification

```python
from sklearn.datasets import load_iris

# Load iris dataset
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Find best K
best_k = 5
best_score = 0

for k in range(1, 21):
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train_scaled, y_train)
    score = model.score(X_test_scaled, y_test)
    
    if score > best_score:
        best_score = score
        best_k = k

print(f'Best K: {best_k}, Accuracy: {best_score:.4f}')

# Train final model
final_model = KNeighborsClassifier(n_neighbors=best_k)
final_model.fit(X_train_scaled, y_train)

# Predict new flower
new_flower = [[5.1, 3.5, 1.4, 0.2]]  # Sepal length, sepal width, petal length, petal width
new_flower_scaled = scaler.transform(new_flower)
prediction = final_model.predict(new_flower_scaled)
prediction_proba = final_model.predict_proba(new_flower_scaled)

print(f'\nPredicted class: {iris.target_names[prediction[0]]}')
print('Probabilities:')
for name, prob in zip(iris.target_names, prediction_proba[0]):
    print(f'  {name}: {prob:.2%}')
```

### Curse of Dimensionality

```python
# Demonstrate curse of dimensionality
from sklearn.datasets import make_classification

dimensions = [2, 10, 50, 100, 200]
accuracies = []

for n_features in dimensions:
    X, y = make_classification(
        n_samples=500,
        n_features=n_features,
        n_informative=n_features,
        random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train_scaled, y_train)
    
    accuracies.append(model.score(X_test_scaled, y_test))

# Plot
plt.figure(figsize=(10, 6))
plt.plot(dimensions, accuracies, marker='o')
plt.xlabel('Number of Dimensions')
plt.ylabel('Accuracy')
plt.title('Curse of Dimensionality in KNN')
plt.grid(True)
plt.show()
```

### Pros and Cons

**Pros:**
- ✅ Simple to understand and implement
- ✅ No training phase (lazy learning)
- ✅ Naturally handles multi-class
- ✅ Non-parametric (no assumptions)
- ✅ Can update easily (add new data)

**Cons:**
- ❌ Slow predictions (O(n) for each prediction)
- ❌ High memory usage (stores all training data)
- ❌ Sensitive to feature scaling
- ❌ Curse of dimensionality
- ❌ Sensitive to outliers
- ❌ Imbalanced data issues

---

## Naive Bayes

### What is Naive Bayes?

Naive Bayes is a probabilistic classifier based on **Bayes' Theorem** with the "naive" assumption that features are independent.

**Bayes' Theorem:**
$$P(y|x) = \frac{P(x|y) \cdot P(y)}{P(x)}$$

Where:
- $P(y|x)$ = Posterior probability (probability of class y given features x)
- $P(x|y)$ = Likelihood (probability of features x given class y)
- $P(y)$ = Prior probability (probability of class y)
- $P(x)$ = Evidence (probability of features x)

**"Naive" Assumption:**
Features are conditionally independent given the class:
$$P(x_1, x_2, ..., x_n | y) = P(x_1|y) \cdot P(x_2|y) \cdot ... \cdot P(x_n|y)$$

### When to Use Naive Bayes?

**Use When:**
- ✅ Text classification (spam detection, sentiment analysis)
- ✅ Small to medium datasets
- ✅ Need fast training and prediction
- ✅ Features are relatively independent
- ✅ Categorical features
- ✅ Need probabilistic predictions

**Don't Use When:**
- ❌ Features are highly correlated
- ❌ Need high accuracy (use ensemble methods)
- ❌ Continuous features with complex distributions
- ❌ Zero-frequency problem (without smoothing)

### Types of Naive Bayes

**1. Gaussian Naive Bayes:** Continuous features (assumes Gaussian distribution)
**2. Multinomial Naive Bayes:** Discrete features (word counts, frequencies)
**3. Bernoulli Naive Bayes:** Binary features (presence/absence)

### Implementation - Gaussian Naive Bayes

```python
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import load_iris

# Load data
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Gaussian Naive Bayes
model = GaussianNB()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print('\nClassification Report:')
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# Show probabilities for first few samples
print('\nProbabilities for first 5 test samples:')
for i in range(5):
    print(f'Sample {i}: {y_pred_proba[i]}')
    print(f'  Predicted: {iris.target_names[y_pred[i]]}')
    print(f'  Actual: {iris.target_names[y_test.iloc[i] if hasattr(y_test, "iloc") else y_test[i]]}')
```

### Implementation - Multinomial Naive Bayes (Text Classification)

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

# Example: Email spam classification
emails = [
    "Win free money now!!!",
    "Meeting at 3pm tomorrow",
    "Get rich quick scheme",
    "Project deadline next week",
    "Claim your prize today",
    "Lunch meeting with team",
    "Limited time offer!!!",
    "Please review the document",
]

labels = [1, 0, 1, 0, 1, 0, 1, 0]  # 1 = spam, 0 = not spam

# Convert text to numerical features
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.25, random_state=42
)

# Train Multinomial Naive Bayes
model = MultinomialNB(alpha=1.0)  # alpha = Laplace smoothing
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')

# Predict new email
new_emails = [
    "Congratulations! You won a prize",
    "Meeting notes from yesterday"
]
new_emails_vectorized = vectorizer.transform(new_emails)
predictions = model.predict(new_emails_vectorized)
probabilities = model.predict_proba(new_emails_vectorized)

for email, pred, prob in zip(new_emails, predictions, probabilities):
    spam_prob = prob[1]
    print(f'\nEmail: "{email}"')
    print(f'Prediction: {"SPAM" if pred == 1 else "NOT SPAM"}')
    print(f'Spam probability: {spam_prob:.2%}')
```

### Real-World Example: Sentiment Analysis

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Movie reviews dataset
reviews = [
    "This movie was excellent and amazing",
    "Terrible movie, waste of time",
    "Great acting and wonderful story",
    "Boring and poorly made film",
    "Loved every minute of it",
    "Worst movie I've ever seen",
    "Fantastic performances by all actors",
    "Disappointing and uninteresting",
    "Brilliant masterpiece",
    "Awful and unbearable to watch"
]

sentiments = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1 = positive, 0 = negative

# TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=50)
X = vectorizer.fit_transform(reviews)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, sentiments, test_size=0.2, random_state=42
)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict new reviews
new_reviews = [
    "Amazing film with great story",
    "Terrible acting and boring plot",
    "Absolutely loved it"
]

new_reviews_vectorized = vectorizer.transform(new_reviews)
predictions = model.predict(new_reviews_vectorized)
probabilities = model.predict_proba(new_reviews_vectorized)

for review, pred, prob in zip(new_reviews, predictions, probabilities):
    print(f'\nReview: "{review}"')
    print(f'Sentiment: {"POSITIVE" if pred == 1 else "NEGATIVE"}')
    print(f'Confidence: {max(prob):.2%}')
```

### Laplace Smoothing

```python
# Without smoothing (alpha=0) - may have zero-frequency problem
model_no_smooth = MultinomialNB(alpha=0.0)

# With Laplace smoothing (alpha=1) - handles zero-frequency
model_smooth = MultinomialNB(alpha=1.0)

# With custom smoothing
model_custom = MultinomialNB(alpha=0.5)

# Train and compare
for name, model in [('No smoothing', model_no_smooth), 
                     ('Laplace smoothing', model_smooth),
                     ('Custom smoothing', model_custom)]:
    try:
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        print(f'{name}: {score:.4f}')
    except:
        print(f'{name}: Failed (zero-frequency problem)')
```

### Feature Probabilities

```python
# Get feature log probabilities
feature_names = vectorizer.get_feature_names_out()
log_probs = model.feature_log_prob_

# Top features for each class
n_top = 5

for class_idx in range(len(model.classes_)):
    print(f'\nTop {n_top} features for class {model.classes_[class_idx]}:')
    top_indices = np.argsort(log_probs[class_idx])[-n_top:][::-1]
    
    for idx in top_indices:
        print(f'  {feature_names[idx]}: {np.exp(log_probs[class_idx][idx]):.4f}')
```

### Pros and Cons

**Pros:**
- ✅ Fast training and prediction
- ✅ Works well with small datasets
- ✅ Handles high-dimensional data
- ✅ Good for text classification
- ✅ Provides probability estimates
- ✅ Simple to implement
- ✅ Works well with categorical features

**Cons:**
- ❌ "Naive" assumption rarely holds
- ❌ Zero-frequency problem (needs smoothing)
- ❌ Not as accurate as other methods
- ❌ Assumes feature independence
- ❌ Poor with correlated features
- ❌ Sensitive to irrelevant features

---

## K-Means Clustering

### What is K-Means?

K-Means is an **unsupervised learning** algorithm that groups data into K clusters based on similarity.

**How it works:**
1. Choose K (number of clusters)
2. Randomly initialize K centroids
3. Assign each point to nearest centroid
4. Update centroids (mean of assigned points)
5. Repeat steps 3-4 until convergence

```
Iteration 1:           Iteration 2:           Converged:
• • •   • • •         • • •   • • •         ● ● ●   ○ ○ ○
  •   +   •             • +     ○               +     +
• • •   • • •         • • •   ○ ○ ○         ● ● ●   ○ ○ ○

+ = Centroids          Reassign points        Final clusters
```

### When to Use K-Means?

**Use When:**
- ✅ Need to group similar data points
- ✅ Customer segmentation
- ✅ Image compression
- ✅ Document clustering
- ✅ Anomaly detection (points far from centroids)
- ✅ Data preprocessing (feature creation)
- ✅ Spherical clusters

**Don't Use When:**
- ❌ Non-spherical clusters
- ❌ Different cluster sizes
- ❌ Different cluster densities
- ❌ Need hierarchical clustering
- ❌ Don't know K in advance

### Implementation - Basic K-Means

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# Generate sample data with 3 clusters
X, y_true = make_blobs(
    n_samples=300,
    centers=3,
    cluster_std=0.60,
    random_state=42
)

# Train K-Means
kmeans = KMeans(
    n_clusters=3,
    init='k-means++',  # Smart initialization
    n_init=10,         # Number of times to run with different seeds
    max_iter=300,      # Maximum iterations
    random_state=42
)
kmeans.fit(X)

# Get cluster labels and centroids
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

# Visualize
plt.figure(figsize=(10, 6))
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.6)
plt.scatter(centroids[:, 0], centroids[:, 1], 
            marker='X', s=200, c='red', edgecolors='black', linewidths=2)
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('K-Means Clustering')
plt.colorbar(label='Cluster')
plt.show()

print(f'Inertia (within-cluster sum of squares): {kmeans.inertia_:.2f}')
print(f'Number of iterations: {kmeans.n_iter_}')
```

### Finding Optimal K - Elbow Method

```python
# Test different K values
inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

# Plot elbow curve
plt.figure(figsize=(10, 6))
plt.plot(K_range, inertias, marker='o')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia (Within-Cluster Sum of Squares)')
plt.title('Elbow Method for Optimal K')
plt.grid(True)
plt.show()

# The "elbow" point indicates optimal K
```

### Finding Optimal K - Silhouette Score

```python
from sklearn.metrics import silhouette_score

# Calculate silhouette scores
silhouette_scores = []

for k in range(2, 11):  # K must be >= 2
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    silhouette_scores.append(score)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(range(2, 11), silhouette_scores, marker='o')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Analysis for Optimal K')
plt.grid(True)
plt.show()

# Best K has highest silhouette score
best_k = silhouette_scores.index(max(silhouette_scores)) + 2
print(f'Optimal K: {best_k}')
print(f'Silhouette Score: {max(silhouette_scores):.4f}')
```

### Real-World Example: Customer Segmentation

```python
# Example: E-commerce customer segmentation
customer_data = pd.DataFrame({
    'customer_id': range(1, 101),
    'total_purchases': np.random.randint(1, 50, 100),
    'avg_order_value': np.random.uniform(20, 200, 100),
    'days_since_last_purchase': np.random.randint(1, 365, 100),
    'customer_lifetime_value': np.random.uniform(100, 5000, 100)
})

# Select features for clustering
X = customer_data[['total_purchases', 'avg_order_value', 
                   'days_since_last_purchase', 'customer_lifetime_value']]

# Scale features (IMPORTANT!)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find optimal K
silhouette_scores = []
for k in range(2, 8):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    silhouette_scores.append(score)

optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2
print(f'Optimal number of segments: {optimal_k}')

# Train final model
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
customer_data['segment'] = kmeans.fit_predict(X_scaled)

# Analyze segments
print('\nSegment Analysis:')
segment_analysis = customer_data.groupby('segment').agg({
    'total_purchases': 'mean',
    'avg_order_value': 'mean',
    'days_since_last_purchase': 'mean',
    'customer_lifetime_value': 'mean'
})
print(segment_analysis)

# Segment interpretation
segment_names = {
    0: 'High-Value Frequent Buyers',
    1: 'Occasional Shoppers',
    2: 'At-Risk Customers',
    # Add more based on your data
}

for segment_id, name in segment_names.items():
    count = (customer_data['segment'] == segment_id).sum()
    print(f'\nSegment {segment_id}: {name}')
    print(f'  Number of customers: {count}')
    print(f'  Avg purchases: {segment_analysis.loc[segment_id, "total_purchases"]:.1f}')
    print(f'  Avg order value: ${segment_analysis.loc[segment_id, "avg_order_value"]:.2f}')
```

### Visualizing Clusters in 2D (PCA)

```python
from sklearn.decomposition import PCA

# Reduce to 2D for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Plot
plt.figure(figsize=(12, 6))

# Plot clusters
plt.subplot(1, 2, 1)
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=customer_data['segment'], cmap='viridis')
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title('Customer Segments (PCA)')
plt.colorbar(label='Segment')

# Plot with original features (first 2)
plt.subplot(1, 2, 2)
plt.scatter(X['total_purchases'], X['avg_order_value'], 
            c=customer_data['segment'], cmap='viridis')
plt.xlabel('Total Purchases')
plt.ylabel('Average Order Value')
plt.title('Customer Segments (Original Features)')
plt.colorbar(label='Segment')

plt.tight_layout()
plt.show()
```

### Predicting New Data Points

```python
# New customers
new_customers = pd.DataFrame({
    'total_purchases': [5, 30],
    'avg_order_value': [50, 150],
    'days_since_last_purchase': [100, 10],
    'customer_lifetime_value': [500, 3000]
})

# Scale and predict
new_customers_scaled = scaler.transform(new_customers)
predictions = kmeans.predict(new_customers_scaled)

print('New customer segments:')
for i, segment in enumerate(predictions):
    print(f'  Customer {i+1}: Segment {segment}')
```

### K-Means Limitations

```python
# Demonstration: K-Means fails on non-spherical clusters
from sklearn.datasets import make_moons

X_moons, _ = make_moons(n_samples=200, noise=0.05, random_state=42)

kmeans = KMeans(n_clusters=2, random_state=42)
labels = kmeans.fit_predict(X_moons)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.scatter(X_moons[:, 0], X_moons[:, 1])
plt.title('True Structure (Non-Spherical)')

plt.subplot(1, 2, 2)
plt.scatter(X_moons[:, 0], X_moons[:, 1], c=labels, cmap='viridis')
plt.title('K-Means Clustering (Fails)')

plt.tight_layout()
plt.show()
```

### Pros and Cons

**Pros:**
- ✅ Simple and easy to implement
- ✅ Fast and scalable
- ✅ Works well with spherical clusters
- ✅ Good for customer segmentation
- ✅ Easy to interpret

**Cons:**
- ❌ Must specify K in advance
- ❌ Sensitive to initialization
- ❌ Assumes spherical clusters
- ❌ Sensitive to outliers
- ❌ Assumes equal cluster sizes
- ❌ Only works with numerical features

---

## Principal Component Analysis (PCA)

### What is PCA?

PCA is a **dimensionality reduction** technique that transforms data to a new coordinate system where the greatest variance lies on the first coordinate (principal component), second greatest on second coordinate, etc.

**Purpose:**
- Reduce number of features
- Remove multicollinearity
- Visualize high-dimensional data
- Speed up algorithms
- Noise reduction

### How PCA Works

```
Original Features (3D)         Principal Components (2D)
     Z                               PC2
     ↑                                ↑
     • •                              •
    • • •          →                • •
   • • • •                         • • •
  • • • • •                       • • • •
 ———————→ Y                    ———————————→ PC1
X                             
```

**Steps:**
1. Standardize the data
2. Compute covariance matrix
3. Calculate eigenvectors and eigenvalues
4. Sort eigenvalues (descending)
5. Select top K eigenvectors
6. Transform data

### When to Use PCA?

**Use When:**
- ✅ Too many features (high-dimensional)
- ✅ Features are correlated
- ✅ Need to visualize data
- ✅ Speed up training
- ✅ Remove noise
- ✅ Feature extraction

**Don't Use When:**
- ❌ Need interpretability (PCs are linear combinations)
- ❌ Features already independent
- ❌ Small number of features
- ❌ Non-linear relationships (use kernel PCA)

### Implementation - Basic PCA

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

# Load data
iris = load_iris()
X = iris.data
y = iris.target

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)  # Reduce to 2 dimensions
X_pca = pca.fit_transform(X_scaled)

# Visualize
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis')
plt.xlabel(f'First PC ({pca.explained_variance_ratio_[0]:.2%} variance)')
plt.ylabel(f'Second PC ({pca.explained_variance_ratio_[1]:.2%} variance)')
plt.title('PCA: Iris Dataset')
plt.colorbar(scatter, label='Species')
plt.show()

print(f'Original shape: {X.shape}')
print(f'Reduced shape: {X_pca.shape}')
print(f'Explained variance ratio: {pca.explained_variance_ratio_}')
print(f'Total variance explained: {sum(pca.explained_variance_ratio_):.2%}')
```

### Choosing Number of Components

```python
# Fit PCA with all components
pca_full = PCA()
pca_full.fit(X_scaled)

# Plot cumulative explained variance
cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(cumulative_variance) + 1), 
         cumulative_variance, marker='o')
plt.axhline(y=0.95, color='r', linestyle='--', label='95% variance')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('Explained Variance by Number of Components')
plt.legend()
plt.grid(True)
plt.show()

# Find number of components for 95% variance
n_components_95 = np.argmax(cumulative_variance >= 0.95) + 1
print(f'Components needed for 95% variance: {n_components_95}')
```

### Specify Variance to Retain

```python
# Automatically choose components to retain 95% variance
pca_auto = PCA(n_components=0.95)
X_pca_auto = pca_auto.fit_transform(X_scaled)

print(f'Number of components: {pca_auto.n_components_}')
print(f'Explained variance: {sum(pca_auto.explained_variance_ratio_):.2%}')
```

### Feature Contribution to Components

```python
# Get component loadings
components_df = pd.DataFrame(
    pca_full.components_,
    columns=iris.feature_names,
    index=[f'PC{i+1}' for i in range(len(pca_full.components_))]
)

print('Component Loadings:')
print(components_df)

# Visualize loadings
plt.figure(figsize=(10, 6))
plt.imshow(components_df, cmap='coolwarm', aspect='auto')
plt.colorbar(label='Loading')
plt.yticks(range(len(components_df)), components_df.index)
plt.xticks(range(len(iris.feature_names)), iris.feature_names, rotation=45)
plt.title('PCA Component Loadings')
plt.tight_layout()
plt.show()
```

### Real-World Example: High-Dimensional Data

```python
# Generate high-dimensional data
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=1000,
    n_features=50,
    n_informative=30,
    n_redundant=20,
    random_state=42
)

print(f'Original dimensions: {X.shape}')

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA (retain 95% variance)
pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)

print(f'Reduced dimensions: {X_pca.shape}')
print(f'Variance retained: {sum(pca.explained_variance_ratio_):.2%}')
print(f'Dimensionality reduction: {X.shape[1]} → {X_pca.shape[1]}')
```

### PCA for Speed Improvement

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import time

# Without PCA
start = time.time()
model_full = RandomForestClassifier(n_estimators=100, random_state=42)
scores_full = cross_val_score(model_full, X_scaled, y, cv=5)
time_full = time.time() - start

# With PCA
start = time.time()
model_pca = RandomForestClassifier(n_estimators=100, random_state=42)
scores_pca = cross_val_score(model_pca, X_pca, y, cv=5)
time_pca = time.time() - start

print('Without PCA:')
print(f'  Accuracy: {scores_full.mean():.4f} (+/- {scores_full.std():.4f})')
print(f'  Time: {time_full:.2f}s')

print('\nWith PCA (95% variance):')
print(f'  Accuracy: {scores_pca.mean():.4f} (+/- {scores_pca.std():.4f})')
print(f'  Time: {time_pca:.2f}s')
print(f'  Speedup: {time_full/time_pca:.2f}x')
```

### Inverse Transform (Reconstruction)

```python
# Transform and reconstruct
X_pca = pca.transform(X_scaled)
X_reconstructed = pca.inverse_transform(X_pca)

# Calculate reconstruction error
reconstruction_error = np.mean((X_scaled - X_reconstructed) ** 2)
print(f'Reconstruction error: {reconstruction_error:.6f}')

# Visualize original vs reconstructed (first sample)
sample_idx = 0
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.bar(range(X.shape[1]), X_scaled[sample_idx])
plt.xlabel('Feature')
plt.ylabel('Value')
plt.title('Original (Scaled)')

plt.subplot(1, 3, 2)
plt.bar(range(X_pca.shape[1]), X_pca[sample_idx])
plt.xlabel('Component')
plt.ylabel('Value')
plt.title('PCA Components')

plt.subplot(1, 3, 3)
plt.bar(range(X.shape[1]), X_reconstructed[sample_idx])
plt.xlabel('Feature')
plt.ylabel('Value')
plt.title('Reconstructed')

plt.tight_layout()
plt.show()
```

### PCA in ML Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=0.95)),
    ('classifier', LogisticRegression(max_iter=1000))
])

# Train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline.fit(X_train, y_train)

# Evaluate
train_score = pipeline.score(X_train, y_train)
test_score = pipeline.score(X_test, y_test)

print(f'Train accuracy: {train_score:.4f}')
print(f'Test accuracy: {test_score:.4f}')
print(f'Number of components used: {pipeline.named_steps["pca"].n_components_}')
```

### Pros and Cons

**Pros:**
- ✅ Reduces dimensionality
- ✅ Removes multicollinearity
- ✅ Speeds up algorithms
- ✅ Reduces overfitting
- ✅ Data visualization
- ✅ Noise reduction

**Cons:**
- ❌ Loss of interpretability
- ❌ May lose information
- ❌ Assumes linear relationships
- ❌ Sensitive to scaling
- ❌ Computationally expensive for large datasets
- ❌ Components may not be meaningful

---

## Gradient Boosting

### What is Gradient Boosting?

Gradient Boosting builds models **sequentially**, where each new model corrects errors made by previous models.

**Key Concept:**
- Build weak learners (shallow trees) sequentially
- Each tree learns from mistakes of previous trees
- Combine predictions using weighted sum
- Focus on hard-to-predict samples

```
Data → Tree 1 → Errors₁ → Tree 2 → Errors₂ → Tree 3 → ... → Final Prediction
       (0.3)             (0.25)            (0.2)
       
Final = 0.3×Tree₁ + 0.25×Tree₂ + 0.2×Tree₃ + ...
```

### Gradient Boosting vs Random Forest

| Aspect | Random Forest | Gradient Boosting |
|--------|--------------|-------------------|
| **Training** | Parallel (independent trees) | Sequential (dependent trees) |
| **Trees** | Deep trees | Shallow trees |
| **Objective** | Reduce variance | Reduce bias |
| **Overfitting** | Less prone | More prone |
| **Speed** | Faster | Slower |
| **Accuracy** | Good | Better |

### When to Use Gradient Boosting?

**Use When:**
- ✅ Need highest accuracy
- ✅ Tabular/structured data
- ✅ Kaggle competitions
- ✅ Can afford training time
- ✅ Have enough data
- ✅ Mixed feature types

**Don't Use When:**
- ❌ Need fast training
- ❌ Very small datasets
- ❌ Need interpretability
- ❌ Real-time predictions needed
- ❌ Limited computational resources

### Implementation - GradientBoostingClassifier

```python
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import make_classification

# Generate data
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=15,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Gradient Boosting
model = GradientBoostingClassifier(
    n_estimators=100,        # Number of boosting stages
    learning_rate=0.1,       # Shrinks contribution of each tree
    max_depth=3,             # Shallow trees
    min_samples_split=2,
    min_samples_leaf=1,
    subsample=0.8,           # Fraction of samples for each tree
    random_state=42
)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print(f'ROC-AUC: {roc_auc_score(y_test, y_pred_proba[:, 1]):.4f}')
```

### Feature Importance

```python
# Get feature importance
feature_importance = pd.DataFrame({
    'feature': [f'feature_{i}' for i in range(X.shape[1])],
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

# Visualize
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'][:10], 
         feature_importance['importance'][:10])
plt.xlabel('Importance')
plt.title('Top 10 Feature Importances')
plt.tight_layout()
plt.show()
```

### Learning Curves

```python
# Track performance during training
from sklearn.metrics import accuracy_score

train_scores = []
test_scores = []

for i, y_pred_train in enumerate(model.staged_predict(X_train)):
    train_scores.append(accuracy_score(y_train, y_pred_train))
    
for i, y_pred_test in enumerate(model.staged_predict(X_test)):
    test_scores.append(accuracy_score(y_test, y_pred_test))

# Plot
plt.figure(figsize=(10, 6))
plt.plot(train_scores, label='Train')
plt.plot(test_scores, label='Test')
plt.xlabel('Number of Estimators')
plt.ylabel('Accuracy')
plt.title('Learning Curves')
plt.legend()
plt.grid(True)
plt.show()

# Find optimal number of estimators
optimal_n = np.argmax(test_scores) + 1
print(f'Optimal number of estimators: {optimal_n}')
```

### XGBoost (Extreme Gradient Boosting)

```python
# Install: pip install xgboost
import xgboost as xgb

# Train XGBoost
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    subsample=0.8,
    colsample_bytree=0.8,  # Fraction of features for each tree
    objective='binary:logistic',
    eval_metric='logloss',
    random_state=42,
    use_label_encoder=False
)

xgb_model.fit(
    X_train, y_train,
    eval_set=[(X_train, y_train), (X_test, y_test)],
    verbose=False
)

# Predictions
y_pred = xgb_model.predict(X_test)

print(f'XGBoost Accuracy: {accuracy_score(y_test, y_pred):.4f}')

# Plot training history
results = xgb_model.evals_result()
plt.figure(figsize=(10, 6))
plt.plot(results['validation_0']['logloss'], label='Train')
plt.plot(results['validation_1']['logloss'], label='Test')
plt.xlabel('Number of Estimators')
plt.ylabel('Log Loss')
plt.title('XGBoost Training History')
plt.legend()
plt.grid(True)
plt.show()
```

### LightGBM (Light Gradient Boosting Machine)

```python
# Install: pip install lightgbm
import lightgbm as lgb

# Train LightGBM
lgb_model = lgb.LGBMClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

lgb_model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    eval_metric='logloss',
    callbacks=[lgb.early_stopping(stopping_rounds=10), lgb.log_evaluation(period=0)]
)

# Predictions
y_pred = lgb_model.predict(X_test)

print(f'LightGBM Accuracy: {accuracy_score(y_test, y_pred):.4f}')
```

### Hyperparameter Tuning

```python
from sklearn.model_selection import RandomizedSearchCV

# Define parameter distribution
param_dist = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'subsample': [0.6, 0.8, 1.0],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Randomized search
random_search = RandomizedSearchCV(
    GradientBoostingClassifier(random_state=42),
    param_distributions=param_dist,
    n_iter=20,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)
random_search.fit(X_train, y_train)

print(f'Best parameters: {random_search.best_params_}')
print(f'Best score: {random_search.best_score_:.4f}')

# Best model
best_model = random_search.best_estimator_
y_pred = best_model.predict(X_test)
print(f'Test accuracy: {accuracy_score(y_test, y_pred):.4f}')
```

### Real-World Example: Credit Scoring

```python
# Generate credit data
credit_data = pd.DataFrame({
    'age': np.random.randint(18, 70, 1000),
    'income': np.random.randint(20000, 150000, 1000),
    'credit_score': np.random.randint(300, 850, 1000),
    'debt_to_income': np.random.uniform(0, 1, 1000),
    'num_accounts': np.random.randint(1, 15, 1000),
    'num_delinquencies': np.random.randint(0, 5, 1000),
    'employment_length': np.random.randint(0, 30, 1000)
})

# Create target (approved/rejected)
credit_data['approved'] = (
    (credit_data['credit_score'] > 650) &
    (credit_data['debt_to_income'] < 0.4) &
    (credit_data['num_delinquencies'] < 2)
).astype(int)

# Prepare data
X = credit_data.drop('approved', axis=1)
y = credit_data['approved']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train XGBoost
model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print(f'Precision: {precision_score(y_test, y_pred):.4f}')
print(f'Recall: {recall_score(y_test, y_pred):.4f}')
print(f'ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}')

# Feature importance
xgb.plot_importance(model, max_num_features=10)
plt.title('Feature Importance')
plt.tight_layout()
plt.show()

# Predict for new applicant
new_applicant = pd.DataFrame({
    'age': [35],
    'income': [75000],
    'credit_score': [720],
    'debt_to_income': [0.25],
    'num_accounts': [5],
    'num_delinquencies': [0],
    'employment_length': [8]
})

approval_prob = model.predict_proba(new_applicant)[0, 1]
print(f'\nNew applicant approval probability: {approval_prob:.2%}')

if approval_prob > 0.7:
    print('Decision: APPROVE')
elif approval_prob > 0.4:
    print('Decision: MANUAL REVIEW')
else:
    print('Decision: REJECT')
```

### Pros and Cons

**Pros:**
- ✅ Highest accuracy (often wins competitions)
- ✅ Handles mixed data types
- ✅ No feature scaling needed
- ✅ Handles missing values (XGBoost/LightGBM)
- ✅ Feature importance
- ✅ Robust to outliers
- ✅ Works with imbalanced data

**Cons:**
- ❌ Slow training (sequential)
- ❌ Prone to overfitting
- ❌ Many hyperparameters to tune
- ❌ Less interpretable
- ❌ Requires careful tuning
- ❌ Memory intensive

---

## Model Selection Guide

### Algorithm Comparison Matrix

| Algorithm | Complexity | Training Speed | Prediction Speed | Interpretability | Handles Non-linear | Handles Missing | Feature Scaling | Best Use Case |
|-----------|------------|----------------|------------------|------------------|-------------------|-----------------|-----------------|---------------|
| **Linear Regression** | Low | Fast | Fast | High | ❌ | ❌ | Required | Linear relationships |
| **Logistic Regression** | Low | Fast | Fast | High | ❌ | ❌ | Required | Binary classification |
| **Decision Tree** | Medium | Fast | Fast | High | ✅ | ✅ | Not required | Interpretable model |
| **Random Forest** | High | Medium | Medium | Medium | ✅ | ✅ | Not required | High accuracy needed |
| **SVM** | High | Slow | Medium | Low | ✅ (kernel) | ❌ | Required | High-dimensional data |
| **KNN** | Low | Fast | Slow | Medium | ✅ | ❌ | Required | Simple baseline |
| **Naive Bayes** | Low | Fast | Fast | Medium | ❌ | ❌ | Not required | Text classification |
| **K-Means** | Medium | Fast | Fast | High | ❌ | ❌ | Required | Customer segmentation |
| **PCA** | Medium | Medium | Fast | Low | ❌ | ❌ | Required | Dimensionality reduction |
| **Gradient Boosting** | Very High | Slow | Medium | Low | ✅ | ✅ (XGB/LGB) | Not required | Competitions, max accuracy |

### Decision Flow Chart

```
START
│
├─ Supervised or Unsupervised?
│  │
│  ├─ SUPERVISED → Regression or Classification?
│  │  │
│  │  ├─ REGRESSION
│  │  │  │
│  │  │  ├─ Linear relationship? → YES → Linear Regression
│  │  │  │                       → NO ↓
│  │  │  ├─ Need interpretability? → YES → Decision Tree
│  │  │  │                         → NO ↓
│  │  │  ├─ Need high accuracy? → YES → Gradient Boosting / Random Forest
│  │  │  └─ Simple baseline? → YES → KNN Regressor
│  │  │
│  │  └─ CLASSIFICATION
│  │     │
│  │     ├─ Binary or Multi-class?
│  │     │  │
│  │     │  ├─ BINARY
│  │     │  │  │
│  │     │  │  ├─ Linear boundary? → YES → Logistic Regression
│  │     │  │  │                   → NO ↓
│  │     │  │  ├─ Text data? → YES → Naive Bayes
│  │     │  │  │              → NO ↓
│  │     │  │  ├─ High-dimensional? → YES → SVM (RBF kernel)
│  │     │  │  │                     → NO ↓
│  │     │  │  ├─ Need interpretability? → YES → Decision Tree
│  │     │  │  │                         → NO ↓
│  │     │  │  └─ Need highest accuracy? → YES → Gradient Boosting
│  │     │  │
│  │     │  └─ MULTI-CLASS
│  │     │     │
│  │     │     ├─ Small dataset? → YES → Naive Bayes / KNN
│  │     │     │                 → NO ↓
│  │     │     ├─ Need interpretability? → YES → Decision Tree
│  │     │     │                         → NO ↓
│  │     │     └─ Need high accuracy? → YES → Random Forest / Gradient Boosting
│  │     │
│  └─ UNSUPERVISED
│     │
│     ├─ Clustering? → YES → K-Means / Hierarchical
│     │
│     └─ Dimensionality Reduction? → YES → PCA
│
END
```

### Dataset Size Considerations

| Dataset Size | Recommended Algorithms | Avoid |
|-------------|------------------------|-------|
| **Very Small (<100)** | Naive Bayes, Simple Linear/Logistic | Deep trees, Gradient Boosting |
| **Small (100-1K)** | Decision Tree, KNN, SVM | Neural Networks, Ensemble methods |
| **Medium (1K-100K)** | Random Forest, SVM, Gradient Boosting | KNN (slow predictions) |
| **Large (100K-1M)** | Logistic Regression, Random Forest, XGBoost | SVM (slow training) |
| **Very Large (>1M)** | Linear models, LightGBM, SGD-based | KNN, SVM |

### Problem Type Guide

**Linear Relationships:**
→ Linear Regression, Logistic Regression

**Non-linear Relationships:**
→ Decision Tree, Random Forest, SVM (kernel), Gradient Boosting

**High-Dimensional Data:**
→ SVM, PCA + any algorithm, Regularized Linear models

**Text Classification:**
→ Naive Bayes, Logistic Regression with TF-IDF

**Image Classification:**
→ SVM, Random Forest (for simple tasks)

**Customer Segmentation:**
→ K-Means, Hierarchical Clustering

**Anomaly Detection:**
→ Isolation Forest, One-Class SVM, K-Means (distance from centroids)

**Time Series:**
→ ARIMA, LSTM (not covered here), Gradient Boosting

**Imbalanced Data:**
→ Random Forest (class_weight), Gradient Boosting, SVM (class_weight)

### When to Use Each Algorithm

**Linear Regression:**
- ✅ Continuous target
- ✅ Linear relationship
- ✅ Need interpretability
- ✅ Fast predictions

**Logistic Regression:**
- ✅ Binary classification
- ✅ Need probabilities
- ✅ Linear decision boundary
- ✅ Baseline model

**Decision Tree:**
- ✅ Need interpretability
- ✅ Mixed feature types
- ✅ Non-linear relationships
- ✅ No scaling needed

**Random Forest:**
- ✅ High accuracy
- ✅ Prevent overfitting
- ✅ Feature importance
- ✅ Robust model

**SVM:**
- ✅ High-dimensional data
- ✅ Clear margin
- ✅ Small/medium datasets
- ✅ Non-linear (with kernel)

**KNN:**
- ✅ Simple baseline
- ✅ Non-linear boundaries
- ✅ Multi-class naturally
- ✅ Small datasets

**Naive Bayes:**
- ✅ Text classification
- ✅ Fast training/prediction
- ✅ Small datasets
- ✅ Probabilistic output

**K-Means:**
- ✅ Customer segmentation
- ✅ Data exploration
- ✅ Feature creation
- ✅ Simple clustering

**PCA:**
- ✅ Too many features
- ✅ Data visualization
- ✅ Speed up algorithms
- ✅ Remove multicollinearity

**Gradient Boosting:**
- ✅ Highest accuracy
- ✅ Competitions
- ✅ Tabular data
- ✅ Can afford training time

---

## Interview Questions for 3 YOE

### Question 1: Bias-Variance Tradeoff

**Question:** Explain the bias-variance tradeoff and how it relates to overfitting and underfitting.

**Answer:**
- **Bias:** Error from wrong assumptions (underfitting)
  - High bias = model too simple
  - Example: Linear model for non-linear data
  
- **Variance:** Error from sensitivity to training data (overfitting)
  - High variance = model too complex
  - Example: Deep decision tree memorizing training data
  
- **Tradeoff:** 
  - Decreasing bias → increases variance
  - Decreasing variance → increases bias
  - Goal: Find sweet spot with minimum total error
  
- **Total Error = Bias² + Variance + Irreducible Error**

**Example:**
```python
# High Bias (Underfitting)
model = DecisionTreeClassifier(max_depth=1)  # Too simple

# High Variance (Overfitting)
model = DecisionTreeClassifier(max_depth=None)  # Too complex

# Balanced
model = DecisionTreeClassifier(max_depth=5)  # Just right
```

---

### Question 2: Overfitting vs Underfitting

**Question:** How do you detect and prevent overfitting?

**Answer:**

**Detection:**
- Large gap between train and test accuracy
- High train accuracy, low test accuracy
- Learning curves show divergence
- Cross-validation scores vary significantly

**Prevention:**
1. **More Data:** Collect more training samples
2. **Cross-Validation:** Use k-fold CV
3. **Regularization:** L1/L2 penalties (Ridge, Lasso)
4. **Early Stopping:** Stop training when validation error increases
5. **Feature Selection:** Remove irrelevant features
6. **Ensemble Methods:** Random Forest, Gradient Boosting
7. **Dropout:** For neural networks
8. **Pruning:** For decision trees

**Example:**
```python
# Regularization
from sklearn.linear_model import Ridge
model = Ridge(alpha=1.0)  # Higher alpha = more regularization

# Cross-validation
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)
```

---

### Question 3: Precision vs Recall

**Question:** When would you optimize for precision vs recall? Give real-world examples.

**Answer:**

**Precision = TP / (TP + FP)** - "Of all positive predictions, how many were correct?"
**Recall = TP / (TP + FN)** - "Of all actual positives, how many did we catch?"

**Optimize for Precision:**
- **When:** False positives are costly
- **Examples:**
  - Email spam detection (don't want to mark important emails as spam)
  - Product recommendations (don't want to recommend irrelevant products)
  - Medical test (don't want to unnecessarily worry patients)

**Optimize for Recall:**
- **When:** False negatives are costly
- **Examples:**
  - Cancer detection (don't want to miss any cases)
  - Fraud detection (catch as many frauds as possible)
  - Security systems (catch all threats)

**F1-Score:** Harmonic mean of precision and recall (use when balance needed)

**Example:**
```python
# Adjust threshold for precision/recall tradeoff
y_pred_proba = model.predict_proba(X_test)[:, 1]

# High precision (fewer false positives)
y_pred_high_precision = (y_pred_proba > 0.7).astype(int)

# High recall (fewer false negatives)
y_pred_high_recall = (y_pred_proba > 0.3).astype(int)
```

---

### Question 4: Cross-Validation

**Question:** What is cross-validation and why is it important?

**Answer:**

**Cross-Validation:** Technique to evaluate model performance on unseen data by splitting data into multiple folds.

**K-Fold Cross-Validation:**
1. Split data into K folds
2. Train on K-1 folds, validate on 1 fold
3. Repeat K times (each fold used as validation once)
4. Average results

**Why Important:**
- ✅ Better estimate of model performance
- ✅ Uses all data for training and validation
- ✅ Reduces variance in performance estimate
- ✅ Helps detect overfitting
- ✅ More reliable than single train-test split

**Types:**
- **K-Fold:** Standard approach
- **Stratified K-Fold:** Maintains class distribution in each fold
- **Leave-One-Out (LOO):** K = number of samples (expensive)
- **Time Series Split:** For temporal data (no shuffling)

**Example:**
```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

# K-Fold
scores = cross_val_score(model, X, y, cv=5)
print(f'Mean: {scores.mean():.4f}, Std: {scores.std():.4f}')

# Stratified K-Fold (for imbalanced data)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf)
```

---

### Question 5: Feature Engineering

**Question:** What is feature engineering and what are some common techniques?

**Answer:**

**Feature Engineering:** Creating new features or transforming existing ones to improve model performance.

**Common Techniques:**

1. **Handling Missing Values:**
   - Mean/median/mode imputation
   - Forward/backward fill
   - KNN imputation
   - Drop rows/columns

2. **Encoding Categorical Variables:**
   - Label Encoding (ordinal)
   - One-Hot Encoding (nominal)
   - Target Encoding
   - Frequency Encoding

3. **Scaling/Normalization:**
   - StandardScaler (z-score)
   - MinMaxScaler (0-1 range)
   - RobustScaler (resistant to outliers)

4. **Feature Creation:**
   - Polynomial features
   - Interaction features (A × B)
   - Binning/Discretization
   - Date/time features (day, month, year, weekday)

5. **Feature Selection:**
   - Correlation analysis
   - Feature importance from tree models
   - Recursive Feature Elimination (RFE)
   - L1 regularization (Lasso)

6. **Dimensionality Reduction:**
   - PCA
   - LDA
   - t-SNE

**Example:**
```python
# Polynomial features
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# One-hot encoding
X_encoded = pd.get_dummies(df, columns=['category'])

# Binning
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 60, 100], 
                         labels=['child', 'young', 'middle', 'senior'])
```

---

### Question 6: Handling Imbalanced Data

**Question:** How do you handle imbalanced datasets?

**Answer:**

**Techniques:**

1. **Resampling:**
   - **Oversampling:** Add copies of minority class (SMOTE)
   - **Undersampling:** Remove samples from majority class
   - **Combination:** SMOTEENN, SMOTETomek

2. **Class Weights:**
   - Assign higher weight to minority class
   - Most sklearn models support `class_weight='balanced'`

3. **Ensemble Methods:**
   - BalancedRandomForest
   - EasyEnsemble
   - BalancedBagging

4. **Anomaly Detection:**
   - Treat minority as anomaly
   - Use One-Class SVM, Isolation Forest

5. **Evaluation Metrics:**
   - Don't use accuracy
   - Use: Precision, Recall, F1-Score, ROC-AUC, PR-AUC

6. **Threshold Adjustment:**
   - Lower threshold for minority class

**Example:**
```python
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

# SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Class weights
model = RandomForestClassifier(class_weight='balanced')

# Manual weights
weights = {0: 1, 1: 10}  # Class 1 has 10x weight
model = RandomForestClassifier(class_weight=weights)
```

---

### Question 7: Regularization

**Question:** What is regularization and what are the differences between L1, L2, and ElasticNet?

**Answer:**

**Regularization:** Technique to prevent overfitting by penalizing large coefficients.

**Types:**

**1. L2 Regularization (Ridge):**
- Penalty: $\lambda \sum_{j=1}^{n} \beta_j^2$
- Shrinks coefficients towards zero
- Doesn't make coefficients exactly zero
- Good when all features are relevant
- Handles multicollinearity

**2. L1 Regularization (Lasso):**
- Penalty: $\lambda \sum_{j=1}^{n} |\beta_j|$
- Can make coefficients exactly zero (feature selection)
- Sparse models
- Good when many irrelevant features

**3. ElasticNet:**
- Combination of L1 and L2
- Penalty: $\lambda_1 \sum |\beta_j| + \lambda_2 \sum \beta_j^2$
- Benefits of both
- Good when features are correlated

**Comparison:**

| Aspect | L2 (Ridge) | L1 (Lasso) | ElasticNet |
|--------|-----------|-----------|------------|
| **Feature Selection** | ❌ | ✅ | ✅ |
| **Handles Multicollinearity** | ✅ | ❌ | ✅ |
| **Sparse Models** | ❌ | ✅ | ✅ |
| **Computational** | Fast | Fast | Slower |

**Example:**
```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet

# L2
ridge = Ridge(alpha=1.0)

# L1
lasso = Lasso(alpha=1.0)

# ElasticNet
elastic = ElasticNet(alpha=1.0, l1_ratio=0.5)  # 0.5 = 50% L1, 50% L2
```

---

### Question 8: ROC-AUC Curve

**Question:** What is ROC-AUC and when is it useful?

**Answer:**

**ROC (Receiver Operating Characteristic) Curve:**
- Plots True Positive Rate vs False Positive Rate
- TPR = Recall = TP / (TP + FN)
- FPR = FP / (FP + TN)

**AUC (Area Under Curve):**
- Ranges from 0 to 1
- 1.0 = Perfect classifier
- 0.5 = Random classifier
- < 0.5 = Worse than random

**When Useful:**
- ✅ Comparing multiple models
- ✅ Imbalanced datasets
- ✅ Binary classification
- ✅ Threshold-independent metric
- ✅ Trade-off between TPR and FPR

**When NOT Useful:**
- ❌ Multi-class (use multi-class ROC or other metrics)
- ❌ Heavily imbalanced (use PR-AUC instead)
- ❌ Need specific threshold

**Interpretation:**
- AUC = 0.90-1.0: Excellent
- AUC = 0.80-0.90: Good
- AUC = 0.70-0.80: Fair
- AUC = 0.60-0.70: Poor
- AUC = 0.50-0.60: Fail

**Example:**
```python
from sklearn.metrics import roc_curve, roc_auc_score

y_pred_proba = model.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
auc = roc_auc_score(y_test, y_pred_proba)

plt.plot(fpr, tpr, label=f'AUC = {auc:.2f}')
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

---

### Question 9: Ensemble Methods

**Question:** What are ensemble methods and what are the main types?

**Answer:**

**Ensemble Methods:** Combine multiple models to improve performance.

**Main Types:**

**1. Bagging (Bootstrap Aggregating):**
- Train models independently on random subsets
- Average predictions (regression) or vote (classification)
- Reduces variance
- Example: Random Forest
- **Goal:** Reduce overfitting

**2. Boosting:**
- Train models sequentially
- Each model corrects previous errors
- Reduces bias
- Example: Gradient Boosting, XGBoost, AdaBoost
- **Goal:** Improve accuracy

**3. Stacking:**
- Train multiple diverse models
- Use another model (meta-learner) to combine predictions
- Example: Train Logistic Regression on predictions from RF, SVM, XGB

**Comparison:**

| Aspect | Bagging | Boosting | Stacking |
|--------|---------|----------|----------|
| **Training** | Parallel | Sequential | Both |
| **Reduces** | Variance | Bias | Both |
| **Overfitting** | Less prone | More prone | Depends |
| **Speed** | Fast | Slow | Slow |
| **Example** | Random Forest | XGBoost | Custom |

**When to Use:**
- **Bagging:** High variance models (deep trees)
- **Boosting:** High bias models (shallow trees) or need max accuracy
- **Stacking:** Have diverse models, need best performance

**Example:**
```python
# Bagging
from sklearn.ensemble import BaggingClassifier
bagging = BaggingClassifier(
    base_estimator=DecisionTreeClassifier(),
    n_estimators=10
)

# Boosting
from sklearn.ensemble import GradientBoostingClassifier
boosting = GradientBoostingClassifier(n_estimators=100)

# Stacking
from sklearn.ensemble import StackingClassifier
estimators = [
    ('rf', RandomForestClassifier()),
    ('svm', SVC(probability=True))
]
stacking = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression()
)
```

---

### Question 10: Feature Scaling

**Question:** Why is feature scaling important and when is it needed?

**Answer:**

**Why Important:**
- Algorithms using distance metrics are sensitive to scale
- Gradient descent converges faster
- Regularization works better
- Prevents features with large values from dominating

**When Needed:**

**Required:**
- ✅ KNN (distance-based)
- ✅ SVM (distance to hyperplane)
- ✅ Logistic Regression (with regularization)
- ✅ Linear Regression (with regularization)
- ✅ PCA (variance-based)
- ✅ Neural Networks

**NOT Required:**
- ❌ Decision Trees
- ❌ Random Forest
- ❌ Gradient Boosting
- ❌ Naive Bayes

**Scaling Methods:**

**1. StandardScaler (Z-score normalization):**
- Mean = 0, Std = 1
- Formula: $(x - \mu) / \sigma$
- Use: Most common, works well with normally distributed data

**2. MinMaxScaler:**
- Scale to [0, 1] range
- Formula: $(x - x_{min}) / (x_{max} - x_{min})$
- Use: When need bounded range, neural networks

**3. RobustScaler:**
- Uses median and IQR (resistant to outliers)
- Formula: $(x - median) / IQR$
- Use: When data has outliers

**Example:**
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Use same scaler!

# MinMaxScaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_train)

# RobustScaler
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X_train)

# IMPORTANT: Fit on training data, transform both train and test
```

---

### Question 11: Curse of Dimensionality

**Question:** What is the curse of dimensionality and how do you address it?

**Answer:**

**Curse of Dimensionality:** As dimensions increase, data becomes sparse and distance metrics become less meaningful.

**Problems:**
- Data points become equidistant in high dimensions
- Requires exponentially more data
- Computational complexity increases
- Overfitting risk increases
- Distance-based algorithms (KNN, K-Means) perform poorly

**Solutions:**

1. **Dimensionality Reduction:**
   - PCA
   - LDA
   - t-SNE
   - UMAP

2. **Feature Selection:**
   - Remove irrelevant features
   - Feature importance
   - Correlation analysis
   - RFE

3. **Regularization:**
   - L1 (Lasso) for feature selection
   - L2 (Ridge) to prevent overfitting

4. **Domain Knowledge:**
   - Engineer meaningful features
   - Remove redundant features

5. **Use Appropriate Algorithms:**
   - Avoid KNN for high dimensions
   - Use tree-based methods (handle high dimensions better)

**Example:**
```python
# Before: 100 dimensions, poor performance
X_high_dim = make_classification(n_features=100)

# Solution 1: PCA
pca = PCA(n_components=0.95)  # Retain 95% variance
X_reduced = pca.fit_transform(X_high_dim)
print(f'Reduced from {X_high_dim.shape[1]} to {X_reduced.shape[1]} features')

# Solution 2: Feature selection with Lasso
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
selected_features = np.where(lasso.coef_ != 0)[0]
X_selected = X[:, selected_features]
```

---

### Question 12: Model Evaluation Workflow

**Question:** Describe your complete workflow for training and evaluating a machine learning model.

**Answer:**

**Complete ML Workflow:**

**1. Problem Definition:**
- Understand business problem
- Define success metrics
- Identify supervised/unsupervised, regression/classification

**2. Data Collection & Exploration:**
- Load data
- Check shape, types, missing values
- EDA: distributions, correlations, outliers
- Visualizations

**3. Data Preprocessing:**
- Handle missing values
- Encode categorical variables
- Feature scaling (if needed)
- Handle outliers

**4. Feature Engineering:**
- Create new features
- Polynomial features
- Interaction terms
- Date/time features

**5. Train-Test Split:**
- Split data (typically 80-20 or 70-30)
- Stratified split for classification
- Time-based split for time series

**6. Model Selection:**
- Start with simple baseline
- Try multiple algorithms
- Use cross-validation

**7. Hyperparameter Tuning:**
- GridSearchCV or RandomizedSearchCV
- Optimize on validation set

**8. Model Evaluation:**
- Multiple metrics (accuracy, precision, recall, F1, ROC-AUC)
- Confusion matrix
- Learning curves
- Feature importance

**9. Error Analysis:**
- Analyze misclassifications
- Check for bias
- Identify edge cases

**10. Model Deployment:**
- Save model (joblib/pickle)
- Monitor performance
- Retrain periodically

**Example:**
```python
# Complete workflow
from sklearn.pipeline import Pipeline

# 1. Define pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=0.95)),
    ('classifier', RandomForestClassifier())
])

# 2. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 3. Hyperparameter tuning
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [5, 10, None]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='f1')
grid_search.fit(X_train, y_train)

# 4. Evaluate
y_pred = grid_search.predict(X_test)
print(classification_report(y_test, y_pred))

# 5. Save model
import joblib
joblib.dump(grid_search.best_estimator_, 'model.pkl')
```

---

### Question 13: Random Forest vs Gradient Boosting

**Question:** What are the key differences between Random Forest and Gradient Boosting? When would you use one over the other?

**Answer:**

**Key Differences:**

| Aspect | Random Forest | Gradient Boosting |
|--------|--------------|-------------------|
| **Training** | Parallel (independent trees) | Sequential (dependent trees) |
| **Tree Depth** | Deep trees | Shallow trees (stumps) |
| **Objective** | Reduce variance (bagging) | Reduce bias (boosting) |
| **Speed** | Faster training | Slower training |
| **Overfitting** | Less prone | More prone (needs tuning) |
| **Accuracy** | Good | Better (often) |
| **Hyperparameters** | Fewer to tune | Many to tune |
| **Interpretability** | Moderate | Lower |

**Use Random Forest When:**
- ✅ Need fast training
- ✅ Want robust model (less overfitting)
- ✅ Limited time for hyperparameter tuning
- ✅ Parallel processing available
- ✅ Good accuracy is enough

**Use Gradient Boosting When:**
- ✅ Need highest accuracy
- ✅ Kaggle competitions
- ✅ Can afford training time
- ✅ Have time for hyperparameter tuning
- ✅ Structured/tabular data
- ✅ Willing to prevent overfitting carefully

**Example:**
```python
# Random Forest: Fast, good default performance
rf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
rf.fit(X_train, y_train)

# Gradient Boosting: Slower, needs tuning, but better
gb = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    subsample=0.8
)
gb.fit(X_train, y_train)

# Compare
print(f'RF Test Score: {rf.score(X_test, y_test):.4f}')
print(f'GB Test Score: {gb.score(X_test, y_test):.4f}')
```

---

### Question 14: Handling Categorical Variables

**Question:** What are different ways to handle categorical variables in machine learning?

**Answer:**

**Encoding Techniques:**

**1. Label Encoding:**
- Convert categories to integers: {Red: 0, Blue: 1, Green: 2}
- **Use:** Ordinal data (low, medium, high)
- **Don't use:** Nominal data (introduces false ordering)

**2. One-Hot Encoding:**
- Create binary column for each category
- **Use:** Nominal data with few categories (<10)
- **Don't use:** High cardinality (too many columns)

**3. Target Encoding:**
- Replace category with mean of target
- **Use:** High cardinality, tree-based models
- **Risk:** Overfitting (use smoothing)

**4. Frequency Encoding:**
- Replace with frequency of category
- **Use:** When frequency matters

**5. Binary Encoding:**
- Convert to binary digits
- **Use:** High cardinality (middle ground)

**6. Leave-One-Out Encoding:**
- Like target encoding but exclude current row
- **Use:** Reduce overfitting

**Example:**
```python
# Label Encoding (ordinal)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['size_encoded'] = le.fit_transform(df['size'])  # S, M, L → 0, 1, 2

# One-Hot Encoding (nominal)
df_encoded = pd.get_dummies(df, columns=['color'], drop_first=True)

# Target Encoding
category_means = df.groupby('category')['target'].mean()
df['category_encoded'] = df['category'].map(category_means)

# Frequency Encoding
freq = df['city'].value_counts(normalize=True)
df['city_freq'] = df['city'].map(freq)

# For sklearn models
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

ct = ColumnTransformer([
    ('onehot', OneHotEncoder(drop='first'), ['category1', 'category2'])
], remainder='passthrough')

X_transformed = ct.fit_transform(X)
```

---

### Question 15: Deployment and Monitoring

**Question:** After training a model, what considerations are important for deployment and monitoring?

**Answer:**

**Deployment Considerations:**

**1. Model Serialization:**
- Save trained model (joblib, pickle)
- Save preprocessing pipeline
- Version control models

**2. Infrastructure:**
- API endpoint (Flask, FastAPI)
- Cloud deployment (AWS, Azure, GCP)
- Containerization (Docker)
- Load balancing

**3. Performance:**
- Latency requirements
- Throughput (requests/second)
- Model size (memory)
- Batch vs real-time predictions

**4. Reproducibility:**
- Fixed random seeds
- Version dependencies (requirements.txt)
- Data versioning

**Monitoring:**

**1. Model Performance:**
- Accuracy, precision, recall tracking
- Compare with baseline
- A/B testing
- Performance degradation alerts

**2. Data Drift:**
- Input distribution changes
- Feature statistics monitoring
- Detect when retrain needed

**3. Concept Drift:**
- Relationship between features and target changes
- Monitor prediction distribution
- Retrain triggers

**4. System Metrics:**
- Response time
- Error rates
- Resource usage (CPU, memory)
- Request volume

**5. Business Metrics:**
- Impact on KPIs
- ROI
- User satisfaction

**Example:**
```python
# 1. Save model
import joblib
from datetime import datetime

model_version = datetime.now().strftime('%Y%m%d_%H%M%S')
joblib.dump(model, f'model_{model_version}.pkl')
joblib.dump(scaler, f'scaler_{model_version}.pkl')

# 2. API endpoint (Flask)
from flask import Flask, request, jsonify

app = Flask(__name__)
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    X = pd.DataFrame([data])
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0].tolist()
    
    return jsonify({
        'prediction': int(prediction),
        'probability': probability,
        'model_version': model_version
    })

# 3. Monitoring
import logging

logging.info(f'Prediction: {prediction}, Input: {data}')

# 4. Data drift detection
from scipy.stats import ks_2samp

# Compare training vs production feature distributions
for feature in features:
    stat, p_value = ks_2samp(X_train[feature], X_production[feature])
    if p_value < 0.05:
        print(f'Data drift detected in {feature}')
```

---

## Summary

This comprehensive guide covered:

1. **Supervised Learning:**
   - Regression: Linear Regression
   - Classification: Logistic Regression, Decision Trees, Random Forest, SVM, KNN, Naive Bayes, Gradient Boosting

2. **Unsupervised Learning:**
   - Clustering: K-Means
   - Dimensionality Reduction: PCA

3. **Key Concepts:**
   - When to use each algorithm
   - Real-world implementations
   - Hyperparameter tuning
   - Feature engineering
   - Model evaluation

4. **Interview Preparation:**
   - 15 detailed questions with answers
   - Practical code examples
   - Decision-making criteria

**Next Steps:**
- Practice implementing these algorithms
- Work on real datasets (Kaggle)
- Build end-to-end ML projects
- Learn deep learning (next level)
- Study MLOps for production deployment

**Resources:**
- scikit-learn documentation
- Kaggle competitions
- ML papers (arXiv)
- Coursera ML courses
- Hands-on practice

---

**End of Traditional ML Complete Guide** 🎯

Total Coverage:
- ✅ 11 Machine Learning Algorithms
- ✅ Complete implementations with code
- ✅ Real-world examples
- ✅ When to use / when not to use
- ✅ Hyperparameter tuning
- ✅ Model comparison
- ✅ 15 Interview questions
- ✅ Deployment considerations

Good luck with your interviews! 🚀