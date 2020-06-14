import numpy as np
from scipy import stats


def cross_correlate(a, b, metric=stats.pearsonr):
    assert len(a)==len(b)
    n = len(a)
#     print(f'signal: {n}')
    w = n//2
#     print(f'window: {w}')
    metric(a,b)[0]

    i = (n-w)//2
    j = i + w
#     print((i,j), len(b[i:j]))

    lags = np.arange(-i,n-j)

    rhos = [metric(a[i:j], b[i+lag:j+lag])[0]
            for lag in lags]

    return lags, rhos


if True:
    import numpy as np
    import matplotlib.pyplot as plt

    k = np.linspace(0, 2*np.pi, 1000)
    a = np.sin(k)
    b = np.roll(a, 50)

    plt.plot(k, a, label='a')
    plt.plot(k, b, label='b')
    plt.legend()
    plt.show()

    lags, rhos = cross_correlate(a, b)
    plt.plot(lags, rhos)
    

if True:
    # https://currents.soest.hawaii.edu/ocn_data_analysis/_static/SEM_EDOF.html
    
    npts = 500
    x = np.linspace(0, 50, npts)
    y1 = 5 * np.sin(x/2) + np.random.randn(npts)
    y2 = 5 * np.cos(x/2) + np.random.randn(npts)

    lags = np.arange(-npts + 1, npts)
    ccov = np.correlate(y1 - y1.mean(), y2 - y2.mean(), mode='full')
    ccor = ccov / (npts * y1.std() * y2.std())

    fig, axs = plt.subplots(nrows=2)
    fig.subplots_adjust(hspace=0.4)
    ax = axs[0]
    ax.plot(x, y1, label='y1')
    ax.plot(x, y2, label='y2')
    ax.set_ylim(-10, 10)
    ax.legend(loc='upper right', fontsize='small', ncol=2)

    ax = axs[1]
    ax.plot(lags, ccor)
    ax.set_ylim(-1.1, 1.1)
    ax.set_ylabel('cross-correlation')
    ax.set_xlabel('lag of y1 relative to y2')

    maxlag = lags[np.argmax(ccor)]
    print("max correlation is at lag %d" % maxlag)