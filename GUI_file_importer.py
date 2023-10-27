import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os

selected_files = {}
geology_data = None

def browse_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")])
    if file_paths:
        for file_path in file_paths:
            selected_files[file_path] = os.path.splitext(os.path.basename(file_path))[0]
            update_file_listbox()

def update_file_listbox():
    file_list.delete(0, tk.END)  # Clear the listbox
    for file_name in selected_files.values():
        file_list.insert(tk.END, file_name)

def import_files_to_dataframe():
    for file_path, file_name in selected_files.items():
        try:
            df = pd.read_csv(file_path)
            global collar_data, survey_data, sample_data, geology_data
            if 'geology' in file_name.lower():
                global geology_data
                geology_data = df
                df_name = 'geology_data'
                geology_data = pd.read_csv(file_path, skiprows=15)  # Drop the first 15 rows
                print(df_name)
                print(geology_data)  # Print the modified geology dataframe
            else:
                # Apply naming rules for other CSV files here
                # For example, if 'survey' is in the file name, set DataFrame name to 'survey_data'
                if 'survey' in file_name.lower():
                    df_name = 'survey_data'
                    survey_data = df.copy()
                elif 'sample' in file_name.lower():
                    df_name = 'sample_data'
                    sample_data = df.copy()
                elif 'collar' in file_name.lower():
                    df_name = 'collar_data'
                    collar_data = df.copy()
                else:
                    df_name = file_name
                
                print(df_name)
                print(df)  # Print the other dataframes

        except Exception as e:
            print(f"Error importing '{file_name}': {str(e)}")



def main():
    root = tk.Tk()
    root.title("CSV File Reader")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(frame, text="Select CSV files:")
    label.pack(pady=10)

    global file_list
    file_list = tk.Listbox(frame, selectmode=tk.SINGLE, width=40, height=5)
    file_list.pack(pady=10)

    browse_button = tk.Button(frame, text="Browse", command=browse_files)
    browse_button.pack()

    import_button = tk.Button(frame, text="Import CSV Files", command=import_files_to_dataframe)
    import_button.pack()

    root.mainloop()
    return collar_data, survey_data, sample_data, geology_data

if __name__ == "__main__":
    main()
