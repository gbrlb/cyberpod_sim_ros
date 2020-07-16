#!/usr/bin/env python 
# license removed for brevity

import rospy 
from cyberpod_sim_ros.msg import * 
import numpy as np
import scipy as sp 
import sklearn.metrics
from sklearn.metrics.pairwise import euclidean_distances, rbf_kernel

class regression_perception: 

    state_image_ = state()
    state_predicted_ = state()

    def __init__(self):
        # Init pubs, subs
        self.sub_state_image_ = rospy.Subscriber('state_image', state, self.imageCallback )
        self.pub_state_predicted_ = rospy.Publisher('input', state, queue_size=1) 

        self.load_model()

    def load_model(self):
        train_data_fn = 'gridded_data.csv'
        test_data = 'uniform'

        # loading model parameters
        data = np.load('../data/coeff_train{}_test{}.npz'.format(train_data_fn, test_data))
        self.coeff = data['coeff'] # n_train by n_target
        self.gamma = data['gamma'] # scalar parameter for RBF kernel
        self.Xs_train = data['Xs_train'] # n_train by n_features training data

    def predict(self, Xs):
        # compute exp(-gamma * ||Xs - Xs_train||^2)
        # K = euclidean_distances(Xs, self.Xs_train, squared=True) # fast implementation
        # K *= -self.gamma
        # np.exp(K, K)  # exponentiate K in-place
        K = rbf_kernel(Xs, self.Xs_train, gamma=self.gamma)
        return np.dot(K, self.coeff)

    def imageCallback(self, data):
        self.state_image_ = data
        self.predict(image.reshape(1, -1))

    def estimateCallback(self):
        self.state_predicted = self.predict(self.state_image_.reshape(1, -1))
        self.pub_state_predicted_.publish(self.state_predicted)


def run_perception():
    perception = regression_perception()

    
    
    rospy.init_node('perception', anonymous=True)
    rate = rospy.Rate(10) 
    while not rospy.is_shutdown(): 
        rate.sleep()

if __name__ == "__main__": 
    try: 
        run_perception()
    except rospy.ROSInterruptException: 
        pass