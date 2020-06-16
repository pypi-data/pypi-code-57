# import libraries:
import sys, os
sys.path.insert(0,os.path.realpath(os.path.join(os.getcwd(),'../..')))
from getdist import plots, MCSamples
from getdist.gaussian_mixtures import GaussianND
import getdist
import scipy
import matplotlib.pyplot as plt
import numpy as np
# import the tensiometer tools that we need:
from tensiometer import utilities
from tensiometer import chains_convergence
from tensiometer import pymaxent

# load the chains (remove no burn in since the example chains have already been cleaned):
chains_dir = './test_chains/'
# the DES Y1 3x2 chain:
chain = getdist.mcsamples.loadMCSamples(file_root=chains_dir+'DES', no_cache=True)


# expand in moments:
par_ind = 7
pippo = chain.get1DDensityGridData(par_ind)
pippo.normalize()

pippo.bounds()


total_weights = np.sum(chain.weights)
mean = np.dot(chain.weights, chain.samples[:,par_ind])/total_weights
moments = [ np.dot(chain.weights, (chain.samples[:,par_ind])**k)/total_weights for k in range(100)]

sol1,lambdas1 = pymaxent.reconstruct(moments[:3],bnds=[np.amin(pippo.x), np.amax(pippo.x)])
sol2,lambdas2 = pymaxent.reconstruct(moments[:5],bnds=[np.amin(pippo.x), np.amax(pippo.x)])
sol3,lambdas3 = pymaxent.reconstruct(moments[:7],bnds=[np.amin(pippo.x), np.amax(pippo.x)])

plt.plot(pippo.x, pippo.P)
plt.plot(pippo.x, sol1(pippo.x))
plt.plot(pippo.x, sol2(pippo.x))
plt.plot(pippo.x, sol3(pippo.x))

# cut the chains:
chains = utilities.get_separate_mcsamples(chain)
max_elements = np.log10(np.amin([len(ch.samples) for ch in chains]))

num_el_fine = np.logspace(1, max_elements,1000).astype('int')
num_el_fine = np.unique(num_el_fine)
num_el_coarse = np.logspace(1, np.floor(max_elements),4).astype('int')
num_el_coarse = np.unique(num_el_coarse)




res_GR = []
for ind in range(len(num_el_fine)):
    temp_samples = [ samps[0:num_el_fine[ind]] for samps in samples]
    res_GR.append(compute_R0(temp_samples))
res_GR = np.array(res_GR)



# convergence of the parameter:

# convergence of moments:

# now look at multi dimensions: is the result the same?

# what is the result for the minimum?

# what is the worse mode?

# what happens to higher moments?

# same thing with only two chains:


import numpy as np
import matplotlib.pyplot as plt
import getdist
from getdist import plots, MCSamples


axes[1,1]




X = np.random.multivariate_normal(mean=np.array([1,2]), cov=np.array([[1.,0.5],[0.5,2.]]), size=1000)
x,y = X[:,0], X[:,1]
sample = MCSamples(samples=X, names=['x','y'])
fig, axes = plt.subplots(2,2, figsize=(4,4))
axes[1,1].scatter(x,y, s=1)
g = getdist.plots.get_subplot_plotter(rc_sizes=True)
g.plot_2d([sample], param1='x', param2='y', lw=1)

pass
