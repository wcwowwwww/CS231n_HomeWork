from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]
    num_classes = W.shape[1]

    scores = np.dot(X, W)

    for i in range(num_train):
        cur_scores = scores[i, :]
        shift_scores = cur_scores - np.max(cur_scores)
        loss += -np.log(np.exp(shift_scores[y[i]])/np.sum(np.exp(shift_scores)))
        for j in range(num_classes):
            softmax_score = np.exp(shift_scores[j])/np.sum(np.exp(shift_scores))
            if j == y[i]:
                dW[:, j] += (softmax_score - 1) * X[i]
            else:
                dW[:, j] += softmax_score * X[i]

    loss /= num_train
    loss += reg * np.sum(W*W)

    dW /= num_train
    dW += 2*reg*W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]

    scores = np.dot(X, W)
    shift_scores = scores - np.max(scores, axis=1).reshape(-1, 1)

    softmax_output = np.exp(shift_scores)
    softmax_output = softmax_output / np.sum(softmax_output, axis=1).reshape(-1, 1)

    loss = -np.sum(np.log(softmax_output[np.arange(num_train), y])) / num_train + reg * np.sum(W * W)

    dScore = softmax_output
    dScore[range(num_train), y] = dScore[range(num_train), y] - 1

    dW = np.dot(X.T, dScore) / num_train + 2 * reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
