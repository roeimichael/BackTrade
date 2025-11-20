import pandas as pd
from config.path_config import PathConfig
from utils.file_utils import read_lines_from_file


def find_outliers_IQR(df):
    q1 = df.quantile(0.25)
    q3 = df.quantile(0.75)
    IQR = q3 - q1
    outliers = df[((df < (q1 - 1.5 * IQR)) | (df > (q3 + 1.5 * IQR)))]
    return outliers


def analyze_outliers(dates_dir=None, columns_file=None):
    if dates_dir is None:
        dates_dir = PathConfig.DATA_DATES2_DIR

    if columns_file is None:
        columns_file = PathConfig.COLUMNS_SMALL_FILE

    dates_list = read_lines_from_file(PathConfig.DATES_FILE)
    cols = read_lines_from_file(columns_file)

    outlier_counts = {}

    for col in cols:
        if all(x not in col for x in ["CDL", "Date", "ticker", "Unnamed"]):
            outlier_counts[col] = 0

    for date in dates_list:
        date_file = dates_dir / f"{date}.csv"

        try:
            df = pd.read_csv(date_file)

            for col in cols:
                if col in outlier_counts and col in df.columns:
                    outliers = find_outliers_IQR(df[col])
                    outlier_counts[col] += len(outliers)

        except FileNotFoundError:
            print(f"File not found: {date_file}")
            continue
        except Exception as e:
            print(f"Error processing {date}: {e}")
            continue

    output_file = PathConfig.DATA_DIR / "DictFile.txt"
    with open(output_file, "w") as file:
        for key, value in outlier_counts.items():
            file.write(f'{key}:{value}\n')

    print("\nOutlier counts by column:")
    for key, value in outlier_counts.items():
        print(f"{key}: {value}")

    return outlier_counts


if __name__ == '__main__':
    analyze_outliers()
