import pandas as pd
def keep(keep_list,path):
    keep_pd = pd.DataFrame([keep_list], columns=keep_list)
    keep_pd.to_csv(path, index=0, encoding="utf-8")

def get(path):
    return list(pd.read_csv(path).values[0])