import pandas as pd

def filter_dates(df, start, end):
    if pd.Timestamp(end) <= pd.Timestamp(start):
        raise ValueError('End date must follow start date')
    return df.loc[(df.index >= start) & (df.index < end)].copy()

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

    print(filter_dates(df, '1990-01-01', '2023-01-01'))


if __name__ == '__main__':
    main()