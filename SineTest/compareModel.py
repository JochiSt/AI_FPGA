#!/bin/python3
import numpy as np

def getDistances( truth, predict):
    """
        return the distances between the model and the truth
    """
    return truth - predict


def meanAbsDistance( truth, predict ):
    """
        compare the model to truth and return the mean absolute distance
    """

    distances = getDistances( truth, predict )

    abs_distances = np.absolute(distances)

    mean_distance = np.mean(abs_distances)

    return mean_distance



