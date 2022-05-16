
def printVersions():
    # printout the used versions
    import sys
    print('Python ' + sys.version)

    from numpy import __version__
    print('Numpy ' + __version__)

    # from https://stackoverflow.com/a/42121886
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    from tensorflow import __version__
    print('TensorFlow ' + __version__)

    from tensorflow.keras import __version__
    print('Keras ' + __version__)

    from qkeras import __version__
    print('QKeras ' + __version__)

    # from https://stackoverflow.com/a/53763710
    import warnings
    warnings.filterwarnings("ignore")

    from hls4ml import __version__
    print('HLS4ML ' + __version__)


if __name__ == "__main__":
    printVersions()
