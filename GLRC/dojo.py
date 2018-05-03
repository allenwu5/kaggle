import tensorflow as tf
import numpy as np

np.random.seed(101)
tf.set_random_seed(101)

rand_a = np.random.uniform(0, 100, (5,5))
print(rand_a)

