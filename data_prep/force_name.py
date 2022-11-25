
import os

list_forces = os.listdir('data/force_kmls')
import pandas as pd

df = pd.Series([e[:-4] for e in list_forces])

df.to_csv("data/forces.csv")