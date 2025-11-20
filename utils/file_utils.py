import pandas as pd
from pathlib import Path
from typing import List, Union


def read_lines_from_file(file_path: Union[str, Path]) -> List[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def load_csv(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
    return pd.read_csv(file_path, **kwargs)


def save_csv(df: pd.DataFrame, file_path: Union[str, Path], **kwargs) -> None:
    df.to_csv(file_path, **kwargs)
