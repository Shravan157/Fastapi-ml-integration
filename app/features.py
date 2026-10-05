import pandas as pd 


FEATURES = ['age','bmi','children','smoker','smoker_obese']

def add_features(raw : pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df['bmi'] = df['weight'] / df['height'] **2
    df['smoker'] = df['smoker'].astype(int)
    df['smoker_obese'] = df['bmi'] * (df['bmi']>=30).astype(int)
    return df[FEATURES]
    