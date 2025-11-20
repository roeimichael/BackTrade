import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, precision_score, recall_score

from config.path_config import PathConfig


def load_data():
    target_df = pd.read_csv(PathConfig.TARGET_FILE)
    dates_df = pd.read_csv(PathConfig.DATES_FILE)
    dates = dates_df.values.flatten().tolist() if hasattr(dates_df, 'values') else dates_df.tolist()
    return target_df, dates


def preprocess_data(dates, index, target_df):
    date_file = PathConfig.DATA_DATES2_5_DIR / f"{dates[index]}.csv"
    next_date_file = PathConfig.DATA_DATES2_5_DIR / f"{dates[index + 1]}.csv"

    date_df = pd.read_csv(date_file)
    next_date_df = pd.read_csv(next_date_file)

    x_train = date_df.drop(['ticker'], axis=1, errors='ignore')
    x_validate = next_date_df.drop(['ticker'], axis=1, errors='ignore')

    y_train = target_df[dates[index + 1]]
    y_validate = target_df[dates[index + 2]]

    scaler = preprocessing.StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_validate = scaler.fit_transform(x_validate)

    return x_train, y_train, x_validate, y_validate


def evaluate_model(predictions, y_validate):
    accuracy = accuracy_score(predictions, y_validate)
    precision = precision_score(predictions, y_validate, zero_division=0)
    recall = recall_score(predictions, y_validate, zero_division=0)
    return accuracy, precision, recall


def plot_metrics(models, accuracies, precisions, recalls, exclude_models=None):
    if exclude_models is None:
        exclude_models = []

    model_indices = [i for i, model in enumerate(models) if model not in exclude_models]
    models = [model for i, model in enumerate(models) if i in model_indices]
    accuracies = [accuracy for i, accuracy in enumerate(accuracies) if i in model_indices]
    precisions = [precision for i, precision in enumerate(precisions) if i in model_indices]
    recalls = [recall for i, recall in enumerate(recalls) if i in model_indices]

    x = np.arange(len(models))
    fig, axs = plt.subplots(nrows=3, figsize=(15, 20))
    cmap = plt.get_cmap("tab10")

    metrics = [(accuracies, 'Accuracy'), (precisions, 'Precision'), (recalls, 'Recall')]

    for ax, (metric_values, metric_name) in zip(axs, metrics):
        rects = ax.bar(x, metric_values, color=cmap.colors)
        ax.set_ylabel('Scores')
        ax.set_title(f'Comparison of {metric_name} for Different Models')
        ax.set_xticks([])

        for i, rect in enumerate(rects):
            height = rect.get_height()
            ax.annotate(
                f'{round(height, 2)}',
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center',
                va='bottom'
            )

        handles = [plt.Rectangle((0, 0), 1, 1, color=cmap(i)) for i in range(len(models))]
        ax.legend(handles, models, title="Models", loc="upper right")

    fig.tight_layout()
    plt.show()
