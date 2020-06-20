from matplotlib import pyplot as plt
from figure import FuncFig
import numpy as np

if __name__ == "__main__":
	fig, ax = plt.subplots(FigureClass=FuncFig, animate=True, time = 5)

	# f1 = ax.add_func(lambda x: np.exp(- (x-0.5) ** 2 / 0.1), x0=0, x1 = 1, marker="s", markevery=[5, 20, 30], timings=[0,1])
	# f2 = ax.add_func(lambda x: np.sin(5*x), x0=0, x1=1, sample_per_it=2, color="blue", timings=[2, 3])
	# ax.fill_between(f1, f2, timings=[2,3])

	f = ax.add_func(lambda x, t: np.exp( - (x - 0.5) ** 2 / (0.01*t+1e-3)**.5), x0=0, x1=1, timings=[0, 5], is_functional=True)

	fig.render()

	# fig.save()

	plt.show()
