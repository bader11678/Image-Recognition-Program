from dataclasses import dataclass

import numpy as np
from FirstProject import mnist as data


######## FOR LATER ######################################################
# @dataclass
# class TrainingConfig:
#     """Class that utilizes the training conditions for the model"""
#     iterations: int
#     learning_rate: float

# alternative perceptron learning rule
# def train(self, x, y):
#     for j in range(len(x)):
#         error = y[j] - self.predict(x[j])
#         for i in range(len(x[j])):
#             self.weights[i] += self.r * error * x[j][i]
#         self.bias += self.r * error
#######################################################################
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def forward(X, w):
    weighted_sum = np.matmul(X, w)
    return sigmoid(weighted_sum)


def classify(X, w):
    y_hat = forward(X, w)
    labels = np.argmax(y_hat, axis=1)
    return labels.reshape(-1, 1)


def loss(X, Y, w):
    y_hat = forward(X, w)
    first_term = Y * np.log(y_hat)
    second_term = (1 - Y) * np.log(1 - y_hat)
    return -np.sum(first_term + second_term) / X.shape[0]


def gradient(X, Y, w):
    return np.matmul(X.T, (forward(X, w) - Y)) / X.shape[0]


def report(iteration, X_train, Y_train, X_test, Y_test, w):
    matches = np.count_nonzero(classify(X_test, w) == Y_test)
    n_test_examples = Y_test.shape[0]
    matches = matches * 100.0 / n_test_examples
    training_loss = loss(X_train, Y_train, w)
    print("%d - Loss: %.20f, %.2f%%" % (iteration, training_loss, matches))


def train(X_train, Y_train, X_test, Y_test, iterations, lr):
    w = np.zeros((X_train.shape[1], Y_train.shape[1]))
    for i in range(iterations):
        report(i, X_train, Y_train, X_test, Y_test, w)
        w -= gradient(X_train, Y_train, w) * lr
    report(iterations, X_train, Y_train, X_test, Y_test, w)
    return w


w = train(data.X_train, data.Y_train, data.X_test, data.Y_test, iterations=200, lr=1e-5)
