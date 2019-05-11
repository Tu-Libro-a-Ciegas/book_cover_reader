import pandas as pd
from pandas_gbq import to_gbq


def dataframe_from_json(json):
    return pd.DataFrame.from_dict(json)


