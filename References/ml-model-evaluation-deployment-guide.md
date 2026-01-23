# ML Model Evaluation & Deployment - Complete Guide

> **Comprehensive reference for model evaluation, deployment strategies, monitoring, and production best practices for ML/AI engineers**

---

## Table of Contents

1. [Model Evaluation Fundamentals](#model-evaluation-fundamentals)
2. [Classification Metrics](#classification-metrics)
3. [Regression Metrics](#regression-metrics)
4. [Cross-Validation Strategies](#cross-validation-strategies)
5. [Model Selection & Comparison](#model-selection--comparison)
6. [Hyperparameter Tuning](#hyperparameter-tuning)
7. [Model Interpretability](#model-interpretability)
8. [Deployment Strategies](#deployment-strategies)
9. [Model Serving Architecture](#model-serving-architecture)
10. [A/B Testing & Experimentation](#ab-testing--experimentation)
11. [Model Monitoring](#model-monitoring)
12. [Model Drift Detection](#model-drift-detection)
13. [Model Retraining Strategies](#model-retraining-strategies)
14. [MLOps Best Practices](#mlops-best-practices)
15. [Production Issues & Solutions](#production-issues--solutions)
16. [Cost Optimization](#cost-optimization)
17. [Real-World Scenarios](#real-world-scenarios)
18. [Interview Questions](#interview-questions)

---

## Model Evaluation Fundamentals

### What is Model Evaluation?

Model evaluation is the process of assessing how well your ML model performs on unseen data to determine if it's ready for production.

### Key Principles

**1. Train-Validation-Test Split**

```python
import numpy as np
from sklearn.model_selection import train_test_split

# Standard split
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Result: 70% train, 15% validation, 15% test

print(f"Train size: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
print(f"Validation size: {len(X_val)} ({len(X_val)/len(X)*100:.1f}%)")
print(f"Test size: {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")

"""
WHY THREE SPLITS?

Training Set (70%):
- Train model parameters
- Fit the model

Validation Set (15%):
- Tune hyperparameters
- Select best model
- Early stopping
- Can be used multiple times

Test Set (15%):
- Final evaluation ONLY
- Estimate real-world performance
- Use ONLY ONCE (no peeking!)
- Represents production data
"""
```

**2. Never Touch Test Set Until Final Evaluation**

```python
# ❌ WRONG: Using test set multiple times
for model in [model1, model2, model3]:
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)  # WRONG!
    print(f"Test score: {score}")

# ✅ CORRECT: Use validation set for comparison
for model in [model1, model2, model3]:
    model.fit(X_train, y_train)
    val_score = model.score(X_val, y_val)  # Validation
    print(f"Validation score: {val_score}")

# Select best model based on validation
best_model = model2

# ONLY NOW evaluate on test set (ONCE)
final_score = best_model.score(X_test, y_test)
print(f"Final test score: {final_score}")
```

**3. Data Leakage Prevention**

```python
"""
DATA LEAKAGE: When information from test/validation leaks into training

Common Causes:
1. Scaling before split
2. Feature selection before split
3. Time series: using future to predict past
4. Duplicate records across splits
5. Target encoding on entire dataset
"""

# ❌ WRONG: Data leakage example
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Leak! Uses test data statistics

X_train, X_test = train_test_split(X_scaled, test_size=0.2)  # Too late!

# ✅ CORRECT: Fit only on training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit on train only
X_test_scaled = scaler.transform(X_test)        # Transform test

# ✅ EVEN BETTER: Use Pipeline
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier())
])

pipeline.fit(X_train, y_train)  # Scaler fits only on train
test_score = pipeline.score(X_test, y_test)  # Correct evaluation
```

---

## Classification Metrics

### 1. Confusion Matrix

```python
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# Predictions
y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
y_pred = [1, 0, 1, 0, 0, 1, 0, 1, 1, 0]

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)

"""
Confusion Matrix Structure:

                Predicted
                0    1
Actual  0      TN   FP
        1      FN   TP

TN (True Negative):  Correctly predicted negative
FP (False Positive): Incorrectly predicted positive (Type I Error)
FN (False Negative): Incorrectly predicted negative (Type II Error)
TP (True Positive):  Correctly predicted positive
"""

print("Confusion Matrix:")
print(cm)
print(f"\nTrue Negatives:  {cm[0,0]}")
print(f"False Positives: {cm[0,1]}")
print(f"False Negatives: {cm[1,0]}")
print(f"True Positives:  {cm[1,1]}")

# Visualize
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
```

### 2. Accuracy, Precision, Recall, F1-Score

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Calculate metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print(f"Accuracy:  {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall:    {recall:.3f}")
print(f"F1-Score:  {f1:.3f}")

"""
METRIC DEFINITIONS:

Accuracy = (TP + TN) / (TP + TN + FP + FN)
- Overall correctness
- Good when classes are balanced
- BAD when classes are imbalanced!

Precision = TP / (TP + FP)
- Of all positive predictions, how many were correct?
- "How precise are we when we say positive?"
- High precision = Few false alarms

Recall (Sensitivity) = TP / (TP + FN)
- Of all actual positives, how many did we catch?
- "How complete is our detection?"
- High recall = Few missed cases

F1-Score = 2 * (Precision * Recall) / (Precision + Recall)
- Harmonic mean of precision and recall
- Good when you need balance

WHEN TO USE WHICH?

Medical Diagnosis (Cancer Detection):
- Priority: HIGH RECALL (don't miss any cancer cases)
- Accept some false positives (false alarms)
- recall = 0.95+ required

Spam Detection:
- Priority: HIGH PRECISION (don't mark important emails as spam)
- Accept some false negatives (some spam gets through)
- precision = 0.95+ required

Fraud Detection:
- Priority: BALANCE (F1-Score)
- Need to catch fraud but not annoy customers
- f1_score = 0.80+ required
"""

# Example: Imbalanced dataset problem
y_imbalanced = [0]*95 + [1]*5  # 95% negative, 5% positive
y_pred_dumb = [0]*100           # Predict everything as negative

accuracy_dumb = accuracy_score(y_imbalanced, y_pred_dumb)
print(f"\nDumb model accuracy: {accuracy_dumb:.3f}")  # 0.95!
# But recall = 0.0 (missed all positives!)
```

### 3. ROC Curve and AUC

```python
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.linear_model import LogisticRegression

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Get probability predictions (not class predictions)
y_proba = model.predict_proba(X_test)[:, 1]  # Probability of positive class

# Calculate ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_auc = auc(fpr, tpr)

# Plot ROC curve
plt.figure(figsize=(10, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate (Recall)')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()

"""
ROC CURVE INTERPRETATION:

AUC (Area Under Curve):
- AUC = 1.0: Perfect classifier
- AUC = 0.9-1.0: Excellent
- AUC = 0.8-0.9: Good
- AUC = 0.7-0.8: Fair
- AUC = 0.6-0.7: Poor
- AUC = 0.5: Random (no better than coin flip)
- AUC < 0.5: Worse than random (predictions inverted!)

ADVANTAGES:
✅ Threshold-independent
✅ Good for imbalanced datasets
✅ Compares multiple models easily
✅ Shows tradeoff between TPR and FPR

DISADVANTAGES:
❌ Optimistic for imbalanced data
❌ Doesn't show actual performance at specific threshold
❌ Equal weight to FP and FN

WHEN TO USE:
- Comparing multiple models
- Don't know optimal threshold yet
- Class balance is reasonable
"""

# Calculate AUC directly
auc_score = roc_auc_score(y_test, y_proba)
print(f"AUC-ROC Score: {auc_score:.3f}")

# Find optimal threshold (max Youden's J statistic)
optimal_idx = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_idx]
print(f"Optimal threshold: {optimal_threshold:.3f}")
```

### 4. Precision-Recall Curve

```python
from sklearn.metrics import precision_recall_curve, average_precision_score

# Calculate precision-recall curve
precision_vals, recall_vals, thresholds_pr = precision_recall_curve(y_test, y_proba)
avg_precision = average_precision_score(y_test, y_proba)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(recall_vals, precision_vals, color='blue', lw=2, 
         label=f'PR curve (AP = {avg_precision:.2f})')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")
plt.grid(True)
plt.show()

"""
PRECISION-RECALL CURVE:

Average Precision (AP):
- AP = 1.0: Perfect
- AP = 0.9+: Excellent
- AP < 0.5: Poor

WHEN TO USE PR CURVE INSTEAD OF ROC:
✅ Highly imbalanced datasets (rare positive class)
✅ Care more about positive class
✅ Example: Fraud (0.1% positive), Disease screening

ROC vs PR Curve:
- ROC: Good for balanced datasets
- PR: Better for imbalanced datasets (focuses on positive class)

Example: 1% fraud rate
- ROC AUC might be 0.95 (looks great!)
- PR AUC might be 0.30 (shows real challenge)
"""
```

### 5. Multi-Class Classification Metrics

```python
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# Load multi-class dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Classification report
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

"""
Multi-class metrics:

macro avg: Average of each class (equal weight)
- Good when all classes equally important
- Treats imbalanced classes fairly

weighted avg: Weighted by class support
- Good when classes have different importance
- Reflects actual distribution

Example Output:
              precision    recall  f1-score   support

     class_0       1.00      1.00      1.00        19
     class_1       0.92      1.00      0.96        12
     class_2       1.00      0.93      0.97        14

    accuracy                           0.98        45
   macro avg       0.97      0.98      0.98        45
weighted avg       0.98      0.98      0.98        45
"""

# Multi-class confusion matrix
cm_multi = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm_multi, annot=True, fmt='d', cmap='Blues',
            xticklabels=iris.target_names,
            yticklabels=iris.target_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Multi-Class Confusion Matrix')
plt.show()

# Multi-class ROC AUC
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score

# Binarize labels for multi-class ROC
y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
y_proba = model.predict_proba(X_test)

# Calculate AUC for each class
roc_auc_per_class = {}
for i in range(len(iris.target_names)):
    roc_auc_per_class[iris.target_names[i]] = roc_auc_score(
        y_test_bin[:, i], y_proba[:, i]
    )

print("\nROC AUC per class:")
for class_name, auc_score in roc_auc_per_class.items():
    print(f"{class_name}: {auc_score:.3f}")

# Overall multi-class AUC
overall_auc = roc_auc_score(y_test_bin, y_proba, average='macro')
print(f"\nOverall AUC (macro): {overall_auc:.3f}")
```

---

## Regression Metrics

### 1. MAE, MSE, RMSE, R²

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import numpy as np

# Generate regression data
X = np.random.randn(1000, 5)
y = 3*X[:,0] + 2*X[:,1] - X[:,2] + np.random.randn(1000)*0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Calculate metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("Regression Metrics:")
print(f"MAE (Mean Absolute Error):     {mae:.4f}")
print(f"MSE (Mean Squared Error):      {mse:.4f}")
print(f"RMSE (Root Mean Squared Error): {rmse:.4f}")
print(f"R² (R-squared):                {r2:.4f}")

"""
METRIC DEFINITIONS:

MAE = mean(|y_true - y_pred|)
- Average absolute error
- Same unit as target variable
- Less sensitive to outliers
- Easy to interpret

MSE = mean((y_true - y_pred)²)
- Average squared error
- Penalizes large errors more
- Unit is squared
- More sensitive to outliers

RMSE = sqrt(MSE)
- Square root of MSE
- Same unit as target variable
- Penalizes large errors
- Most commonly used

R² = 1 - (SS_residual / SS_total)
- Proportion of variance explained
- Range: -∞ to 1.0
- R² = 1.0: Perfect fit
- R² = 0.0: Model as good as mean
- R² < 0.0: Worse than predicting mean!

WHEN TO USE WHICH?

MAE:
✅ When outliers should be treated equally
✅ When you want interpretable error
✅ Example: House price prediction (avg error = $10K)

RMSE:
✅ When large errors are particularly bad
✅ Most common in ML competitions
✅ Example: Demand forecasting (large errors costly)

R²:
✅ When comparing models
✅ When understanding model quality
✅ NOT for comparing across different datasets
"""

# Visualize predictions vs actual
plt.figure(figsize=(12, 5))

# Plot 1: Predictions vs Actual
plt.subplot(1, 2, 1)
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title(f'Predictions vs Actual (R²={r2:.3f})')
plt.grid(True)

# Plot 2: Residuals
plt.subplot(1, 2, 2)
residuals = y_test - y_pred
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.grid(True)

plt.tight_layout()
plt.show()
```

### 2. MAPE (Mean Absolute Percentage Error)

```python
def mean_absolute_percentage_error(y_true, y_pred):
    """Calculate MAPE"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    # Avoid division by zero
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

mape = mean_absolute_percentage_error(y_test, y_pred)
print(f"MAPE: {mape:.2f}%")

"""
MAPE = mean(|y_true - y_pred| / |y_true|) × 100%

ADVANTAGES:
✅ Scale-independent (can compare across datasets)
✅ Easy to interpret (error in percentage)
✅ Good for business metrics

DISADVANTAGES:
❌ Undefined when y_true = 0
❌ Asymmetric (penalizes over-predictions more)
❌ Sensitive to small denominators

WHEN TO USE:
✅ Sales forecasting (% error matters)
✅ Comparing models on different scales
✅ Business reporting (easier to understand)

AVOID WHEN:
❌ Target values near or equal to zero
❌ Need symmetric error metric
"""
```

### 3. Custom Regression Metrics

```python
from sklearn.metrics import make_scorer

def weighted_mae(y_true, y_pred, weights=None):
    """Custom weighted MAE (penalize errors on high values more)"""
    if weights is None:
        weights = np.abs(y_true)  # Weight by actual value
    
    errors = np.abs(y_true - y_pred)
    weighted_errors = errors * weights
    return np.mean(weighted_errors) / np.mean(weights)

# Use in cross-validation
weighted_mae_scorer = make_scorer(weighted_mae, greater_is_better=False)

from sklearn.model_selection import cross_val_score

scores = cross_val_score(
    model, X_train, y_train,
    cv=5,
    scoring=weighted_mae_scorer
)

print(f"Weighted MAE (CV): {-scores.mean():.4f} (+/- {scores.std():.4f})")
```

---

## Cross-Validation Strategies

### 1. K-Fold Cross-Validation

```python
from sklearn.model_selection import KFold, cross_val_score, cross_validate
from sklearn.ensemble import RandomForestClassifier

# K-Fold CV
kfold = KFold(n_splits=5, shuffle=True, random_state=42)

model = RandomForestClassifier(n_estimators=100)

# Simple scoring
scores = cross_val_score(model, X, y, cv=kfold, scoring='accuracy')

print(f"K-Fold CV Scores: {scores}")
print(f"Mean Accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")

"""
K-FOLD CROSS-VALIDATION:

Process:
1. Split data into K equal folds
2. For each fold:
   - Use fold as validation set
   - Use remaining K-1 folds as training set
   - Train and evaluate model
3. Average performance across K folds

ADVANTAGES:
✅ Uses all data for both training and validation
✅ More reliable than single split
✅ Reduces variance in evaluation
✅ Better estimate of generalization

DISADVANTAGES:
❌ K times slower (train K models)
❌ Not suitable for time series (data shuffling)
❌ May be computationally expensive

CHOOSING K:
- K=5: Standard, good balance
- K=10: More reliable, slower
- K=n (LOO): Maximum reliability, very slow
- Larger dataset → can use smaller K
"""

# Multiple metrics
scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
cv_results = cross_validate(model, X, y, cv=kfold, scoring=scoring)

print("\nMultiple Metrics:")
for metric in scoring:
    scores = cv_results[f'test_{metric}']
    print(f"{metric:12s}: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

### 2. Stratified K-Fold

```python
from sklearn.model_selection import StratifiedKFold

# Stratified K-Fold (preserves class distribution)
stratified_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores_stratified = cross_val_score(model, X, y, cv=stratified_kfold, scoring='accuracy')

print(f"Stratified K-Fold CV Scores: {scores_stratified}")
print(f"Mean Accuracy: {scores_stratified.mean():.3f} (+/- {scores_stratified.std():.3f})")

"""
STRATIFIED K-FOLD:

Difference from regular K-Fold:
- Maintains class distribution in each fold
- Each fold has same % of each class as original dataset

WHEN TO USE:
✅ Imbalanced datasets
✅ Classification problems
✅ Small datasets

Example:
Original: 90% class 0, 10% class 1
Each fold: 90% class 0, 10% class 1 (maintained)

Regular K-Fold might give:
Fold 1: 95% class 0, 5% class 1
Fold 2: 85% class 0, 15% class 1
→ Inconsistent evaluation!
"""

# Verify stratification
for fold, (train_idx, val_idx) in enumerate(stratified_kfold.split(X, y)):
    train_dist = np.bincount(y[train_idx]) / len(train_idx)
    val_dist = np.bincount(y[val_idx]) / len(val_idx)
    print(f"Fold {fold+1} - Train: {train_dist}, Val: {val_dist}")
```

### 3. Time Series Cross-Validation

```python
from sklearn.model_selection import TimeSeriesSplit

# Time Series Split
tscv = TimeSeriesSplit(n_splits=5)

"""
TIME SERIES SPLIT:

Regular CV: ❌ WRONG for time series (data leakage!)
- Trains on future, validates on past
- Shuffles data (loses temporal order)

Time Series CV: ✅ CORRECT
- Only trains on past
- Validates on future
- Expands training window

Example with 10 data points:
Split 1: Train [0,1], Test [2]
Split 2: Train [0,1,2], Test [3]
Split 3: Train [0,1,2,3], Test [4]
Split 4: Train [0,1,2,3,4], Test [5]
...

ALWAYS USE FOR:
- Stock price prediction
- Sales forecasting
- Weather prediction
- Any temporal data
"""

print("Time Series Cross-Validation:")
for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
    print(f"Fold {fold+1}:")
    print(f"  Train: {train_idx[0]} to {train_idx[-1]} (size={len(train_idx)})")
    print(f"  Test:  {test_idx[0]} to {test_idx[-1]} (size={len(test_idx)})")

# Evaluate with time series CV
scores_ts = cross_val_score(model, X, y, cv=tscv, scoring='accuracy')
print(f"\nTime Series CV Mean: {scores_ts.mean():.3f} (+/- {scores_ts.std():.3f})")
```

### 4. Custom Cross-Validation

```python
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut

# Group K-Fold (for grouped data)
"""
Example: Medical data with multiple measurements per patient
- Want to ensure same patient not in both train and test
- Prevents data leakage from same patient
"""

# Example groups (patient IDs)
groups = np.array([1,1,1,2,2,3,3,3,4,4,5,5,5,5])

group_kfold = GroupKFold(n_splits=3)

print("Group K-Fold:")
for fold, (train_idx, test_idx) in enumerate(group_kfold.split(X, y, groups)):
    train_groups = groups[train_idx]
    test_groups = groups[test_idx]
    print(f"Fold {fold+1}:")
    print(f"  Train groups: {np.unique(train_groups)}")
    print(f"  Test groups:  {np.unique(test_groups)}")
    # Verify no overlap
    assert len(set(train_groups) & set(test_groups)) == 0

"""
OTHER CV STRATEGIES:

LeaveOneOut (LOO):
- n_splits = n_samples
- Each sample used once as test
- Maximum variance reduction
- Very slow for large datasets

LeavePOut (LPO):
- Leave P samples out each time
- Even slower than LOO

ShuffleSplit:
- Random train/test splits
- Can overlap between splits
- Good for large datasets

StratifiedShuffleSplit:
- Stratified version of ShuffleSplit
- Good for imbalanced data
"""
```

---

## Model Selection & Comparison

### 1. Comparing Multiple Models

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import pandas as pd

def compare_models(X, y, cv=5):
    """Compare multiple models with cross-validation"""
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(),
        'Random Forest': RandomForestClassifier(n_estimators=100),
        'Gradient Boosting': GradientBoostingClassifier(),
        'SVM': SVC(probability=True),
        'KNN': KNeighborsClassifier(),
        'Naive Bayes': GaussianNB()
    }
    
    results = []
    
    for name, model in models.items():
        print(f"Evaluating {name}...")
        
        # Cross-validation with multiple metrics
        cv_results = cross_validate(
            model, X, y,
            cv=cv,
            scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
            return_train_score=True
        )
        
        results.append({
            'Model': name,
            'Train Accuracy': cv_results['train_accuracy'].mean(),
            'Test Accuracy': cv_results['test_accuracy'].mean(),
            'Test Precision': cv_results['test_precision'].mean(),
            'Test Recall': cv_results['test_recall'].mean(),
            'Test F1': cv_results['test_f1'].mean(),
            'Test ROC-AUC': cv_results['test_roc_auc'].mean(),
            'Std Dev': cv_results['test_accuracy'].std()
        })
    
    # Create DataFrame
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values('Test Accuracy', ascending=False)
    
    return df_results

# Compare models
results_df = compare_models(X, y, cv=5)

print("\nModel Comparison:")
print(results_df.to_string(index=False))

# Visualize comparison
plt.figure(figsize=(12, 6))
plt.barh(results_df['Model'], results_df['Test Accuracy'], xerr=results_df['Std Dev'])
plt.xlabel('Accuracy')
plt.title('Model Comparison (5-Fold CV)')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

"""
MODEL SELECTION CRITERIA:

1. Performance Metrics:
   - Accuracy (for balanced data)
   - F1-Score (for imbalanced data)
   - ROC-AUC (for ranking ability)
   - Domain-specific metrics

2. Training Time:
   - Fast: Linear models, Naive Bayes
   - Medium: Decision Trees, KNN
   - Slow: Random Forest, Gradient Boosting, SVM

3. Prediction Time:
   - Fast: Linear models
   - Medium: Decision Trees, SVM
   - Slow: KNN, Random Forest

4. Interpretability:
   - High: Linear models, Decision Trees
   - Medium: Random Forest (feature importance)
   - Low: Neural Networks, SVM (kernel)

5. Overfitting:
   - Check: Train vs Test performance gap
   - Large gap = Overfitting
"""

# Check for overfitting
results_df['Overfitting Gap'] = results_df['Train Accuracy'] - results_df['Test Accuracy']
print("\nOverfitting Analysis:")
print(results_df[['Model', 'Train Accuracy', 'Test Accuracy', 'Overfitting Gap']].to_string(index=False))
```

### 2. Statistical Significance Testing

```python
from scipy import stats
from sklearn.model_selection import cross_val_score

def compare_models_statistical(model1, model2, X, y, cv=10):
    """Compare two models with statistical significance test"""
    
    # Get cross-validation scores for both models
    scores1 = cross_val_score(model1, X, y, cv=cv, scoring='accuracy')
    scores2 = cross_val_score(model2, X, y, cv=cv, scoring='accuracy')
    
    # Perform paired t-test
    t_stat, p_value = stats.ttest_rel(scores1, scores2)
    
    print(f"Model 1 mean accuracy: {scores1.mean():.4f} (+/- {scores1.std():.4f})")
    print(f"Model 2 mean accuracy: {scores2.mean():.4f} (+/- {scores2.std():.4f})")
    print(f"\nPaired t-test:")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")
    
    if p_value < 0.05:
        if scores1.mean() > scores2.mean():
            print(f"  Model 1 is significantly better (p < 0.05)")
        else:
            print(f"  Model 2 is significantly better (p < 0.05)")
    else:
        print(f"  No significant difference (p >= 0.05)")
    
    return scores1, scores2, p_value

# Compare two models
model1 = RandomForestClassifier(n_estimators=100)
model2 = GradientBoostingClassifier()

scores1, scores2, p_value = compare_models_statistical(model1, model2, X, y, cv=10)

# Visualize distribution
plt.figure(figsize=(10, 6))
plt.boxplot([scores1, scores2], labels=['Random Forest', 'Gradient Boosting'])
plt.ylabel('Accuracy')
plt.title('Model Performance Distribution')
plt.grid(axis='y', alpha=0.3)
plt.show()
```

---

## Hyperparameter Tuning

### 1. Grid Search

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Define parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']
}

# Grid search
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1,  # Use all CPU cores
    verbose=1
)

print("Running Grid Search...")
grid_search.fit(X_train, y_train)

# Best parameters
print(f"\nBest parameters: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_:.4f}")

# Best model
best_model = grid_search.best_estimator_
test_score = best_model.score(X_test, y_test)
print(f"Test score: {test_score:.4f}")

# All results
cv_results_df = pd.DataFrame(grid_search.cv_results_)
print("\nTop 10 parameter combinations:")
print(cv_results_df[['params', 'mean_test_score', 'std_test_score', 'rank_test_score']]
      .sort_values('rank_test_score')
      .head(10))

"""
GRID SEARCH:

ADVANTAGES:
✅ Exhaustive search (tries all combinations)
✅ Guaranteed to find best in grid
✅ Reproducible
✅ Easy to understand

DISADVANTAGES:
❌ Exponentially slow (n_params1 × n_params2 × ...)
❌ Curse of dimensionality
❌ May miss optimal values between grid points

Example:
3 parameters × 3 values each = 27 combinations
5 parameters × 4 values each = 1,024 combinations
With 5-fold CV: 1,024 × 5 = 5,120 models!

WHEN TO USE:
- Small parameter space (<100 combinations)
- Need exhaustive search
- Have computational resources
- Final tuning (narrow range)
"""
```

### 2. Random Search

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

# Define parameter distributions
param_dist = {
    'n_estimators': randint(50, 500),
    'max_depth': randint(5, 50),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': uniform(0.1, 0.9)
}

# Random search
random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_dist,
    n_iter=100,  # Number of random combinations to try
    cv=5,
    scoring='f1',
    n_jobs=-1,
    random_state=42,
    verbose=1
)

print("Running Random Search...")
random_search.fit(X_train, y_train)

print(f"\nBest parameters: {random_search.best_params_}")
print(f"Best CV score: {random_search.best_score_:.4f}")

"""
RANDOM SEARCH:

ADVANTAGES:
✅ Much faster than Grid Search
✅ Can sample from continuous distributions
✅ Often finds good solutions quickly
✅ Better exploration of parameter space

DISADVANTAGES:
❌ Not exhaustive (might miss optimal)
❌ Need to choose n_iter
❌ Results may vary (need fixed random_state)

RESEARCH FINDING:
Random Search often performs as well as Grid Search
with 10-20% of the computation!

WHEN TO USE:
- Large parameter space
- Limited computational resources
- Initial exploration
- Continuous parameter distributions
"""

# Compare Grid vs Random Search
print("\nComparison:")
print(f"Grid Search:   {grid_search.best_score_:.4f} ({len(grid_search.cv_results_['params'])} combinations)")
print(f"Random Search: {random_search.best_score_:.4f} (100 combinations)")
```

### 3. Bayesian Optimization

```python
from skopt import BayesSearchCV
from skopt.space import Real, Integer

# Define search space
search_space = {
    'n_estimators': Integer(50, 500),
    'max_depth': Integer(5, 50),
    'min_samples_split': Integer(2, 20),
    'min_samples_leaf': Integer(1, 10),
    'max_features': Real(0.1, 0.9)
}

# Bayesian optimization
bayes_search = BayesSearchCV(
    RandomForestClassifier(random_state=42),
    search_space,
    n_iter=50,  # Fewer iterations needed
    cv=5,
    scoring='f1',
    n_jobs=-1,
    random_state=42,
    verbose=1
)

print("Running Bayesian Optimization...")
bayes_search.fit(X_train, y_train)

print(f"\nBest parameters: {bayes_search.best_params_}")
print(f"Best CV score: {bayes_search.best_score_:.4f}")

"""
BAYESIAN OPTIMIZATION:

How it works:
1. Build probabilistic model of objective function
2. Use model to select most promising parameters
3. Evaluate those parameters
4. Update model with new results
5. Repeat

ADVANTAGES:
✅ More efficient than Grid/Random Search
✅ Learns from previous evaluations
✅ Focuses on promising regions
✅ Good for expensive objective functions

DISADVANTAGES:
❌ More complex to set up
❌ Overhead for simple models
❌ May converge to local optimum

WHEN TO USE:
- Expensive model training
- Need few iterations
- Complex parameter interactions
- Limited computational budget

COMPARISON:
Grid Search:    1,000 iterations → good result
Random Search:  100 iterations → good result
Bayesian Opt:   20-50 iterations → good result
"""

# Learning curve (how score improves over iterations)
plt.figure(figsize=(10, 6))
plt.plot(range(len(bayes_search.cv_results_['mean_test_score'])),
         bayes_search.cv_results_['mean_test_score'])
plt.xlabel('Iteration')
plt.ylabel('CV Score')
plt.title('Bayesian Optimization Learning Curve')
plt.grid(True)
plt.show()
```

### 4. Hyperparameter Importance

```python
def analyze_hyperparameter_importance(cv_results):
    """Analyze which hyperparameters matter most"""
    
    df = pd.DataFrame(cv_results)
    
    # Extract parameters
    params_df = pd.json_normalize(df['params'])
    scores = df['mean_test_score']
    
    # Calculate correlation of each parameter with score
    correlations = {}
    for col in params_df.columns:
        if params_df[col].dtype in ['int64', 'float64']:
            corr = np.corrcoef(params_df[col], scores)[0, 1]
            correlations[col] = abs(corr)
    
    # Sort by importance
    importance_df = pd.DataFrame(correlations.items(), 
                                 columns=['Parameter', 'Importance'])
    importance_df = importance_df.sort_values('Importance', ascending=False)
    
    print("Hyperparameter Importance:")
    print(importance_df)
    
    # Visualize
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Parameter'], importance_df['Importance'])
    plt.xlabel('Absolute Correlation with Score')
    plt.title('Hyperparameter Importance')
    plt.tight_layout()
    plt.show()
    
    return importance_df

# Analyze
importance = analyze_hyperparameter_importance(grid_search.cv_results_)
```

---

## Model Interpretability

### 1. Feature Importance

```python
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Get feature importance
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("Feature Importance:")
print(feature_importance)

# Visualize
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'][:15], feature_importance['importance'][:15])
plt.xlabel('Importance')
plt.title('Top 15 Feature Importances')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

"""
FEATURE IMPORTANCE INTERPRETATION:

Random Forest/Gradient Boosting:
- Based on mean decrease in impurity
- Shows which features split data best
- Cumulative across all trees

Linear Models:
- Coefficients magnitude = importance
- Need scaled features for comparison

LIMITATIONS:
❌ Biased towards high-cardinality features
❌ Correlated features split importance
❌ Doesn't show direction (positive/negative impact)
"""
```

### 2. SHAP Values

```python
import shap

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Calculate SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values[1], X_test, feature_names=feature_names)

# Force plot for single prediction
shap.force_plot(explainer.expected_value[1], shap_values[1][0], X_test[0], 
                feature_names=feature_names)

"""
SHAP (SHapley Additive exPlanations):

ADVANTAGES:
✅ Consistent and locally accurate
✅ Shows feature contribution for each prediction
✅ Based on game theory (Shapley values)
✅ Works for any model
✅ Shows positive/negative impact

INTERPRETATION:
- Red: High feature value
- Blue: Low feature value
- Horizontal position: Impact on prediction
- Right = increases prediction
- Left = decreases prediction

USE CASES:
- Explain individual predictions
- Understand model globally
- Feature selection
- Model debugging
- Regulatory compliance (need explanations)
"""

# Dependence plot (shows feature interaction)
shap.dependence_plot(0, shap_values[1], X_test, feature_names=feature_names)
```

### 3. LIME (Local Interpretable Model-Agnostic Explanations)

```python
from lime import lime_tabular

# Create LIME explainer
explainer = lime_tabular.LimeTabularExplainer(
    X_train,
    feature_names=feature_names,
    class_names=['Negative', 'Positive'],
    mode='classification'
)

# Explain a prediction
instance_idx = 0
exp = explainer.explain_instance(
    X_test[instance_idx], 
    model.predict_proba,
    num_features=10
)

# Show explanation
exp.show_in_notebook(show_table=True)

# As plot
exp.as_pyplot_figure()

"""
LIME:

How it works:
1. Perturb the input (create similar samples)
2. Get model predictions for perturbed samples
3. Fit simple interpretable model (linear) locally
4. Use simple model to explain complex model

ADVANTAGES:
✅ Model-agnostic (works with any model)
✅ Local explanation (for specific prediction)
✅ Easy to understand (linear explanation)

DISADVANTAGES:
❌ Instability (perturbations may vary)
❌ Only local (not global understanding)
❌ Computational overhead

WHEN TO USE:
- Need to explain specific predictions
- Black-box models (neural networks)
- Debugging misclassifications
- Building trust with stakeholders
"""
```

### 4. Partial Dependence Plots

```python
from sklearn.inspection import PartialDependenceDisplay

# Partial dependence plot
fig, ax = plt.subplots(figsize=(12, 4))
PartialDependenceDisplay.from_estimator(
    model, X_train, features=[0, 1, (0, 1)], 
    feature_names=feature_names,
    ax=ax
)
plt.tight_layout()
plt.show()

"""
PARTIAL DEPENDENCE PLOTS:

Shows marginal effect of one or two features on predictions
- How does changing feature X affect prediction?
- Averages out effect of all other features

INTERPRETATION:
- Y-axis: Predicted value
- X-axis: Feature value
- Slope: Feature impact direction and magnitude

USE CASES:
- Understand feature relationships
- Verify model makes sense
- Feature engineering insights
- Communication with domain experts
"""
```

---

Due to length, I'll continue with the remaining sections in the next part. Should I proceed with:
- Deployment Strategies
- Model Serving Architecture  
- A/B Testing
- Model Monitoring
- Drift Detection
- Retraining
- MLOps
- Production Issues
- Cost Optimization
- Real-World Scenarios
- Interview Questions

?