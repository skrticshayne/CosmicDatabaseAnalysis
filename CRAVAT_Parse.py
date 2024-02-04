#CRAVAT_Parse
#Author Shayne Skrtic
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv

# Function to convert three-letter amino acids to one-letter codes
def three_to_one_letter_aa(three_letter_code):
    aa_dict = {
        'Cys': 'C', 'Asp': 'D', 'Ser': 'S', 'Gln': 'Q', 'Lys': 'K',
        'Ile': 'I', 'Pro': 'P', 'Thr': 'T', 'Phe': 'F', 'Asn': 'N',
        'Gly': 'G', 'His': 'H', 'Leu': 'L', 'Arg': 'R', 'Trp': 'W',
        'Ala': 'A', 'Val': 'V', 'Glu': 'E', 'Tyr': 'Y', 'Met': 'M'
    }
    return aa_dict.get(three_letter_code, '')

# Function to convert protein change format
def convert_protein_change_format(protein_change):
    original_aa = three_to_one_letter_aa(protein_change[2:5])
    position = protein_change[5:-3]
    mutated_aa = three_to_one_letter_aa(protein_change[-3:])
    return f"{original_aa}A{position}{mutated_aa};"

# Extract significant positions
def extract_significant_positions(filename):
    significant_positions = []
    with open(filename, 'r') as file:
        for _ in range(6):
            file.readline()
        headers = file.readline().strip().split('\t')
        chasm_pvalue_idx = headers.index("P-value")
        vest_pvalue_idx = headers.index("P-value", chasm_pvalue_idx + 1)
        pos_idx = headers.index("Pos")
        for line in file:
            columns = line.strip().split('\t')
            try:
                chasm_pvalue = float(columns[chasm_pvalue_idx])
                vest_pvalue = float(columns[vest_pvalue_idx])
            except ValueError:
                continue
            if chasm_pvalue < 0.05 or vest_pvalue < 0.05:
                significant_positions.append(columns[pos_idx])
    return significant_positions

# Extract and format significant mutations
def extract_significant_mutations(filename):
    formatted_changes = []
    with open(filename, 'r') as file:
        for _ in range(6):
            file.readline()
        headers = file.readline().strip().split('\t')
        chasm_pvalue_idx = headers.index("P-value")
        vest_pvalue_idx = headers.index("P-value", chasm_pvalue_idx + 1)
        protein_change_idx = headers.index("Protein_Change")
        for line in file:
            columns = line.strip().split('\t')
            try:
                chasm_pvalue = float(columns[chasm_pvalue_idx])
                vest_pvalue = float(columns[vest_pvalue_idx])
            except ValueError:
                continue
            if chasm_pvalue < 0.05 or vest_pvalue < 0.05:
                formatted_changes.append(convert_protein_change_format(columns[protein_change_idx]))
    return formatted_changes

# Write to TSV function
def write_tsv(data, desktop_path, output_file):
    with open(os.path.join(desktop_path, output_file), 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        for row in data:
            writer.writerow(row)

# Process files for matched rows
def process_files(key_list, tsv_file, desktop_path):
    matched_rows = []
    with open(tsv_file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        headers = next(reader)
        matched_rows.append(headers)
        for row in reader:
            if row[1] in key_list:
                matched_rows.append(row)
    return matched_rows

# Get desktop path
def get_desktop_path():
    if sys.platform.startswith('win'):
        return os.path.join(os.environ['USERPROFILE'], 'Desktop')
    else:
        return os.path.join(os.path.expanduser('~'), 'Desktop')

# Find the second TSV file
def find_second_tsv_file():
    desktop_path = get_desktop_path()
    cosmic_folder = os.path.join(desktop_path, "Cosmic Parsing Results")
    return os.path.join(cosmic_folder, "Loliplot_data.tsv")

# Main function
def main():
    def create_gui():
        root = tk.Tk()
        root.title("Cravat Analysis")

        # Create a frame to contain the label and button
        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack(expand=True)

        # Set a blue theme
        root.configure(bg='light blue')
        frame.configure(bg='light blue')

        # Create a label for instructions with black text
        label = tk.Label(frame, text="Select Cravat Output:", bg='light blue', fg='black')
        label.pack()

        # Create a button to browse and select the TSV file with black text
        browse_button = ttk.Button(frame, text="Select TSV File", command=process_and_match)
        browse_button.pack(pady=10)

        # Create a quit button
        quit_button = ttk.Button(frame, text="Quit", command=root.destroy)
        quit_button.pack(pady=10)

        # Center the window on the screen
        window_width = 400
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        root.mainloop()

    def process_and_match():
        tsv_file1 = filedialog.askopenfilename(title="Select Cravat Output", filetypes=[("TSV files", "*.tsv"), ("All files", "*.*")])
        if not tsv_file1:
            return

        # Process for significant positions
        significant_positions = extract_significant_positions(tsv_file1)
        desktop_path = get_desktop_path()
        tsv_file2 = find_second_tsv_file()
        if not os.path.exists(tsv_file2):
            messagebox.showerror('Error', 'Loliplot_data.tsv not found in the Cosmic Parsing Results folder on your Desktop.')
            return
        matched_data = process_files(significant_positions, tsv_file2, desktop_path)
        output_file1 = 'Loliplot_#2_Output.tsv'
        write_tsv(matched_data, desktop_path, output_file1)

        # Process for significant mutations
        protein_changes = extract_significant_mutations(tsv_file1)
        output_file2 = os.path.join(desktop_path, "individual_list.txt")
        with open(output_file2, 'w') as output_file:
            for change in protein_changes:
                output_file.write(change + '\n')

        messagebox.showinfo('Success', f'Files have been saved to the Desktop: \n1. {output_file1}\n2. {output_file2}')

    create_gui()

if __name__ == '__main__':
    main()
