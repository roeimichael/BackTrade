import os
import pandas as pd
from config.path_config import PathConfig
from config.processing_config import ProcessingConfig
from config.model_config import ModelConfig


def add_close_change_column(data, threshold):
    data['Close Change %'] = (data['Close'] - data['Close'].shift(1)) / data['Close'].shift(1) * 100
    data[f'Over_{threshold}'] = (data['Close Change %'] > threshold).astype(int)
    return data


def merge_csv_files(path, column_name):
    merged_data = pd.DataFrame()
    csv_files = [f for f in os.listdir(path) if f.endswith(".csv")]

    for filename in csv_files:
        file_path = os.path.join(path, filename)
        data = pd.read_csv(file_path)

        if column_name in data.columns:
            column = data[[column_name]] * 100
            merged_data = pd.concat([merged_data, column], axis=1) if not merged_data.empty else column

    if not merged_data.empty:
        merged_data.columns = [f.split(".")[0] for f in csv_files]
        if 'Date' in data.columns:
            merged_data.index = data['Date']

        output_file = PathConfig.DATA_SNP_DIR / f"{column_name}.csv"
        merged_data.to_csv(output_file, index=True)


def create_binary_file(file_path, threshold, index_col):
    data = pd.read_csv(file_path, index_col=index_col)
    binary_data = (data >= threshold).astype(int)

    base_name = os.path.basename(file_path).split('.')[0]
    output_file = PathConfig.DATA_SNP_DIR / f"{base_name}_binary{threshold}.csv"
    binary_data.to_csv(output_file, index=True)


def add_num_stocks_column(sp500_file, binary_file, threshold):
    sp500_data = pd.read_csv(sp500_file)
    binary_data = pd.read_csv(binary_file)
    num_stocks = binary_data.sum(axis=1)
    sp500_data[f"Num Stocks Above {threshold}"] = num_stocks
    sp500_data.to_csv(sp500_file, index=False)


def analyze_sp500_precision(threshold=2.5):
    sp500_csv = PathConfig.DATA_SNP_DIR / "S&P500.csv"
    close_change_csv = PathConfig.DATA_SNP_DIR / f"Close Change_binary{threshold}.csv"

    add_num_stocks_column(sp500_csv, close_change_csv, threshold)

    sp_df = pd.read_csv(sp500_csv)

    if 'precision' in sp_df.columns:
        date_range = sp_df[ModelConfig.DATE_RANGE_START:ModelConfig.DATE_RANGE_END]
        avg_precision = date_range['precision'].mean()
        print(f"Average precision: {avg_precision:.4f}")
        return avg_precision
    else:
        print("Precision column not found in S&P500 data")
        return None


if __name__ == "__main__":
    analyze_sp500_precision()
