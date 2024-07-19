import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt
import numpy as np


def load_data():
    # Load target data and dates
    target_df = pd.read_csv("./data/target.csv")  # Adjust the path as needed
    dates = pd.read_csv("./data/dates.csv").values.flatten().tolist()  # Adjust the path as needed
    return target_df, dates


def preprocess_data(dates, index, target_df):
    date_df = pd.read_csv(f"./data/dates2.5/{dates[index]}.csv")
    next_date_df = pd.read_csv(f"./data/dates2.5/{dates[index + 1]}.csv")

    x_train = date_df.drop(['ticker'], axis=1)
    x_validate = next_date_df.drop(['ticker'], axis=1)

    y_train = target_df[dates[index + 1]]
    y_validate = target_df[dates[index + 2]]

    scaler = preprocessing.StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_validate = scaler.fit_transform(x_validate)

    return x_train, y_train, x_validate, y_validate


def evaluate_model(predictions, y_validate):
    accuracy = accuracy_score(predictions, y_validate)
    precision = precision_score(predictions, y_validate)
    recall = recall_score(predictions, y_validate)
    return accuracy, precision, recall


def plot_metrics(models, accuracies, precisions, recalls, exclude_models=[]):
    model_indices = [i for i, model in enumerate(models) if model not in exclude_models]
    models = [model for i, model in enumerate(models) if i in model_indices]
    accuracies = [accuracy for i, accuracy in enumerate(accuracies) if i in model_indices]
    precisions = [precision for i, precision in enumerate(precisions) if i in model_indices]
    recalls = [recall for i, recall in enumerate(recalls) if i in model_indices]

    x = np.arange(len(models))
    fig, axs = plt.subplots(nrows=3, figsize=(15, 20))
    cmap = plt.get_cmap("tab10")

    metrics = [(accuracies, 'Accuracy'), (precisions, 'Precision'), (recalls, 'Recall')]
    for ax, metric in zip(axs, metrics):
        rects = ax.bar(x, metric[0], color=cmap.colors)
        ax.set_ylabel('Scores')
        ax.set_title(f'Comparison of {metric[1]} for Different Models')
        ax.set_xticks([])
        for i, rect in enumerate(rects):
            height = rect.get_height()
            ax.annotate('{}'.format(round(height, 2)),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        handles = [plt.Rectangle((0, 0), 1, 1, color=cmap(i)) for i in range(len(models))]
        ax.legend(handles, models, title="Models", loc="upper right")

    fig.tight_layout()
    plt.show()
