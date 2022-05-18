import pandas as pd
import pkg_resources

# def load_segments():
#     w_s = pd.read_csv('/data/word-segments.csv')
#     return w_s

def load_segments():
    """Return a dataframe about the 68 different Roman Emperors.

    Contains the following fields:
        name        68 non-null int64
        L           68 non-null object
        prefix      68 non-null object
    ... (docstring truncated) ...

    """
    # This is a stream-like object. If you want the actual info, call
    # stream.read()

    print('Loading name segments...')
    stream = pkg_resources.resource_stream(__name__, 'data/word-segments.csv')
    return pd.read_csv(stream, encoding='latin-1')
