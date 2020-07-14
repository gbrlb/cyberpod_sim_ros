import numpy as np
import sklearn.metrics
import train_models
from sklearn.metrics.pairwise import euclidean_distances

train_data_fn = 'gridded_data.csv'
test_data = 'uniform'

# loading model parameters
data = np.load('../data/coeff_train{}_test{}.npz'.format(train_data_fn, test_data))
coeff = data['coeff'] # n_train by n_target
gamma = data['gamma'] # scalar parameter for RBF kernel
Xs_train = data['Xs_train'] # n_train by n_features training data

# constructing prediction function
def predict(Xs):
    # compute exp(-gamma * ||Xs - Xs_train||^2)
    K = euclidean_distances(Xs, Xs_train, squared=True) # fast implementation
    K *= -gamma
    np.exp(K, K)  # exponentiate K in-place
    return np.dot(K, coeff)

# confirming that model was loaded correctly
y_pred_old = data['y_pred']
y_pred = predict(Xs_train)
np.testing.assert_allclose(y_pred, y_pred_old)

# demonstrating prediction from image
demo_idx = 10
data = np.load('../data/' + train_data_fn.split('.')[0] + '_processed.npz')
state = data['states'][demo_idx]
image = data['images'][demo_idx]

def predict_from_single_image(image):
    # reshape image to be 1 by n_features
    return predict(image.reshape(1, -1))

print(predict_from_single_image(image), state)