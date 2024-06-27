import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
import seaborn as sns
import enrichment as en
import data_prep as dp
# Assume the following functions are defined elsewhere in your project
# from your_module import dp.prepare_data, conduct_enrichment_top_n, plot_enrichment

def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def run_enrichment():
    targetome_file = targetome_entry.get()
    affinity_file = affinity_entry.get()
    n = n_entry.get()
    drug = drug_entry.get()

    # Validate inputs
    if not targetome_file or not affinity_file or not n or not drug:
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    try:
        n = eval(n)  # Converts the string input into an int or list
        if not (isinstance(n, int) or isinstance(n, list)):
            raise ValueError
    except:
        messagebox.showerror("Error", "Invalid input for n. It must be an int or a list of ints.")
        return

    try:
        df = dp.prepare_data(targetome_file, affinity_file)
        if isinstance(n, int):
            df_enriched = en.conduct_enrichment_top_n(df, n)
            en.plot_enrichment(df_enriched, n, drug)
        elif isinstance(n, list):
            for i in n:
                df_enriched = en.conduct_enrichment_top_n(df, i)
                en.plot_enrichment(df_enriched, i, drug)
        messagebox.showinfo("Success", "Enrichment analysis completed.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_gui():
    # Create the GUI window
    root = tk.Tk()
    root.title("Enrichment Analysis")

    # Create and place the input fields
    tk.Label(root, text="Targetome File").grid(row=0, column=0)
    global targetome_entry
    targetome_entry = tk.Entry(root, width=50)
    targetome_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: select_file(targetome_entry)).grid(row=0, column=2)

    tk.Label(root, text="Affinity File").grid(row=1, column=0)
    global affinity_entry
    affinity_entry = tk.Entry(root, width=50)
    affinity_entry.grid(row=1, column=1)
    tk.Button(root, text="Browse", command=lambda: select_file(affinity_entry)).grid(row=1, column=2)

    tk.Label(root, text="n (int or list)").grid(row=2, column=0)
    global n_entry
    n_entry = tk.Entry(root, width=50)
    n_entry.grid(row=2, column=1)

    tk.Label(root, text="Drug Name").grid(row=3, column=0)
    global drug_entry
    drug_entry = tk.Entry(root, width=50)
    drug_entry.grid(row=3, column=1)

    # Create and place the Run button
    tk.Button(root, text="Run Enrichment", command=run_enrichment).grid(row=4, columnspan=3)

    # Run the GUI loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
