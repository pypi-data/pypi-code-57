import pandas as pd
from pyutil.performance.return_series import from_nav


def __last(frame, datefmt=None):
    frame = frame.sort_index(axis=1, ascending=False)
    if datefmt:
        frame = frame.rename(columns=lambda x: x.strftime(datefmt))
    frame = frame.dropna(axis=0, how="all")
    frame["total"] = (frame + 1).prod(axis=1) - 1
    frame.index.name = "Portfolio"
    return frame


def nav(portfolios) -> pd.DataFrame:
    """
    :param portfolios: A dictionary or DataFrame of Portfolios
    :return: A dictionary of NAV curves
    """
    frame = pd.DataFrame({name: p.nav for name, p in portfolios.items()})
    frame.columns.name = "Portfolio"
    return frame


def returns(portfolios: dict) -> pd.DataFrame:
    """
    :param portfolios: A dictionary of Portfolios
    :return: A dictionary of NAV curves
    """

    frame = pd.DataFrame({name: p.returns for name, p in portfolios.items() if hasattr(p, "nav")})
    frame.columns.name = "Portfolio"
    return frame


def mtd(frame) -> pd.DataFrame:
    frame = frame.apply(lambda x: from_nav(x).tail_month)
    return __last(frame.transpose(), datefmt="%b %d").dropna(axis=0, how="all")


def ytd(frame) -> pd.DataFrame:
    frame = frame.apply(lambda x: from_nav(x).tail_year.resample(rule="M"))
    return __last(frame.transpose(), datefmt="%m").dropna(axis=0, how="all")


def recent(frame, n=15) -> pd.DataFrame:
    frame = frame.apply(lambda x: from_nav(x).recent(n=n))
    return __last(frame.tail(n).transpose(), datefmt="%b %d").dropna(axis=0, how="all").dropna(axis=1, how="all")


def sector(portfolios, symbolmap, total=False) -> pd.DataFrame:
    d = {name: portfolio.sector(symbolmap=symbolmap, total=total).iloc[-1] for name, portfolio in portfolios.items()}
    return pd.DataFrame(d).dropna(axis=1, how="all")


def performance(frame, **kwargs) -> pd.DataFrame:
    return frame.apply(lambda x: from_nav(x).summary_format(**kwargs)).dropna(axis=1, how="all")


def drawdown(frame) -> pd.DataFrame:
    return frame.apply(lambda x: from_nav(x).drawdown).dropna(axis=1, how="all")


def ewm_volatility(frame, **kwargs) -> pd.DataFrame:
    return frame.apply(lambda x: from_nav(x).ewm_volatility(**kwargs)).dropna(axis=1, how="all")



