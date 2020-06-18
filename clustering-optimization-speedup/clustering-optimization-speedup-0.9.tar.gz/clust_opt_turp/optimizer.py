import cvxpy as cp
import numpy as np


def optimize_port(data, value, returns, criterion='return_bound'):
    """
    :param data: data on stock assets prices for clustering, format: each array row is
        data on prices changes in period at percents from the beginning of the beginning of the period
        (e.g. first value in row = 1.0)
    :param value: optimization criterion value:
        risk if criterion="risk_bound"
        return if criterion="return_bound",
        gamma if criterion="risk_return"
    :param criterion: optimization method - by risk bound ("risk_bound"), value bound ("return_bound")
        or RAPOC ("risk_return")
    :param returns: vector of assets returns
    :return: vector of assets weights in optimal portfolio
    """
    CV = np.cov(data)
    weights_var = cp.Variable(data.shape[0])
    return_var = returns * weights_var
    risk_var = cp.quad_form(weights_var, CV)
    if criterion == "risk_bound":
        prob = cp.Problem(cp.Maximize(return_var), [risk_var <= cp.Parameter(name="max_risk", value=value, nonneg=True),
                                                    cp.sum(weights_var) == 1, weights_var >= 0])
    elif criterion == "return_bound":
        prob = cp.Problem(cp.Minimize(risk_var), [return_var >= cp.Parameter(name="min_ret", value=value, nonneg=True),
                                                  cp.sum(weights_var) == 1, weights_var >= 0])
    elif criterion == "risk_return":
        prob = cp.Problem(cp.Maximize(return_var - cp.Parameter(name="gamma", value=value, nonneg=True) * risk_var),
                          [cp.sum(weights_var) == 1, weights_var >= 0])
    prob.solve()
    return weights_var.value
