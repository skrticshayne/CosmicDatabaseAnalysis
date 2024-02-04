#Cosmic_Parse
#Author @Shayne Skrtic 
#Co-Author @ Chat-gpt 
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import sys

# Define the decade ranges
decade_ranges = [
    (0, 10),
    (11, 20),
    (21, 30),
    (31, 40),
    (41, 50),
    (51, 60),
    (61, 70),
    (71, 80),
    (81, 90),
    (91, 100)
]

# Function to open a file dialog for selecting an Excel file and processing it
def browse_and_process_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xlsm")])
    if file_path:
        folder_path = create_result_folder()  # Create a folder for results
        # Convert the Excel file to CSV
        csv_file_path = convert_excel_to_csv(file_path, folder_path)
        if csv_file_path:
            CodingNonCodingFrequency(csv_file_path, folder_path)
            Mut_Type_Frequency(csv_file_path, folder_path)
            Primary_Histology_Frequency(csv_file_path, folder_path)
            Primary_Site_Frequency(csv_file_path, folder_path)
            process_csv_for_Cravat(csv_file_path, folder_path)
            process_csv_for_Loliplot(csv_file_path, folder_path)
            create_txt_file(folder_path)

# Function to create a folder for results on the desktop
def create_result_folder():
# Changed to use get_desktop_path()
    desktop_path = get_desktop_path()
    folder_path = os.path.join(desktop_path, "Cosmic Parsing Results")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def get_desktop_path():
    return os.path.join(os.path.expanduser('~'), 'Desktop')

# Function to convert an Excel file to CSV
def convert_excel_to_csv(excel_file, folder_path):
    try:
        df = pd.read_excel(excel_file)  # Read the Excel file
        # Generate a CSV file path in the results folder
        csv_file_path = os.path.join(folder_path, "Excel_to_CSV.csv")
        df.to_csv(csv_file_path, index=False, encoding='utf-8')  # Save as CSV
        return csv_file_path
    except Exception as e:
        print("Error converting Excel to CSV:", str(e))
        return None

# Function to create a text file with "hi" on the desktop
def create_txt_file(folder_path):
    txt_path = os.path.join(folder_path, "Important_Parsing_Info.txt")
    with open(txt_path, "w") as hi_file:
        hi_file.write("""
Your Data Is now Parsed

Coding_noncoding_Results may be copied and pasted into graph pad for Graph making
*Note this Program Drops Duplicate Identical Mutations from Coding/Noncoding Counts*
*This is done so that a "more common" Mutation does not skew data
######################
Primary_Histology_Results may also be copied and pasted into Graph pad
######################
Primary_Site_Results may also be copied and pasted into Graph pad
######################
Mutation_Description_Counts may also be copied and pasted into Graph pad
######################
Excel_to_Tsv is the Original COSMIC File now in CSV form This may be ignored if not needed
######################
Dropped Cravat Data.txt holds important information about dropped mutations.
This shows how many Deletions, Indels, And Duplications were dropped from the dataset
As we do not Need these for our purposes
######################
CRAVAT_data.tsv is the file you will need to run your Cravat analysis Here are the steps to doing that

1) Navigate to https://run.opencravat.org/submit/nocache/index.html

2)in the top left select hg38/GRCh38 under Genome:

3)Press add Input Files and input CRAVAT_data.tsv
this is found within the folder Cosmic Parsing Results folder on your desktop

4)Select Show all Categories

5)Select FATHMM MKL, VEST4, and CHASMplus

6)Press annotate and wait for CRAVAT to finish running

7)Select opem Results viewer
######################
Loliplot_data.tsv is the file you will need to create your initial Loliplot
*Note you will need to make another from Significant CRAVAT mutations this is the first one with all Mutations*

Here are the steps to generating LoliPlot
1) navigate to https://www.cbioportal.org/mutation_mapper

2)press choose File and select Loliplot_data.tsv
his is found within the folder Cosmic Parsing Results folder on your desktop

3)Press Visualize

4)Download Image
######################
If your computer has issues opening the CSV files (Old Windows Machines)
Navigate to this website to turn them into excel sheets
https://cloudconvert.com/

Author of Code @Shayne Skrtic
if code is giving errors or bad data shoot me an email skrtics@xavier.edu

""")

# Function to process the data
def process_csv_for_Loliplot(file_path, folder_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Check if the "AGE" column exists in the DataFrame
    if ' AGE' in df.columns:
        # Drop rows where the "AGE" column is null
        df.dropna(subset=[' AGE'], inplace=True)
        if ' MUTATION_DESCRIPTION' in df.columns:
            # Drop rows with values other than 'Substitution - Missense' in the "MUTATION_DESCRIPTION" column
            original_row_count = len(df)
            df = df[df[' MUTATION_DESCRIPTION'] == 'Substitution - Missense']

            # Check if the "HGVSG" column exists in the DataFrame
            if ' HGVSG' in df.columns:
                # Split the "HGVSG" column into three parts and create new columns
                df[['chromosome', 'Start_position', 'Reference_Allele']] = df[' HGVSG'].str.extract(r'(\d+):g\.(\d+)([A-Z])>', expand=True)

                # Extract the characters after the ">" symbol and create a new column
                df['Variant_Allele'] = df[' HGVSG'].str.extract(r'>([A-Z])', expand=False)

                # Add a new column with the same data as 'Start_position'
                df['End_Position'] = df['Start_position']

                # Reorder the columns with 'AfterG' as the last column
                df = df[['chromosome', 'Start_position', 'End_Position', 'Reference_Allele', 'Variant_Allele']]

                # Drop blank rows at the end of the DataFrame
                df.dropna(how='all', inplace=True)

                # Save the DataFrame to a TSV file in the results folder
                output_file_path = os.path.join(folder_path, "Loliplot_data.tsv")
                df.to_csv(output_file_path, sep='\t', index=False)
        else:
            print("The 'HGVSG' column does not exist in the selected CSV file.")
    else:
        print("The 'AGE' column does not exist in the selected CSV file.")

def process_csv_for_Cravat(file_path, folder_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Check if the "AGE" column exists in the DataFrame
    if ' AGE' in df.columns:
        # Drop rows where the "AGE" column is null
        original_row_count = len(df)
        df.dropna(subset=[' AGE'], inplace=True)

        # Check if the "MUTATION_DESCRIPTION" column exists in the DataFrame
        if ' MUTATION_DESCRIPTION' in df.columns:
            # Drop rows with values other than 'Substitution - Missense' in the "MUTATION_DESCRIPTION" column
            original_row_count = len(df)
            df = df[df[' MUTATION_DESCRIPTION'] == 'Substitution - Missense']

            # Check if the "HGVSG" column exists in the DataFrame
            if ' HGVSG' in df.columns:
                # Split the "HGVSG" column into three parts and create new columns
                df[['chrom', 'pos', 'ref_base']] = df[' HGVSG'].str.extract(r'(\d+):g\.(\d+)([A-Z])>', expand=True)

                # Extract the characters after the ">" symbol and create a new column
                df['alt_base'] = df[' HGVSG'].str.extract(r'>([A-Z])', expand=False)

                # Reorder the columns with 'AfterG' as the last column
                df = df[['chrom', 'pos', 'ref_base', 'alt_base']]

                # Drop blank rows at the end of the DataFrame
                original_row_count = len(df)
                df.dropna(how='all', inplace=True)
                rows_dropped = original_row_count - len(df)

                # Remove duplicates from the "chrom" column
                df.drop_duplicates(subset=['pos'], keep='first', inplace=True)

                # Save the DataFrame to a TSV file in the results folder
                output_file_path = os.path.join(folder_path, "CRAVAT_data.tsv")
                df.to_csv(output_file_path, sep='\t', index=False)

            
            else:
                print("The 'HGVSG' column does not exist in the selected CSV file.")
        else:
            print("The 'MUTATION_DESCRIPTION' column does not exist in the selected CSV file.")
    else:
        print("The 'AGE' column does not exist in the selected CSV file.")
        
def CodingNonCodingFrequency(file_path, folder_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Remove rows where the 'AGE' column is empty
    df.dropna(subset=[' AGE'], inplace=True)

    # Check for and remove duplicate values in the 'HGVSG' column, keeping only one of each unique value
    df.drop_duplicates(subset=[' HGVSG'], keep='first', inplace=True)

    Total = len(df)

    # Drop all rows that contain 'p.?'
    df = df[~(df[' MUTATION_AA'] == 'p.?')]

    # Select the columns you want to keep (replace 'column1' and 'column2' with your column names)
    Age_Sort_selected_columns_Only_Coding = df[[' AGE', ' MUTATION_AA']]

    Coding = len(Age_Sort_selected_columns_Only_Coding)

    NonCoding = Total - Coding

    # Save the results to a CSV file in the results folder
    result_df = pd.DataFrame({
        'Total Mutations': [Total],
        'Coding Mutations': [Coding],
        'NonCoding Mutations': [NonCoding]
    })

    # Define the path to save the CSV file in the results folder
    csv_file_path = os.path.join(folder_path, "coding_noncoding_results.csv")

    result_df.to_csv(csv_file_path, index=False)

def Mut_Type_Frequency(file_path, folder_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Remove rows where the 'AGE' column is null
    df.dropna(subset=[' AGE'], inplace=True)

    # Drop rows with 'p.?' in 'MUTATION_AA'
    df = df[~(df[' MUTATION_AA'] == 'p.?')]

    # Create a list of unique values in 'MUTATION_DESCRIPTION' along with their counts
    mutation_description_counts = df[' MUTATION_DESCRIPTION'].value_counts()

    # Save the mutation description counts to a CSV file in the results folder
    mutation_description_counts.to_csv(os.path.join(folder_path, "Mutation_Description_Counts.csv"))

def Primary_Histology_Frequency(file_path, folder_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Remove rows where the 'AGE' column is null
    df.dropna(subset=[' AGE'], inplace=True)

    # Create a new column 'Decade' based on the 'AGE' values
    df['Decade'] = df[' AGE'].apply(assign_decade)

    # Ensure all decades are included and in the desired order
    all_decades = [f"{start}-{end}" for start, end in decade_ranges]
    histology_counts = df.groupby(['Decade', ' PRIMARY_HISTOLOGY']).size().unstack(fill_value=0).T

    # Add columns for missing decades with zeros
    for decade in all_decades:
        if decade not in histology_counts.columns:
            histology_counts[decade] = 0

    # Reorder columns to match the desired order
    histology_counts = histology_counts[all_decades]

    # Sort rows by the sum of values in ascending order
    histology_counts = histology_counts.loc[histology_counts.sum(axis=1).sort_values().index]

    # Save the results to a CSV file in the results folder
    histology_counts.to_csv(os.path.join(folder_path, "primary_histology_results.csv"))

def Primary_Site_Frequency(file_path, folder_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Remove rows where the 'AGE' column is null
    df.dropna(subset=[' AGE'], inplace=True)

    # Create a new column 'Decade' based on the 'AGE' values
    df['Decade'] = df[' AGE'].apply(assign_decade)

    # Ensure all decades are included and in the desired order
    all_decades = [f"{start}-{end}" for start, end in decade_ranges]
    site_counts = df.groupby(['Decade', ' PRIMARY_SITE']).size().unstack(fill_value=0).T

    # Add columns for missing decades with zeros
    for decade in all_decades:
        if decade not in site_counts.columns:
            site_counts[decade] = 0

    # Reorder columns to match the desired order
    site_counts = site_counts[all_decades]

    # Sort rows by the sum of values in ascending order
    site_counts = site_counts.loc[site_counts.sum(axis=1).sort_values().index]

    # Save the results to a CSV file in the results folder
    site_counts.to_csv(os.path.join(folder_path, "primary_site_results.csv"))

def assign_decade(age):
    for start, end in decade_ranges:
        if start <= age <= end:
            return f"{start}-{end}"
    return "Unknown"
def create_gui():
    root = tk.Tk()
    root.title("Cosmic Data Analysis")

    # Create a frame to contain the label and button
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)

    # Set a blue theme
    root.configure(bg='light blue')
    frame.configure(bg='light blue')

    # Create a label for instructions with black text
    label = tk.Label(frame, text="Select an Excel file for analysis:", bg='light blue', fg='black')
    label.pack()
    
    # Create a button to browse and select the Excel file with black text
    browse_button = ttk.Button(frame, text="Select Excel File", command=browse_and_process_excel)
    browse_button.pack(pady=10)

    # Create an exit button
    exit_button = ttk.Button(frame, text="Exit", command=root.destroy)
    exit_button.pack(pady=10)

    # Center the window on the screen
    window_width = 400
    window_height = 200  # Adjusted height to accommodate exit button
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.mainloop()
if __name__ == "__main__":
    create_gui()