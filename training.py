import pandas as pd
from numpy import savetxt
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from config.model_config import ModelConfig
from config.path_config import PathConfig
from utils.file_utils import read_lines_from_file


def create_targets():
    dates_file = PathConfig.DATES_FILE
    dates = read_lines_from_file(dates_file)[:658]

    df_targets = pd.DataFrame(columns=dates)

    for date in dates:
        date_file = PathConfig.DATA_DATES_DIR / f"{date}.csv"
        df = pd.read_csv(date_file)
        df_targets[f'{date}'] = df.get('Target', df.get('Targe'))

    df_targets.to_csv(PathConfig.DATA_DIR / "Targets.csv")


def check_nans(df):
    total_nans = df.isnull().sum().sum()
    print(f"Total NaN values: {total_nans}")
    return total_nans


def train_module(date_for_training="2021-02-26", target_date="2021-03-01"):
    date_file = PathConfig.DATA_DATES_DIR / f"{date_for_training}.csv"
    date_df = pd.read_csv(date_file)

    X = date_df.drop(['ticker'], axis=1, errors='ignore')

    target_file = PathConfig.DATA_DIR / "Targets.csv"
    target_df = pd.read_csv(target_file)
    y = target_df[target_date]

    x_train, x_test, y_train, y_test = train_test_split(
        X, y,
        test_size=ModelConfig.TEST_SIZE,
        random_state=ModelConfig.RANDOM_STATE
    )

    scaler = preprocessing.StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.fit_transform(x_test)

    clf = SVC(
        kernel=ModelConfig.SVM_KERNEL,
        C=ModelConfig.SVM_C,
        gamma=ModelConfig.SVM_GAMMA
    )
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)
    savetxt('y_pred.csv', y_pred, delimiter=',')

    print(f"Predictions saved to y_pred.csv")

    return clf, y_pred


if __name__ == '__main__':
    train_module()
