import pandas as pd

def compareOutputs(df1, df2):
    # Merge the two DataFrames on 'Event ID'
    merged_df = pd.merge(df1, df2, on='Event ID', suffixes=('_df1', '_df2'))

    # Calculate the absolute difference in 'Totals' and add it as a new column
    merged_df['Totals Difference'] = (merged_df['Totals_df1'] - merged_df['Totals_df2']).abs()

    # Filter rows where the difference in 'Totals' is 15 or more
    significant_diffs = merged_df[merged_df['Totals Difference'] >= 15]

    # Check if there are any significant differences
    if significant_diffs.empty:
        print("No significant differences in Totals found.")
        return False, None  # Return False indicating no significant differences, and None for the DataFrame
    else:
        # If significant differences were found, print them and return True and the DataFrame
        print(significant_diffs[['Event ID', 'Totals_df1', 'Totals_df2', 'Totals Difference']])
        return True, significant_diffs[['Event ID', 'Totals_df1', 'Totals_df2', 'Totals Difference']]

if __name__ == '__main__':
    data1 = {
        'Event ID': ['a58faa4e75b965d50446c73bbeef1d82', '39fe52ee8c209de2fc87fc0f692e6094'],
        'Home Team': ['Detroit Pistons', 'Cleveland Cavaliers'],
        'Away Team': ['Charlotte Hornets', 'Phoenix Suns'],
        'Bookmaker Title': ['DraftKings', 'DraftKings'],
        'Totals': [217.0, 220.5]
    }

    data2 = {
        'Event ID': ['a58faa4e75b965d50446c73bbeef1d82', '39fe52ee8c209de2fc87fc0f692e6094'],
        'Home Team': ['Detroit Pistons', 'Cleveland Cavaliers'],
        'Away Team': ['Charlotte Hornets', 'Phoenix Suns'],
        'Bookmaker Title': ['DraftKings', 'DraftKings'],
        'Totals': [232.0, 205.5]  # Changed totals to illustrate the difference
    }

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    has_diff, difference = compareOutputs(df1, df2)
    if has_diff:
        print(difference)













