import pandas as pd

from sklearn.preprocessing import StandardScaler


def standard_scaler(df):

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    scaled_df = pd.DataFrame(scaled, columns=df.columns)

    return scaled_df