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
    # Columns = ['STN_ID', 'Q_FLAG', 'LATITUDE', 'LONGITUDE', 'DEPTH', 'VCAR',
    #             'VTPK', 'VWH$', 'VCMX', 'VTP$', 'WDIR', 'WSPD', 'WSS$',
    #             'GSPD', 'WDIR.1', 'WSPD.1', 'WSS$.1', 'GSPD.1', 'ATMS',
    #             'ATMS.1', 'DRYT', 'SSTP']
    
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

    
    print("\nLargest wave-height measurements:")
    print(
        df.nlargest(10, "VCAR")[["VCAR", "VWH$", "Q_FLAG"]]
    )

    print("\nLowest sea temperatures:")
    print(df.nsmallest(10, "SSTP")[["SSTP", "Q_FLAG"]])

    print("\nHighest sea temperatures:")
    print(df.nlargest(10, "SSTP")[["SSTP", "Q_FLAG"]])


    print("\nLowest wind speeds:")
    print(df.nsmallest(10, "WSPD")[["WSPD", "WSPD.1", "Q_FLAG"]])

    print("\nHighest wind speeds:")
    print(df.nlargest(10, "WSPD")[["WSPD", "WSPD.1", "Q_FLAG"]])

    print("\nMissing wind-speed measurements:")
    print(df[["WSPD", "WSPD.1"]].isna().sum())

    # Count missing measurements
    print("\nMissing measurements:")
    print(df[["VCAR", "SSTP", "WSPD"]].isna().sum())

    flag_1_df = df.loc[df["Q_FLAG"] == 1]

    print("\nLargest wave heights with Q_FLAG = 1:")
    print(flag_1_df.nlargest(10, "VCAR")[["VCAR", "VWH$", "Q_FLAG"]])

    print("\nLowest temperatures with Q_FLAG = 1:")
    print(flag_1_df.nsmallest(10, "SSTP")[["SSTP", "Q_FLAG"]])


    coverage = pd.DataFrame({
        "all_records": df.groupby(df.index.year).size(),
        "flag_1_records": flag_1_df.groupby(flag_1_df.index.year).size()
    }).fillna(0).astype(int)
    print("\nYearly record counts before and after flag-1 filtering:")
    print(coverage)


    flag_counts = pd.crosstab(df.index.year, df["Q_FLAG"])

    print("\nQuality flags by year:")
    print(flag_counts)

    # Compare the two wave-height columns.
    print("\nWave-height summary:")
    print(df[["VCAR", "VWH$"]].describe())

    print("\nLargest buoy-reported wave heights:")
    print(
        df.nlargest(10, "VWH$")[["VCAR", "VWH$", "Q_FLAG"]]
    )

    print("\nSmallest buoy-reported wave heights:")
    print(
        df.nsmallest(10, "VWH$")[["VCAR", "VWH$", "Q_FLAG"]]
    )

    # Check availability and range of buoy-reported heights by year.
    yearly_wave = df.groupby(df.index.year)["VWH$"].agg(
        ["size", "count", "min", "max"]
    )
    yearly_wave["missing"] = (
        yearly_wave["size"] - yearly_wave["count"]
    )

    print("\nBuoy-reported wave heights by year:")
    print(yearly_wave.to_string())

if __name__ == '__main__':
    main()