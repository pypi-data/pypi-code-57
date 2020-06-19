import numpy as np
import copy
import os

from scrinet.greedy import greedyrb
from scrinet.fits import poly
from scrinet.fits import gprfit
from scrinet.fits import nn

import george
from george import kernels


class Surrogate(object):
    def __init__(self, integration, basis_method='eim', output_dir=""):
        """
        basis_method {str}: default 'eim'. Can also be 'rb'
            Choose which method to use as the basis.
            Either 'eim' which is the empirical interpolation method
            or 'rb' which is the reduced basis method
        output_dir {str}: default ""
            directory where things will be saved.
            will default to current directory
        """
        self.integration = integration
        self.basis_method = basis_method
        self.output_dir = output_dir
        if self.output_dir:
            os.makedirs(f"{self.output_dir}", exist_ok=True)
        else:
            self.output_dir = "./"

        self.grb = greedyrb.GreedyReducedBasis(
            integration=self.integration
        )

        pass

    def build_seed_basis(self, ts, ts_coords):
        self.grb.build_seed_basis(ts=ts, ts_coords=ts_coords)

    def run_greedy_sweep(self, ts, ts_coords, greedy_tol=1e-4, verbose=False):
        self.grb.greedy_sweep(
            ts, ts_coords, greedy_tol=greedy_tol, verbose=verbose)

    def setup_eim(self):
        self.grb.setup_eim()

    def build_eim(self, ts):
        self.grb.build_eim(ts)

    def get_basis(self):
        if self.basis_method == 'eim':
            if hasattr(self.grb, 'eim') is False:
                self.setup_eim()
            basis = self.grb.eim.B
        elif self.basis_method == 'rb':
            basis = self.grb.basis
        return basis

    def compute_projection_coefficients(self, ts):
        """
        given an input training set (ts) compute projection
        coefficients using the current self.basis_method
        """

        if self.basis_method == 'eim':
            try:
                idxs = self.grb.eim.indices
            except AttributeError as error:
                print(
                    "Can't find EIM indicies. Perhaps you forgot to construct the EIM with self.grb.build_eim()", flush=True)
                raise
            alpha = np.transpose(ts)[idxs].T
        elif self.basis_method == 'rb':
            alpha = self.grb.compute_projection_coefficients_array(
                self.grb.basis, ts)

        return alpha

    def save_basis(self, filename):
        """
        saves the basis as a "filename.npy" file
        """
        basis = self.get_basis()
        np.save(os.path.join(self.output_dir, filename), basis)

    def fit_eim(self, X, y, maxdegs=None, max_deg_total=None, method='lr', epochs=1000, scaleX=False, scaleY=False, verbose=True, nn_outname="best.h5", validation_data=None, nn_verbose=0, batch_size=None, outname_prefix=""):
        """
        X: domain.shape = (N, M): N = number of greedy points, M = dimensionality.
            e.g., if non-spinning then M=1
        y: range.shape = (P, N) where P is the number of outputs
            EIM data or RB data
        method: default = 'lr' == linear polynomial basis regression
        epochs, scaleX, scaleY, nn_outname: only for method='nn'
        nn_outname: name of output h5 file. '.h5' get appended automatically
        """
        self.method = method
        self.scaleX = scaleX
        self.scaleY = scaleY

        if self.method == 'lr':
            if maxdegs is None:
                raise ValueError("maxdegs is None")
            if max_deg_total is None:
                raise ValueError("max_deg_total is None")

        if X.shape[1] > 1 and method == 'gpr':
            raise NotImplementedError(
                f"Dimension is: {X.shape[0]}. GPR only implemented for 1D at the moment.")

        fits = []

        if self.method == 'nn':
            fit = nn.RegressionANN()
            if verbose:
                print("\n====\ntraining NN\n====\n", flush=True)

            nn_outname = os.path.join(self.output_dir, nn_outname)
            self.history = fit.fit(
                X,
                y.T,
                input_dim=X.shape[1],
                noutput=y.shape[0],
                epochs=epochs,
                validation_data=validation_data,
                outname=nn_outname,
                scaleX=self.scaleX,
                scaleY=self.scaleY,
                verbose=nn_verbose,
                batch_size=batch_size
            )

            fit.load_model(nn_outname)
            fits.append(fit)

        if verbose and self.method == 'nn':
            self.plot_history(outname=outname_prefix)

        for i, ydata in enumerate(y):

            if self.method == 'lr':
                max_degs = poly.generate_degrees(
                    maxdegs=maxdegs, max_deg_total=max_deg_total)
                fit, _ = poly.findpolyfit(
                    X,
                    ydata,
                    max_degs=max_degs,
                    output_best=True,
                    verbose=False
                )
                fits.append(fit)
            elif self.method == 'gpr':
                #                 solver in [george.HODLRSolver, george.BasicSolver]
                solver = george.BasicSolver
                jitter = 1e-4
                yerr = np.zeros(ydata.shape) + jitter
                fit = gprfit.GPRFit(X, ydata, yerr=yerr)
                kernel = np.var(ydata) * \
                    kernels.ExpSquaredKernel(0.5, ndim=1, axes=0)
                fit.setup_kernel(kernel)

                fit.fit(solver=solver)
                fit.opt()
                fits.append(fit)

            if verbose:
                self.plot_fit(
                    X, ydata, fit, i, validation_data=validation_data, outname_prefix=outname_prefix)

        self.fits = fits

    def plot_history(self, outname=None):
        """
        outname {str}, default is None
            shoule be something like 'loss.png'
        """
        import matplotlib
        import matplotlib.pyplot as plt

        plt.figure()
        plt.plot(self.history.history['loss'], label='training loss')
        if 'val_loss' in self.history.history.keys():
            plt.plot(self.history.history['val_loss'], label='validation loss')
        plt.yscale('log')
        plt.ylabel('loss')
        plt.xlabel('epochs')
        plt.legend()
        plt.tight_layout()
        if outname:
            outname = os.path.join(self.output_dir, f"{outname}_loss.png")
            plt.savefig(outname)
        else:
            plt.show()
        plt.close()

    def plot_fit(self, X, ydata, fit, basis_idx, validation_data=None, outname_prefix=None):
        """
        outname_prefix {str}, default is None
            final outname will be f"{outname_prefix}_{basis_idx}.png"
        basis_idx {int}
            basis number to plot
        validation_data {2 tuple}, default is None
            (Xval, yval)
        """
        import matplotlib
        import matplotlib.pyplot as plt

        if self.method == 'lr':
            yhat = fit.predict(X)
        elif self.method == 'gpr':
            # haven't implemented uncertainty
            yhat, _ = fit.predict(X)
        elif self.method == 'nn':
            yhat = fit.predict(X).T[basis_idx]

        if X.shape[1] == 1:
            xhat = np.linspace(
                X.min(),
                X.max(),
                1000)
            if self.method == 'lr':
                yhat_cont = fit.predict(xhat.reshape(-1, 1))
                xhat = np.exp(xhat)
                x2 = np.exp(X.ravel())
            elif self.method == 'gpr':
                # haven't implemented uncertainty
                yhat_cont, _ = fit.predict(xhat.reshape(-1, 1))
                xhat = np.exp(xhat)
                x2 = np.exp(X.ravel())
            if self.method == 'nn':
                yhat_cont = fit.predict(xhat.reshape(-1, 1)).T[basis_idx]
                xhat = np.exp(xhat)
                x2 = np.exp(X.ravel())
            plt.figure()
            plt.title(f"basis number = {basis_idx}")

            if validation_data:
                xval = np.exp(validation_data[0])
                yval = validation_data[1][:, basis_idx]
                plt.scatter(xval, yval, label='validation')

            plt.plot(xhat, yhat_cont, label='extrap', c='C1')
            plt.scatter(x2, ydata, label='data', s=50, c='r', lw=2)
            plt.scatter(x2, yhat, label='fit', marker='x', s=100, lw=2, c='k')
            plt.legend()
            plt.tight_layout()
            if outname_prefix:
                outname = os.path.join(
                    self.output_dir, f"{outname_prefix}_{basis_idx}.png")
                plt.savefig(outname)
            else:
                plt.show()
            plt.close()
        else:
            plt.figure()
            plt.title(f"basis number = {basis_idx}")
            range_x = range(len(yhat))
            plt.scatter(range_x, ydata, label='data', s=50, c='r', lw=2)
            plt.scatter(range_x, yhat, label='fit',
                        marker='x', s=100, lw=2, c='k')
            plt.legend()
            plt.tight_layout()
            if outname_prefix:
                outname = os.path.join(
                    self.output_dir, f"{outname_prefix}_{basis_idx}.png")
                plt.savefig(outname)
            else:
                plt.show()
            plt.close()

    def predict(self, coords, log_index=0):
        """
        coords.shape = (1, M), M=dimension
        log_index: take the log of the log_index'th component.
            by default this is the 0th index.
            Use `log_index=None` to not modify the `coords`.
        """
        coords = np.array(coords)

        assert len(
            coords.shape) > 1, f"expected shape is (1, M) but got {coords.shape}"

        if log_index != None:
            coords[0, log_index] = np.log(coords[0, log_index])

        alpha = np.zeros(len(self.fits))

        if self.method == 'lr':
            for i, fit in enumerate(self.fits):
                alpha[i] = fit.predict(coords)
        elif self.method == 'gpr':
            for i, fit in enumerate(self.fits):
                # haven't implemented uncertainty
                alpha[i], _ = fit.predict(coords)
        elif self.method == 'nn':
            alpha = self.fits[0].predict(coords)[0]

        if self.basis_method == 'eim':
            basis = self.grb.eim.B
        elif self.basis_method == 'rb':
            basis = self.grb.basis

        return np.dot(alpha, basis)

    def validate_surrogate(self, vts, vts_coords, x=None, a=None, b=None):
        """
        vts: validation training set
            vts.shape() = (N, P)
                N = number of entries
                P = number of points e.g. length of time or frequency series
        vts_coords: validation training set coordinates / parameters
            vts_coords.shape() = (N, M).
                N = number of entries
                M = dimensionality
        x: np.ndarray of shape (P,). Default: None
        a, b: float/int. the start and end values of x for integration.
            Default: None
        """
        if self.method in ['lr', 'gpr', 'nn']:
            log_index = 0
        # elif self.method == 'nn':
        #     log_index = None

        if x is not None:
            if a is None:
                a = x[0]
            if b is None:
                b = x[-1]
            mask = (x >= a) & (x <= b)
            x = x[mask]
            integration = greedyrb.Riemann([a, b], len(x))
        else:
            integration = self.grb.integration
            # mask that is all True
            mask = np.ones(vts[0].shape).astype(np.bool)

        model_errors = np.zeros(len(vts))
        for i in range(len(vts)):
            yhat = self.predict([vts_coords[i]], log_index=log_index)[mask]
            y = vts[i][mask]
            # error = self.grb.integration.norm(y-yhat)**2
            error = integration.norm(y-yhat)**2
            model_errors[i] = error

        worst_error_index = np.argmax(model_errors)
        worst_case = vts_coords[worst_error_index]

        return model_errors, worst_case, worst_error_index
