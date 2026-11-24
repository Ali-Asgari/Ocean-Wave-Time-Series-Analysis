import pandas as pd

def main():
    # Load dataset
    df = pd.read_csv("c44137.csv")

    # Convert the DATE column.
    df["DATE"] = pd.to_datetime(
        df["DATE"],
        format="%m/%d/%Y %H:%M"
    )

    # Use DATE as the index.
    df = df.set_index("DATE").sort_index()

    print ("Head:\n", df.head())

    print ("-"*30)
    print ("Info:")
    df.info()



if __name__ == '__main__':
    main()