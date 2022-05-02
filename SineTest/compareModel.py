#!/bin/python3
import numpy as np

def getDistances( truth, predict):
    """
        return the distances between the model and the truth
    """
    distance = np.subtract( truth , predict )
    return distance


def meanAbsDistance( truth, predict ):
    """
        compare the model to truth and return the mean absolute distance
    """

    distances = getDistances( truth, predict )

    abs_distances = np.absolute(distances)

    mean_distance = np.mean(abs_distances)

    return mean_distance



