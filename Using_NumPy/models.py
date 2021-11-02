#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 21:46:32 2021

@author: thierryk
"""

import numpy as np

import functions as fc

def model_forward(X, parameters):
    """
    Implement the linear portion of forward propagation for a single layer (layer l)

    Parameters
    ----------
    X : np.array of shape (n[0], m)
        Data input.
    parameters : dict
        Output of initialize_parameters_deep().

    Returns
    -------
    AL : np.array
        Activation value from the output (last) layer, i.e. prediction vector,
        also called yhat
    caches : list
        caches containing: every cache of linear_activation_forward() 
        (there are L of them, indexed from 0 to L-1).

    """
    caches = []
    A = X
    L = len(parameters) // 2 # number of layers in the neural network
    
    for l in range(1, L):
        A_prev = A
        W = parameters["W"+str(l)]
        b = parameters["b"+str(l)]
        activation = "relu"
        A, cache = fc.linear_activation_forward(A_prev, W, b, activation)
        caches.append(cache)
    
    A_prevL = A
    WL = parameters["W"+str(l+1)]
    bL = parameters["b"+str(l+1)]
    activationL = "sigmoid"
    AL, cache = fc.linear_activation_forward(A_prevL, WL, bL, activationL)
    
    caches.append(cache)
    
    return AL, caches


def model_forward_dropout(X, parameters, keep_prob):
    """
    Implement the linear portion of forward propagation for a single layer (layer l)
    with a dropout regularization.
    
    Parameters
    ----------
    X : np.array of shape (n[0], m)
        Data input.
    parameters : dict
        Output of initialize_parameters_deep().
    keep_prob : float
        Probability that a given hidden unit will be kept [0,1].
        
    Returns
    -------
    AL : np.array
        Activation value from the output (last) layer, i.e. prediction vector,
        also called yhat
    caches : list
        caches containing: every cache of linear_activation_forward() 
        (there are L of them, indexed from 0 to L-1).

    """
    A = X
    caches = []
    L = len(parameters) // 2 # number of layers in the neural network
    listD = []
    
    for l in range(1, L):       
        A_prev = A
        W = parameters["W"+str(l)]
        b = parameters["b"+str(l)]
        activation = "relu"
        A, cache = fc.linear_activation_forward(A_prev, W, b, activation)
        caches.append(cache)
        
        D = np.random.rand(A.shape[0], A.shape[1])
        D = (D<keep_prob).astype(int) # mask creation
        A = A * D
        A = A / keep_prob
        
        listD.append(D)
    
    ### Randomly shut down some neurons 
    
    
    ### For the output layer
    A_prevL = A
    WL = parameters["W"+str(l+1)]
    bL = parameters["b"+str(l+1)]
    activationL = "sigmoid"
    AL, cache = fc.linear_activation_forward(A_prevL, WL, bL, activationL)
    
    caches.append(cache)
    
    return AL, caches, listD


def model_backward(AL, Y, caches):
    """
    Implement the backward propagation for the 
    [LINEAR->RELU] * (L-1) -> LINEAR -> SIGMOID group

    Parameters
    ----------
    AL : np.array of shape Y.shape
        Probability vector, output of the forward propagation (L_model_forward()).
        Also called yhat.
    Y : np.array
        True "label" vector (containing 0 or 1).
    caches : list
        Contain: every cache of linear_activation_forward() with "relu" 
        (it's caches[l], for l in range(L-1) i.e l = 0...L-2) and the cache 
         of linear_activation_forward() with "sigmoid" (it's caches[L-1]).

    Returns
    -------
    grads : dict
        A dictionary with the gradients.

    """
    grads = {}
    L = len(caches) # the number of layers
    #m = AL.shape[1]
    Y = Y.reshape(AL.shape) # Y is now the same shape as AL
    
    dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))
    
    current_cache = caches[L-1]
    dA_prev_temp, dW_temp, db_temp = fc.linear_activation_backward(dAL, current_cache, 'sigmoid')
    grads["dA" + str(L-1)] = dA_prev_temp
    grads["dW" + str(L)] = dW_temp
    grads["db" + str(L)] = db_temp
    
    for l in reversed(range(L-1)):
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = fc.linear_activation_backward(grads["dA" + str(l+1)], current_cache, 'relu')
        grads["dA" + str(l)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp
    
    return grads


def model_backward_dropout(AL, Y, caches, listD, keep_prob):
    """
    Implement the backward propagation for the 
    [LINEAR->RELU] * (L-1) -> LINEAR -> SIGMOID group with dropout regularization.

    Parameters
    ----------
    AL : np.array of shape Y.shape
        Probability vector, output of the forward propagation (L_model_forward()).
        Also called yhat.
    Y : np.array
        True "label" vector (containing 0 or 1).
    caches : list
        Contain: every cache of linear_activation_forward() with "relu" 
        (it's caches[l], for l in range(L-1) i.e l = 0...L-2) and the cache 
         of linear_activation_forward() with "sigmoid" (it's caches[L-1]).
    keep_prob : float
        Probability that a given hidden unit will be kept [0,1].

    Returns
    -------
    grads : dict
        A dictionary with the gradients.

    """
    grads = {}
    L = len(caches) # the number of layers
    #m = AL.shape[1]
    Y = Y.reshape(AL.shape) # Y is now the same shape as AL
    
    dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))
    
    current_cache = caches[L-1]
    dA_prev_temp, dW_temp, db_temp = fc.linear_activation_backward(dAL, current_cache, 'sigmoid')
    grads["dA" + str(L-1)] = dA_prev_temp
    grads["dW" + str(L)] = dW_temp
    grads["db" + str(L)] = db_temp
    
    for l in reversed(range(L-1)):
        current_cache = caches[l]
        
        dA_prev_temp, dW_temp, db_temp = fc.linear_activation_backward(grads["dA" + str(l+1)], current_cache, 'relu')
        dA_prev_temp = dA_prev_temp * listD[l] ### est-ce que listD.size <==> listD[L] ?
        dA_prev_temp = dA_prev_temp / keep_prob
        
        grads["dA" + str(l)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp
    
    return grads


def model_backward_L2regularization(AL, Y, caches, lambd):
    """
    Implement the backward propagation for the 
    [LINEAR->RELU] * (L-1) -> LINEAR -> SIGMOID group with a L2 regularization.

    Parameters
    ----------
    AL : np.array of shape Y.shape
        Probability vector, output of the forward propagation (L_model_forward()).
        Also called yhat.
    Y : np.array
        True "label" vector (containing 0 or 1).
    caches : list
        Contain: every cache of linear_activation_forward() with "relu" 
        (it's caches[l], for l in range(L-1) i.e l = 0...L-2) and the cache 
         of linear_activation_forward() with "sigmoid" (it's caches[L-1]).
    labmd : float
        Regularization factor

    Returns
    -------
    grads : dict
        A dictionary with the gradients regularized.

    """
    grads = {}
    L = len(caches) # the number of layers
    m = AL.shape[1]
    Y = Y.reshape(AL.shape) # Y is now the same shape as AL
    
    dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))
    
    current_cache = caches[L-1]
    dA_prev_temp, dW_temp, db_temp = fc.linear_activation_backward(dAL, current_cache, 'sigmoid')
    grads["dA" + str(L-1)] = dA_prev_temp
    grads["dW" + str(L)] = dW_temp + (lambd/m) * dW_temp   ### regularization + (lambd/m) * dW_temp
    grads["db" + str(L)] = db_temp + (lambd/m) * db_temp   ### regularization + (lambd/m) * db_temp
    
    for l in reversed(range(L-1)):
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = fc.linear_activation_backward(grads["dA" + str(l+1)], current_cache, 'relu')
        grads["dA" + str(l)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp + (lambd/m) * dW_temp    ### regularization + (lambd/m) * dW_temp
        grads["db" + str(l + 1)] = db_temp + (lambd/m) * db_temp    ### regularization + (lambd/m) * db_temp
        
    return grads





def update_parameters(parameters, grads, learning_rate):
    """
    Update parameters using gradient descent

    Parameters
    ----------
    params : dict
        Containing the parameters.
    grads : dict
        Contain the grads output of model_backward.
    learning_rate : float
        Tune the rate of learning.

    Returns
    -------
    parameters : dict
        Contain the update parameters.

    """
    # parameters = params.copy()
    L = len(parameters) // 2 # number of layers in the neural network
    
    for l in range(L):
        parameters["W" + str(l+1)] = parameters["W" + str(l+1)] - \
            learning_rate * grads["dW" + str(l+1)]
        parameters["b" + str(l+1)] = parameters["b" + str(l+1)] - \
            learning_rate * grads["db" + str(l+1)]
    
    return parameters


def predict(X, y, parameters, training_set=True):
    """
    Function used to predict the results of a  L-layer neural network.

    Parameters
    ----------
    X : np.array
        Input dataset.
    y : np.array
        True "label" vector (containing 0 or 1).
    parameters : dict
        Parameters of the trained model.
    training_set : bool, optional
        Verbose parameter

    Returns
    -------
    p : TYPE
        DESCRIPTION.

    """
    if training_set : 
        name = "Training"
    else:
        name = "Validation"
    
    m = X.shape[1]
    p = np.zeros((1,m))
    
    # Forward pass
    probas, caches = model_forward(X, parameters)
    
    for i in range(0, probas.shape[1]):
        if probas[0,i] > 0.5:
            p[0,i] = 1
        else:
            p[0,i] = 0
                  
    print(f"{name} Accuracy: " + str(np.sum((p == y)/m)))
    
    return p