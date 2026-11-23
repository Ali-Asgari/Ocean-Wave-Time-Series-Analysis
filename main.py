import pandas as pd

def main():
    # Load dataset
    df = pd.read_csv("c44137.csv")

    print ("Head:\n", df.head())

    print ("-"*30)
    print ("Info:")
    df.info()



if __name__ == '__main__':
    main()