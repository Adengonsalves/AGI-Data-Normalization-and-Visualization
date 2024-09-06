import pandas as pd
import matplotlib.pyplot as plt

# Input and output file paths
INFILE = "21zpallagi.csv"
METRO_FILE = "Zip to Metro Data CSV.csv"
OUTFILE = "normalized-agi.csv"

def make_normalized_csv():
    # Read the IRS data and select necessary columns
    df = pd.read_csv(INFILE)
    df_subset = df[["zipcode", "agi_stub", "N1", "A00100"]]

    # Group by zipcode and sum the data to aggregate it
    df_aggregates = df_subset.groupby('zipcode').sum()

    # Calculate the average adjusted gross income (AGI), adjusting for income reported in thousands
    # and preventing division by zero errors
    df_aggregates["avg_agi"] = (df_aggregates.A00100 * 1000) / (1 + df_aggregates.N1)

    # Rename the columns for clarity
    df_aggregates.rename(columns={'N1': 'total_filers', 'A00100': 'total_income'}, inplace=True)

    # Drop unnecessary 'agi_stub' column
    df_aggregates.drop('agi_stub', inplace=True, axis=1)

    # Insert blank columns for city, state, and MSA which will be filled with data from another CSV
    df_aggregates.insert(0, 'city', '')
    df_aggregates.insert(0, 'state', '')
    df_aggregates.insert(0, 'msa', '')

    # Read the Metro Data CSV file with appropriate encoding
    df_msas = pd.read_csv(METRO_FILE, encoding='cp1252')

    # Enrich IRS data with metro data
    for index, row in df_aggregates.iterrows():
        city = state = msa = ""
        try:
            # Lookup and strip city, state, and msa from the Metro Data CSV using the zipcode as key
            city = str(df_msas.loc[df_msas["Zip Code"] == index]["City"].values[0]).strip()
            state = str(df_msas.loc[df_msas["Zip Code"] == index]["State"].values[0]).strip()
            msa = str(df_msas.loc[df_msas["Zip Code"] == index]["Primary CSA Name"].values[0]).strip()
            if msa.lower() == "nan":
                msa = ""
        except:
            # In case of any error (e.g., missing data), leave the values as empty strings
            pass
        # Update the row in the dataframe with city, state, and msa information
        df_aggregates.loc[index] = [msa, state, city, row["total_filers"], row["total_income"], row["avg_agi"]]

    # Output the enriched and aggregated data to a CSV file
    df_aggregates.to_csv(OUTFILE)

# Execute the function to process the data
make_normalized_csv()

agi = pd.read_csv('normalized-agi.csv')

#Sorts by agi higest - lowest
sorted_df = agi.sort_values(by='avg_agi', ascending=False)
#Saves it to new file
sorted_df.to_csv('sorted_file.csv', index=False)
agi = pd.read_csv('sorted_file.csv')

# Extract the first 20 rows for the highest AGI and the last 20 rows for the lowest AGI
top_20_agi = agi.head(20)
bottom_20_agi = agi.tail(20)

# Create X-axis labels containing City, State, and ZIP Code
top_20_labels = [f"{row['city']}, {row['state']} {row['zipcode']}" for index, row in top_20_agi.iterrows()]
bottom_20_labels = [f"{row['city']}, {row['state']} {row['zipcode']}" for index, row in bottom_20_agi.iterrows()]

# Plotting top 20 ZIP Codes by Average AGI
plt.figure(figsize=(8, 8))  # Specify figure size
plt.bar(top_20_labels, top_20_agi['avg_agi'], color='blue')  # Create vertical bar chart
plt.xlabel('City, State ZIP Code)')  # Label for the x-axis
plt.ylabel('Average AGI')  # Label for the y-axis
plt.title('Top 20 AGI ZIP Codes')  # Title of the plot
plt.xticks(rotation=90)  # Rotate X-axis labels vertically for better visibility
plt.tight_layout()  # Adjust layout to ensure labels are not cut off
plt.show()  # Display the first plot

# Plotting bottom 20 ZIP Codes by Average AGI
plt.figure(figsize=(8, 8))  # Specify figure size for a new figure
plt.bar(bottom_20_labels, bottom_20_agi['avg_agi'], color='red')  # Create vertical bar chart
plt.xlabel('City, State ZIP Code')  # Label for the x-axis
plt.ylabel('Average AGI')  # Label for the y-axis
plt.title('Bottom 20 AGI ZIP Codes')  # Title of the plot
plt.xticks(rotation=90)  # Rotate X-axis labels vertically for better visibility
plt.tight_layout()  # Adjust layout to ensure labels are not cut off
plt.show()  # Display the second plot



#MSA GRAPHS
data = pd.read_csv('normalized-agi.csv')

# Group by MSA and sum the total filers and total income
msa_grouped = data.groupby('msa').agg({
    'total_filers': 'sum',
    'total_income': 'sum'
})

# Calculate the average AGI for each MSA
msa_grouped['avg_agi'] = msa_grouped['total_income'] / msa_grouped['total_filers']

# Sort the MSAs by average AGI and separate the top 20 and bottom 20
top_20_msas = msa_grouped.sort_values(by='avg_agi', ascending=False).head(20)
bottom_20_msas = msa_grouped.sort_values(by='avg_agi', ascending=True).head(20)

# Create bar chart for Top 20 MSAs
plt.figure(figsize=(8, 8))
plt.bar(top_20_msas.index, top_20_msas['avg_agi'], color='green')
plt.xlabel('MSA')
plt.ylabel('Average AGI')
plt.title('Top 20 AGI MSAs')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Create bar chart for Bottom 20 MSAs
plt.figure(figsize=(8, 8))
plt.bar(bottom_20_msas.index, bottom_20_msas['avg_agi'], color='red')
plt.xlabel('MSA')
plt.ylabel('Average AGI')
plt.title('Bottom 20 AGI MSAs')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()




