import pandas as pd


# Load dataset
df = pd.read_csv("c44137.csv")

print ("Head:\n", df.head())

print ("-"*30)
print ("Info:")
df.info()