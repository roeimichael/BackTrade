import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
from sklearn.svm import SVC, LinearSVC
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import accuracy_score, precision_score, recall_score
from helpers import load_data, preprocess_data, evaluate_model, plot_metrics


warnings.filterwarnings('ignore')

# Define your models here
models = {
    'Logistic Regression': LogisticRegression(),
    'Support Vector Machines': LinearSVC(),
    'Decision Trees': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'Naive Bayes': GaussianNB(),
    'K-Nearest Neighbor': KNeighborsClassifier(),
    'RBF SVM': SVC(gamma=2, C=1),
    'Gaussian Process': GaussianProcessClassifier(1.0 * RBF(1.0)),
    'Neural Net': MLPClassifier(alpha=1, max_iter=1000),
    'AdaBoost': AdaBoostClassifier(),
    'QDA': QuadraticDiscriminantAnalysis()
}

# Initialize data structures for storing results
accuracies, precisions, recalls = {}, {}, {}
avg_accuracies, avg_precisions, avg_recalls = [], [], []

# Load target data and dates
target_df, dates = load_data()

# Iterate over each model and perform training and evaluation
for key in models.keys():
    for i in range(350, 370):
        x_train, y_train, x_validate, y_validate = preprocess_data(dates, i, target_df)

        # Train the model
        models[key].fit(x_train, y_train)

        # Validate the model
        predictions = models[key].predict(x_validate)

        # Evaluate and store metrics
        accuracies[dates[i]], precisions[dates[i]], recalls[dates[i]] = evaluate_model(predictions, y_validate)

    # Calculate average metrics for the current model
    df_model = pd.DataFrame(index=dates[350:370], columns=['Accuracy', 'Precision', 'Recall'])
    df_model['Accuracy'] = accuracies.values()
    df_model['Precision'] = precisions.values()
    df_model['Recall'] = recalls.values()

    avg_accuracies.append(df_model[df_model["Accuracy"] != 0]["Accuracy"].mean())
    avg_precisions.append(df_model[df_model["Precision"] != 0]["Precision"].mean())
    avg_recalls.append(df_model[df_model["Recall"] != 0]["Recall"].mean())

    print(models[key].__class__.__name__)
    print(df_model)
    print(f"Avg. Accuracy = {avg_accuracies[-1]}")
    print(f"Avg. Precision = {avg_precisions[-1]}")
    print(f"Avg. Recall = {avg_recalls[-1]}")
    print("\n\n")

# Plot the metrics
model_names = [model.__class__.__name__ for model in models.values()]
exclude = ["GaussianNB", "SVC"]
plot_metrics(model_names, avg_accuracies, avg_precisions, avg_recalls, exclude_models=exclude)
