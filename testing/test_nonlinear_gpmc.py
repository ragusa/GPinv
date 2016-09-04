from __future__ import print_function
import GPinv
import numpy as np
import unittest
import tensorflow as tf
from make_LosMatrix import make_LosMatrix, AbelLikelihood

class Test_gpmc(unittest.TestCase):
    def test(self):
        """
        Abel inversion for the synthetic data.
        The observation y is generated by the latent function f
        y = A f + e
        with
        A = los-length-matrix
        """
        rng = np.random.RandomState(0)
        n = 30
        N = 40
        # radial position. 0~1
        r = np.linspace(0, 1., n)
        # height of LOS. -0.9~1
        z = np.linspace(-0.9, 0.9, N)
        # observation results at each Z
        y = np.zeros((N, 1))
        # noise amplitude on the observation
        e = 0.1
        # synthetic latent function
        f = np.exp(-(r-0.5)*(r-0.5)/0.1) + np.exp(-(r+0.5)*(r+0.5)/0.1)
        # constructing LOS-matrix
        A = make_LosMatrix(r,z)
        # synthetic signals
        y = np.dot(A, f) + e*rng.randn(N)
        # likelihood
        likelihood = AbelLikelihood(A)

        model = GPinv.nonlinear_model.NonlinearModel(
            X=r.reshape(-1,1), Y=y.reshape(-1,1),
            kern=GPinv.kernels.RBF(1),
            mean_function=GPinv.mean_functions.Constant(np.ones(1)),
            likelihood=likelihood, method='gpmc')

        #model.optimize()
        model.sample(num_samples=10, Lmax=20, epsilon=0.01, verbose=True)

if __name__ == '__main__':
    unittest.main()
