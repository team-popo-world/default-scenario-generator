import pandas as pd

from sklearn.preprocessing import StandardScaler



def standard_scaler(df):
    scaler = StandardScaler()
    
    tmp_df = df.drop("investSessionId", axis=1)
    cols = tmp_df.columns
    scaled_data = scaler.fit_transform(tmp_df)
    
    scaled_df = pd.DataFrame(scaled_data, columns=cols)
    scaled_df["investSessionId"] = df["investSessionId"].values

    return scaled_df


