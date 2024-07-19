import os
import pandas as pd


def add_close_change_column(data, threshold):
    data['Close Change %'] = (data['Close'] - data['Close'].shift(1)) / data['Close'].shift(1) * 100
    data[f'Over_{threshold}'] = (data['Close Change %'] > threshold).astype(int)
    return data


def merge_csv_files(path, column_name):
    merged_data = pd.DataFrame()
    for i, filename in enumerate(os.listdir(path)):
        if filename.endswith(".csv"):
            data = pd.read_csv(os.path.join(path, filename))
            column = data[[column_name]] * 100
            merged_data = pd.concat([merged_data, column], axis=1) if not merged_data.empty else column
    merged_data.columns = [filename.split(".")[0] for filename in os.listdir(path) if filename.endswith(".csv")]
    merged_data.index = data['Date']
    merged_data.to_csv(f"./data/S&Pdata/{column_name}.csv", index=True)


def create_binary_file(file_path, threshold, index_col):
    data = pd.read_csv(file_path, index_col=index_col)
    binary_data = (data >= threshold).astype(int)
    output_file = f"./data/S&Pdata/{os.path.basename(file_path).split('.')[0]}_binary{threshold}.csv"
    binary_data.to_csv(output_file, index=True)


def add_num_stocks_column(sp500_file, binary_file, threshold):
    sp500_data = pd.read_csv(sp500_file)
    binary_data = pd.read_csv(binary_file)
    num_stocks = binary_data.sum(axis=1)
    sp500_data[f"Num Stocks Above {threshold}"] = num_stocks
    sp500_data.to_csv(sp500_file, index=False)


def main():
    sp500_csv = "./data/S&Pdata/S&P500.csv"
    close_change_csv = "./data/S&Pdata/Close Change_binary2.5.csv"

    # Uncomment the following lines to use the functions
    # df = pd.read_csv(sp500_csv)
    # df = add_close_change_column(df, 2.5)
    # df.to_csv(sp500_csv, index=True)

    # merge_csv_files("./data/stocks/", "Close Change")
    # create_binary_file("./data/S&Pdata/Close Change.csv", 2, "Date")

    add_num_stocks_column(sp500_csv, close_change_csv, 2.5)
    sp_df = pd.read_csv(sp500_csv)
    avg_precision = sum(sp_df[350:370]['precision']) / 20
    print(avg_precision)


if __name__ == "__main__":
    main()
