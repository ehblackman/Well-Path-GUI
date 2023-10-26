import tkinter as tk
from tkinter import filedialog
import pandas as pd

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        import_file(file_path)

def import_file(file_path):
    try:
        dataframe = pd.read_csv(file_path)
        print(dataframe)
        root.destroy()  # Close the GUI
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    global root
    root = tk.Tk()
    root.title("CSV File Importer")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(frame, text="Select a CSV file:")
    label.pack(pady=10)

    browse_button = tk.Button(frame, text="Browse", command=browse_file)
    browse_button.pack()

    # Allow horizontal and vertical resizing
    root.resizable(True, True)

    root.mainloop()

if __name__ == "__main__":
    main()
