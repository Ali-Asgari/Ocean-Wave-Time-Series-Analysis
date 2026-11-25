import pandas as pd

def filter_dates(df, start, end):
    if pd.Timestamp(end) <= pd.Timestamp(start):
        raise ValueError('End date must follow start date')
    return df.loc[(df.index >= start) & (df.index < end)].copy()

def load_data(path):
    df = pd.read_csv(path)

    # Remove empty columns created by the CSV header.
    df = df.loc[:, ~df.columns.str.startswith("Unnamed:")]
    
    # Convert the DATE column
    df["DATE"] = pd.to_datetime(
        df["DATE"],
        format="%m/%d/%Y %H:%M"
    )

    # Use DATE as the index
    df = df.set_index("DATE").sort_index()

    return df

def main():
    # Load dataset
    # df = pd.read_csv("c44137.csv")
    df = load_data("c44137.csv")

    # Select a period 
    df = filter_dates(df, '1990-01-01', '2023-01-01')

    print('Rows:', len(df))
    print('Dates:', df.index.min(), 'to', df.index.max())
    print('Columns:', df.columns.tolist())

    # 0    Blank - No quality control (QC) has been performed
    # 1    Good - QC has been performed: record appears correct
    # 3    Doubtful - QC has been performed: record appears doubtful
    # 4    Erroneous - QC has been performed: record appears erroneous
    # 5    Changes - The record has been changed as a result of QC
    # 6    Acceptable - QC has been performed: record seems inconsistent with other records
    # 7    Off Position - There is a problem with the buoy position or mooring. Data may still be useful.
    # 8    Reserved
    # 9    Reserved - indicates missing elements
    print('Flags:', df['Q_FLAG'].value_counts(dropna=False).to_dict())


    #VCAR: Characteristic significant wave height (calculated by MEDS) (m)
    #SSTP: Sea surface temperature (°C) 
    #WSPD: Horizontal wind speed (m/s)
    print(df[['VCAR', 'SSTP', 'WSPD']].describe())



if __name__ == '__main__':
    main()