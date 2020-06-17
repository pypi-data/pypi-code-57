from dataclasses import dataclass
import numpy as np


@dataclass
class Parameter:
    name: str
    bounds: list

    def sample(self, n):
        return np.random.uniform(*self.bounds, size=n)


class Model:
    def __init__(self, model_function: callable, params: list):
        self.model_function = model_function
        self.params = params

    def sample(self, n=None):
        """
        Samples model_function from the params distribution
        """
        params_dict = {param.name: param.sample(n) for param in self.params}
        return self.model_function(**params_dict)


if __name__ == '__main__':
    from tqdm import trange
    import matplotlib.pyplot as graph
    import seaborn as sns

    def profit_func(price, cost):
        return price - cost

    profit_model = Model(
        profit_func,
        params=[
            Parameter('cost', [3, 7]),
            Parameter('price', [10, 12])
        ]
    )

    print(f'${profit_model.sample():.2f}')

    trace = [profit_model.sample() for _ in trange(10000)]
    sns.distplot(trace, label='One at a time')

    trace = profit_model.sample(10000)
    sns.distplot(trace, label='All at once')
    graph.show()
