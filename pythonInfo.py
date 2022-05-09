
def printVersions():
    # printout the used versions
    import sys
    print('Python ' + sys.version)

    from numpy import __version__
    print('Numpy ' + __version__)

    from tensorflow import __version__
    print('TensorFlow ' + __version__)

    from tensorflow.keras import __version__
    print('Keras ' + __version__)

    from hls4ml import __version__
    print('HLS4ML ' + __version__)


if __name__ == "__main__":
    printVersions()
