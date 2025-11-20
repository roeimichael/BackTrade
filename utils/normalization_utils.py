import numpy as np
from typing import List, Union


def windownorm_normalization(data: List[float], window_size: int) -> List[Union[float, None]]:
    normalized_data = []
    for i in range(len(data) - window_size):
        sublist = data[i:i + window_size]
        m = np.mean(sublist)
        std = np.std(sublist)
        if std == 0:
            normalized_data.append(0)
        else:
            normalized_data.append((data[i] - m) / std)
    normalized_data.extend([None] * window_size)
    return normalized_data


def tanh_normalization(data: np.ndarray) -> np.ndarray:
    m = np.mean(data)
    std = np.std(data)
    if std == 0:
        return np.zeros_like(data)
    return 0.5 * (np.tanh(0.01 * ((data - m) / std)) + 1)


def normdist_normalization(data: np.ndarray) -> np.ndarray:
    m = np.nanmean(data)
    std = np.nanstd(data)
    if std == 0:
        return np.zeros_like(data)
    return (data - m) / std


def sigmoid_normalization(data: List[float]) -> List[float]:
    return [1 / (1 + np.exp(-x)) for x in data]


def median_normalization(data: np.ndarray) -> np.ndarray:
    m = np.median(data)
    if m == 0:
        return np.zeros_like(data)
    return data / m


def min_max_normalization(data: np.ndarray) -> np.ndarray:
    min_val = min(data)
    max_val = max(data)
    if max_val == min_val:
        return np.zeros_like(data)
    return (data - min_val) / (max_val - min_val)
