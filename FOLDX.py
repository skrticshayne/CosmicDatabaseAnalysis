#FOLDX
#Author Shayne Skrtic 
#Co Author Chat gpt 
import subprocess
import pandas as pd
from tkinter import filedialog, Label, Button, Entry, StringVar
import tkinter as tk
from tkinter import ttk, StringVar
import shutil
import os

def get_desktop_path():
    return os.path.join(os.path.expanduser('~'), 'Desktop')

def run_foldx_command(foldx_path, *args):
    command = [foldx_path] + list(args)
    full_command = ' '.join(command)
    print("Executing command:", full_command)
    print("Current working directory:", os.getcwd())
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        print("Error:", stderr.decode())
    return stdout.decode()

def repair_pdb(pdb_file, foldx_path):
    repair_command = ["--command=RepairPDB", f"--pdb={pdb_file}"]
    return run_foldx_command(foldx_path, *repair_command)

def run_stability(pdb_file, foldx_path, output_tag=""):
    stability_command = ["--command=Stability", f"--pdb={pdb_file}"]
    if output_tag:
        stability_command.append(f"--output-file={output_tag}")
    return run_foldx_command(foldx_path, *stability_command)

def run_build_model(pdb_file, mutant_file, foldx_path, number_of_runs=1, output_tag=""):
    build_command = ["--command=BuildModel", f"--pdb={pdb_file}", f"--mutant-file={mutant_file}", f"--numberOfRuns={number_of_runs}"]
    if output_tag:
        build_command.append(f"--output-file={output_tag}")
    return run_foldx_command(foldx_path, *build_command)

def select_file(file_path_var, file_type):
    full_path = filedialog.askopenfilename(title=f"Select {file_type} File", filetypes=[(f"{file_type} files", f"*.{file_type}")])
    if full_path:
        file_name = os.path.basename(full_path)
        file_path_var.set(file_name)

def normalize_line_endings(filename):
    with open(filename, 'r', newline=None) as file:
        content = file.read()

    # Normalize line endings to Unix style (LF)
    normalized_content = content.replace('\r\n', '\n').replace('\r', '\n')

    with open(filename, 'w', newline='\n') as file:
        file.write(normalized_content)
    print("Line endings normalized for:", filename)

def write_fxout_to_excel(individual_list_path, output_excel_path):
    data = []
    # Process the original file
    original_data = parse_fxout_content('StabilityOutput_ST.fxout', None)
    data.append(original_data + [0.0])  # Delta Delta G is 0 for original structure

    original_delta_g = original_data[2]

    # Determine the number of mutations from individual_list.txt
    with open(individual_list_path, 'r') as mutation_file:
        for i, mutation in enumerate(mutation_file, start=1):
            mutated_fxout_file = f"StabilityOutput_{i}_ST.fxout"
            mutation_name = mutation.strip().split()[0]
            mutated_data = parse_fxout_content(mutated_fxout_file, mutation_name)

            # Calculate Delta Delta G
            delta_delta_g = mutated_data[2] - original_delta_g
            data.append(mutated_data + [delta_delta_g])

    # Create DataFrame and write to Excel
    df = pd.DataFrame(data, columns=['Mutation', 'PDB File', 'Delta G', 'Delta Delta G'])
    df.to_excel(output_excel_path, index=False)

def parse_fxout_content(fxout_file, mutation_name):
    try:
        with open(fxout_file, 'r') as infile:
            for line in infile:
                if '.pdb' in line:
                    elements = line.split('\t')
                    if len(elements) > 1:
                        pdb_name = elements[0].strip()
                        delta_g = float(elements[1].strip())
                        title = mutation_name if mutation_name else "Initial Structure"
                        return [title, pdb_name, delta_g]
    except FileNotFoundError:
        print(f"File not found: {fxout_file}")
        return [mutation_name if mutation_name else "Initial Structure", "N/A", float('nan')]

def run_pipeline(pdb_var):
    desktop_path = get_desktop_path()
    os.chdir(os.path.join(desktop_path, "foldx5"))  # Updated to use get_desktop_path()
    individual_list_path = 'individual_list.txt'
    pdb_path = pdb_var.get()
    foldx_path = os.path.join(desktop_path, "foldx5", "FoldX")

    if not all([individual_list_path, pdb_path, foldx_path]):
        print("Please select all files.")
        return

    # Normalize line endings in the individual list file
    normalize_line_endings(individual_list_path)

    print("First Repair PDB")
    repair_output = repair_pdb(pdb_path, foldx_path)
    print(repair_output)

    repaired_pdb_path = pdb_path.replace('.pdb', '_Repair.pdb')

    print("Second Repair PDB")
    second_repair_output = repair_pdb(repaired_pdb_path, foldx_path)
    print(second_repair_output)

    repaired_pdb_path2 = repaired_pdb_path.replace('.pdb', '_Repair.pdb')

    print("Third Repair PDB")
    third_repair_output = repair_pdb(repaired_pdb_path2, foldx_path)
    print(third_repair_output)

    repaired_pdb_path3 = repaired_pdb_path2.replace('.pdb', '_Repair.pdb')

    print("Fourth Repair PDB")
    fourth_repair_output = repair_pdb(repaired_pdb_path3, foldx_path)
    print(fourth_repair_output)

    repaired_pdb_path4 = repaired_pdb_path3.replace('.pdb', '_Repair.pdb')

    print("Stability Analysis")
    print(run_stability(repaired_pdb_path4, foldx_path, "StabilityOutput"))

    print("BuildModel Analysis")
    build_model_output = run_build_model(repaired_pdb_path4, individual_list_path, foldx_path)
    print(build_model_output)

    # Stability analysis for each mutation
    with open(individual_list_path, 'r') as mutation_file:
        for i, mutation in enumerate(mutation_file, start=1):
            mutated_pdb_path = f"{repaired_pdb_path4.replace('.pdb', '')}_{i}.pdb"
            print(f"Stability Analysis on Mutation {i}")
            stability_output = run_stability(mutated_pdb_path, foldx_path, f"StabilityOutput_{i}")
            print(stability_output)

    # Write fxout file contents to an Excel file
#CHANGE FILEPATH HERE TO NEW COMPUTERS USERNAME (MAC)
    write_fxout_to_excel(individual_list_path, os.path.join(desktop_path, 'fxout_contents.xlsx'))

    # Call to handle files after the pipeline processes are complete
    handle_files()
#CHANGE FILEPATH HERE TO NEW COMPUTERS USERNAME (MAC)
def handle_files():
    desktop_path = get_desktop_path()
    source_dir = os.path.join(desktop_path, "foldx5")
    dest_dir = os.path.join(desktop_path, "FoldX output Files")
    exclude_file = os.path.join(source_dir, "FoldX")
    additional_file = os.path.join(desktop_path, "fxout_contents.xlsx")

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # List all files in the source directory
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        # Check if it's not the file to exclude and it's not a directory
        if file_path != exclude_file and os.path.isfile(file_path):
            # Move the file
            new_path = shutil.move(file_path, os.path.join(dest_dir, filename))

            # Delete the file if it starts with "WT_" or is a .fxout file
            if filename.startswith("WT_") or filename.endswith(".fxout"):
                os.remove(new_path)

    # Move the additional file
    if os.path.exists(additional_file):
        shutil.move(additional_file, os.path.join(dest_dir, os.path.basename(additional_file)))

    print("Files processed successfully.")

def open_foldx_gui():
    foldx_root = tk.Toplevel()
    foldx_root.title("FoldX Operations GUI")

    frame = tk.Frame(foldx_root, padx=20, pady=20)
    frame.pack(expand=True)

    pdb_var = StringVar()
    pdb_label = tk.Label(frame, text="Select PDB File:")
    pdb_label.pack()

    pdb_entry = ttk.Entry(frame, textvariable=pdb_var, width=50)
    pdb_entry.pack()

    browse_button = ttk.Button(frame, text="Browse", command=lambda: select_file(pdb_var, 'pdb'))
    browse_button.pack()

    run_button = ttk.Button(frame, text="Run FoldX", command=lambda: run_pipeline(pdb_var))
    run_button.pack()

    foldx_root.mainloop()