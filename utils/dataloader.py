import pandas as pd

def load_data(path):
    # on_bad_lines='skip' will ignore rows that have extra commas
    # sep=None + engine='python' tells pandas to automatically detect the separator
    df = pd.read_csv(path, encoding="latin1", on_bad_lines='skip', sep=None, engine='python')
    return df


