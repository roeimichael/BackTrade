import warnings
import pandas as pd
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from config.model_config import ModelConfig
from helpers import load_data, preprocess_data, evaluate_model, plot_metrics

warnings.filterwarnings('ignore')


def get_models():
    return {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Support Vector Machines': LinearSVC(max_iter=ModelConfig.LINEAR_SVC_MAX_ITER),
        'Decision Trees': DecisionTreeClassifier(),
        'Random Forest': RandomForestClassifier(),
        'Naive Bayes': GaussianNB(),
        'K-Nearest Neighbor': KNeighborsClassifier(),
        'RBF SVM': SVC(gamma=2, C=1),
        'Gaussian Process': GaussianProcessClassifier(
            ModelConfig.GAUSSIAN_PROCESS_KERNEL_SCALE * RBF(ModelConfig.GAUSSIAN_PROCESS_RBF_SCALE)
        ),
        'Neural Net': MLPClassifier(alpha=ModelConfig.MLP_ALPHA, max_iter=ModelConfig.MLP_MAX_ITER),
        'AdaBoost': AdaBoostClassifier(),
        'QDA': QuadraticDiscriminantAnalysis()
    }


def train_and_evaluate_models(exclude_models=None):
    if exclude_models is None:
        exclude_models = ["GaussianNB", "SVC"]

    models = get_models()
    target_df, dates = load_data()

    avg_accuracies, avg_precisions, avg_recalls = [], [], []

    for key, model in models.items():
        accuracies, precisions, recalls = {}, {}, {}

        for i in range(ModelConfig.DATE_RANGE_START, ModelConfig.DATE_RANGE_END):
            x_train, y_train, x_validate, y_validate = preprocess_data(dates, i, target_df)

            model.fit(x_train, y_train)
            predictions = model.predict(x_validate)

            acc, prec, rec = evaluate_model(predictions, y_validate)
            accuracies[dates[i]] = acc
            precisions[dates[i]] = prec
            recalls[dates[i]] = rec

        df_model = pd.DataFrame(
            index=dates[ModelConfig.DATE_RANGE_START:ModelConfig.DATE_RANGE_END],
            columns=['Accuracy', 'Precision', 'Recall']
        )
        df_model['Accuracy'] = list(accuracies.values())
        df_model['Precision'] = list(precisions.values())
        df_model['Recall'] = list(recalls.values())

        avg_accuracy = df_model[df_model["Accuracy"] != 0]["Accuracy"].mean()
        avg_precision = df_model[df_model["Precision"] != 0]["Precision"].mean()
        avg_recall = df_model[df_model["Recall"] != 0]["Recall"].mean()

        avg_accuracies.append(avg_accuracy)
        avg_precisions.append(avg_precision)
        avg_recalls.append(avg_recall)

        print(f"\n{model.__class__.__name__}")
        print(df_model)
        print(f"Avg. Accuracy = {avg_accuracy:.4f}")
        print(f"Avg. Precision = {avg_precision:.4f}")
        print(f"Avg. Recall = {avg_recall:.4f}")

    model_names = [model.__class__.__name__ for model in models.values()]
    plot_metrics(model_names, avg_accuracies, avg_precisions, avg_recalls, exclude_models=exclude_models)


if __name__ == '__main__':
    train_and_evaluate_models()
