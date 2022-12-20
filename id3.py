import numpy as np
import pandas as pd


def entropy(S):
    if isinstance(S, list):
        S = pd.Series(S)

    p = -S.value_counts() \
          .div(S.count()) \
          .agg(lambda x: x*np.log2(x)) \
          .sum()

    return p


def target_entropy(S, col, target):
    p_target = entropy(S[target])
    keys = S[col].drop_duplicates()

    entropies = keys.apply(lambda _: (_, entropy(S[target][S[col][S[col] == _].index])))
    ratios = S[col].value_counts().div(len(S))
    res = np.subtract(p_target, entropies.apply(lambda _: ratios.loc[_[0]] * _[1]).sum())

    return col, res


def id3(S, *, target, exclude, verbose=True):
    try:
        if isinstance(S, dict):
            S = pd.DataFrame(S)
    except Exception as e:
        print(e)
        return

    if len(exclude) > 0:
        S = df.loc[:, ~S.columns.isin(exclude)]

    columns = S.columns
    if target not in columns:
        print(f"ERROR: {target=} is not exists in {list(columns)}")
        return

    res = columns.map(lambda x: target_entropy(S, x, target)) \
                 .to_frame(index=False) \
                 .set_index(0)

    return res


# entropies
#a = pd.Series((map(lambda col: entropy(S[col]), columns)), index=columns)
    
a = {
    "customer": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "debt": ["High", "High", "High", "Low", "Low","Low", "Low", "Low", "Low", "Low"],
    "revenue": ["High", "High", "Low", "Low", "Low","High", "High", "Low", "Low", "High"],
    "status": ["Employeer", "Employee", "Employee", "Employee", "Employeer", "Employeer", "Employee", "Employee", "Employeer", "Employeer"],
    "risk": ["Bad", "Bad", "Bad", "Good", "Bad", "Good", "Good", "Good", "Bad", "Good"]
}

df = pd.DataFrame(a)
exclude = ["customer"]

# first epoch
a = id3(df, target="risk", exclude=exclude)
print(a)
