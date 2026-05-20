import numpy as np
from scipy.ndimage import grey_erosion, grey_dilation

def flat_structuring_element(size):
    """Return flat (binary) structuring element of length `size`."""
    return np.ones(size, dtype=bool)

def linear_structuring_element(size):
    """Return linear (ramp) structuring element."""
    return np.linspace(0, 1, size)

def morphological_opening(series, se):
    """Opening = dilation of erosion."""
    eroded = grey_erosion(series, footprint=se)
    opened = grey_dilation(eroded, footprint=se)
    return opened

def morphological_closing(series, se):
    """Closing = erosion of dilation."""
    dilated = grey_dilation(series, footprint=se)
    closed = grey_erosion(dilated, footprint=se)
    return closed

def trend_extraction(series, se_size=5, se_type='flat', operation='opening'):
    """
    Extract trend using morphological opening or closing.
    Returns trend series (same length as input).
    """
    if se_type == 'flat':
        se = flat_structuring_element(se_size)
    else:
        se = linear_structuring_element(se_size)
    if operation == 'opening':
        trend = morphological_opening(series, se)
    else:
        trend = morphological_closing(series, se)
    return trend

def anomaly_detection(series, trend):
    """Residual = original - trend. Return residual standard deviation."""
    residual = series - trend
    return np.std(residual)

def trend_slope(series):
    """Slope of the trend (linear regression) over the whole window."""
    x = np.arange(len(series))
    slope = np.polyfit(x, series, 1)[0]
    return slope

def compute_morphological_score(price_series, se_size=5, se_type='flat', operation='opening', score_type='trend_slope'):
    """
    Compute score for a single ETF price series.
    Returns:
        score: trend slope or anomaly std (lower anomaly = better? For trend slope, higher = better)
    """
    if len(price_series) < se_size:
        return 0.0
    trend = trend_extraction(price_series, se_size, se_type, operation)
    if score_type == 'trend_slope':
        score = trend_slope(trend)
    else:  # anomaly_std
        residual_std = anomaly_detection(price_series, trend)
        # We want higher score = better signal. For anomaly, lower is better, so invert.
        score = -residual_std
    return score
