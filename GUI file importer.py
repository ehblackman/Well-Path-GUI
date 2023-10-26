import tkinter as tk
from tkinter import filedialog
import pandas as pd

selected_files = []

def browse_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")])
    if file_paths:
        for file_path in file_paths:
            selected_files.append(file_path)
            update_file_listbox()

def update_file_listbox():
    file_list.delete(0, tk.END)  # Clear the listbox
    for file_path in selected_files:
        file_list.insert(tk.END, file_path)

def import_files_to_dataframe():
    if not selected_files:
        return  # No files selected

    dataframe_dict = {}  # Create a dictionary to store DataFrames

    for file_path in selected_files:
        try:
            df = pd.read_csv(file_path)
            # Extract the file name without extension as the DataFrame name
            file_name = file_path.split('/')[-1].split('.')[0]
            dataframe_dict[file_name] = df  # Store the DataFrame in the dictionary
        except Exception as e:
            print(f"Error importing '{file_path}': {str(e)}")

    if dataframe_dict:
        # Process the dataframes or access them using their names
        for name, df in dataframe_dict.items():
            print(f"DataFrame Name: {name}")
            print(df)

def main():
    root = tk.Tk()
    root.title("Multiple CSV File Reader")

    # Allow horizontal and vertical resizing
    root.resizable(True, True)

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(frame, text="Select CSV files:")
    label.pack(pady=10)

    global file_list
    file_list = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=40, height=5)
    file_list.pack(pady=10)

    browse_button = tk.Button(frame, text="Browse", command=browse_files)
    browse_button.pack()

    global text_widget
    text_widget = tk.Text(frame)
    text_widget.pack(fill=tk.BOTH, expand=True)

    import_button = tk.Button(frame, text="Import to DataFrame", command=import_files_to_dataframe)
    import_button.pack()

    # Allow horizontal and vertical resizing
    root.resizable(True, True)

    root.mainloop()

if __name__ == "__main__":
    main()
