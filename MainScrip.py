#Author Shayne Skrtic
import tkinter as tk
from tkinter import ttk  # Themed Tkinter
import Cosmic_Parse as Cosmic
import CRAVAT_Parse as Cravat
import R_SCRIPT as RScrip
import FOLDX as FX


# Create the main window
root = tk.Tk()
root.title("COSMIC BioInformatics Pipeline")
root.geometry("400x300")  # Width x Height
root.configure(bg="#333333")  # Background color

# Styling
style = ttk.Style()
style.theme_use('classic')  # 'clam', 'alt', 'default', 'classic' are some themes

style.configure('TButton', font=('Arial', 12, 'bold'), borderwidth='4')
style.map('TButton', foreground=[('!active', 'black'), ('active', 'white')],
          background=[('!active', 'white'), ('active', '#4a7abc')])

# Create and place buttons
button1 = ttk.Button(root, text="COSMIC Parsing", command=Cosmic.create_gui)
button1.pack(pady=10, padx=20, fill=tk.X)

button2 = ttk.Button(root, text="Cravat Output--> Loliplot2 and FoldX Input", command=Cravat.main)
button2.pack(pady=10, padx=20, fill=tk.X)

button3 = ttk.Button(root, text="Chi-Square", command=RScrip.create_gui)
button3.pack(pady=10, padx=20, fill=tk.X)

button4 = ttk.Button(root, text="FoldX", command=FX.open_foldx_gui)
button4.pack(pady=10, padx=20, fill=tk.X)

quit_button = ttk.Button(root, text="Quit", command=root.destroy)
quit_button.pack(pady=10, padx=20, fill=tk.X)

# Start the GUI event loop
root.mainloop()