import numpy as np
import pandas as pd
from empyrical import roll_sortino_ratio, roll_max_drawdown, roll_alpha_beta, roll_sharpe_ratio

def create_sharpe_ratio(returns,periods=20):
    return (
        np.sqrt(periods) *
        np.mean(returns) /
        np.std(returns)
    )


def create_drawdowns(equity_curve):
    high_watermark = [0]
    curve_index = equity_curve.index
    drawdown = pd.Series(index=curve_index)
    duration = pd.Series(index=curve_index)

    for i in range(1, len(curve_index)):
        current_high_watermark = max(
            high_watermark[i-1],
            equity_curve[i]
        )
        high_watermark.append(current_high_watermark)

        drawdown[i] = high_watermark[i] - equity_curve[i]
        duration[i] = 0 if drawdown[i] == 0 else duration[i-1] + 1

    return drawdown.max(), duration.max()


def get_rolling_performance_metrics(series:list, _window=5):
    if len(series) < _window:
        return {
            "sortino": [],
            "sharpe": [],
            "alpha_beta": [],
            "drawdown": []
        }
    

    sortino = roll_sortino_ratio(series, window=_window)
    sharpe = roll_sharpe_ratio(series, window=_window)
    alpha_beta = roll_alpha_beta(series, window=_window)
    drawdown = roll_max_drawdown(series, window=_window)
    
    return {
        "sortino": sortino,
        "sharpe": sharpe,
        "alpha_beta": alpha_beta,
        "drawdown": drawdown
    }