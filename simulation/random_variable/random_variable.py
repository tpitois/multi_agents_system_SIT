import numpy as np

def simulate(name, params):
    match name:
        case "uniform":
            a = params[0]
            b = params[1]
            return (b-a)*np.random.rand() + a
        case "geom":
            return np.random.geometric(*params)
        case "norm":
            return max(np.random.normal(*params), 0.1)
        case "weibull":
            return params[1]*(-np.log(np.random.rand()))**(1/params[0])
        case "bernoulli":
            return np.random.binomial(1, params[0]) 