import numpy as np

print(np.arange(0, 5 ** 2).reshape(5, 5))

x = np.arange(0, 5 ** 2).reshape(5, 5)

print(x[1:-1,1:-1])

y = x[1:-1,1:-1]

print(set(x.flatten()).difference(set(y.flatten())))

z = set(x.flatten()).difference(set(y.flatten()))

print(np.random.choice(list(z), 1))