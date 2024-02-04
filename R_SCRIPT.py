#R_SCRIPT
#Author Shayne Skrtic 
import tkinter as tk
from tkinter import ttk, messagebox
import rpy2.robjects as robjects
import os

def run_r_script(entry):
    # Fetching user input
    try:
        values = list(map(int, entry.get().split(',')))
        if len(values) != 4:
            raise ValueError("Please enter exactly 4 numbers separated by commas")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return

    # Running the R script
    try:
        robjects.r('''
            library(RVAideMemoire)
            run_chi_square <- function(values) {
                data <- matrix(values, nrow=2, byrow=TRUE)
                rownames(data) <- c("Conserved", "Non-Conserved")
                colnames(data) <- c("Disruptive", "Non-Disruptive")
                chi2 <- chisq.test(data)
                fdr <- chisq.multcomp(data, p.method = 'fdr')
                list(chi2=chi2, fdr=fdr)
            }
        ''')
        result = robjects.r['run_chi_square'](robjects.IntVector(values))
        chi2, fdr = result[0], result[1]

        # Write results to a file on the desktop (for Mac)
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        file_path = os.path.join(desktop_path, 'Chi-square_results.txt')
        with open(file_path, 'w') as file:
            file.write(f"Chi-square Test:\n{chi2}\n\nFDR:\n{fdr}")
        messagebox.showinfo("Success", "Results saved to 'Chi-square_results.txt' on your desktop.")
    except Exception as e:
        messagebox.showerror("R Script Error", str(e))

def create_gui():
    # Create the R script GUI window
    r_script_root = tk.Toplevel()
    r_script_root.title("Cosmic Data Analysis")

    # Create a frame to contain the widgets, with padding
    frame = tk.Frame(r_script_root, padx=20, pady=20)
    frame.pack(expand=True)

    # Set a blue theme
    r_script_root.configure(bg='light blue')
    frame.configure(bg='light blue')

    # Create a multi-line label for instructions
    instructions = ("Enter 4 Numbers (comma-separated):\n"
                    "In this Format:\n"
                    "1. Disruptive/Conserved,\n"
                    "2. Disruptive/Non-Conserved,\n"
                    "3. Non-Disruptive/Conserved,\n"
                    "4. Non-Disruptive/Non-Conserved")
    instruction_label = tk.Label(frame, text=instructions, bg='light blue', fg='black', justify=tk.LEFT)
    instruction_label.pack(pady=(20, 5))

    # Create entry widget
    entry = ttk.Entry(frame)
    entry.pack(pady=(0, 20))

    # Create button to run R script
    run_button = ttk.Button(frame, text="Run R Script", command=lambda: run_r_script(entry))
    run_button.pack(pady=10)

    # Quit button
    quit_button = ttk.Button(frame, text="Quit", command=r_script_root.destroy)
    quit_button.pack(pady=10)

    # Center the window on the screen
    window_width = 400
    window_height = 400  # Adjusted for additional content
    screen_width = r_script_root.winfo_screenwidth()
    screen_height = r_script_root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    r_script_root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Assuming this is part of a larger script where `root` is your main Tk window
# If this script is standalone, you need to create a root window for the main GUI
# root = tk.Tk()
# Setup for the main GUI window, including a button to open the R script GUI
# open_r_button = ttk.Button(root, text="Open R Script GUI", command=open_r_script_gui)
# open_r_button.pack(pady=10, padx=20, fill=tk.X)

# Start the main event loop
# root.mainloop()
