from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

# We could include XGBoost if available, but to keep dependencies light, 
# we'll stick with sklearn's built-in models for now.

def get_random_forest_pipeline(n_estimators=100, random_state=42):
    return Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=n_estimators, random_state=random_state))
    ])

def get_decision_tree_pipeline(random_state=42):
    return Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', DecisionTreeClassifier(random_state=random_state))
    ])

# Dictionary of available models for easy comparison
MODELS = {
    'RandomForest': get_random_forest_pipeline,
    'DecisionTree': get_decision_tree_pipeline
}
