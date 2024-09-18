import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox


def generate_insert_statements(table_name, file_paths):
    insert_statements = []

    for file_path in file_paths:
        if file_path.endswith('.csv'):
            # Try different encodings for Arabic support
            encodings = ['utf-8', 'windows-1256', 'ISO-8859-1']
            df = None

            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break  # Exit loop if successful
                except (UnicodeDecodeError, pd.errors.ParserError):
                    continue  # Try next encoding

            if df is None:
                messagebox.showerror("Error", f"Failed to read file: {file_path}.")
                continue

        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            continue

        # Ensure all column names are strings
        df.columns = [str(col) for col in df.columns]

        for index, row in df.iterrows():
            columns = ', '.join(df.columns)
            values = ', '.join(f"'{str(value).replace("'", "''")}'" for value in row)
            insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
            insert_statements.append(insert_statement)

    return insert_statements


def upload_files():
    file_paths = filedialog.askopenfilenames(
        title="Select files",
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
    )

    if not file_paths:
        messagebox.showwarning("No Selection", "No files selected.")
        return

    table_name = table_name_entry.get()
    if not table_name:
        messagebox.showwarning("No Table Name", "Please enter a table name.")
        return

    insert_statements = generate_insert_statements(table_name, file_paths)

    # Displaying insert statements
    output_text.delete(1.0, tk.END)  # Clear previous text
    for stmt in insert_statements:
        output_text.insert(tk.END, stmt + "\n")


# Create the main window
root = tk.Tk()
root.title("SQL Insert Statement Generator")

# Table name input
tk.Label(root, text="Table Name:").pack(pady=5)
table_name_entry = tk.Entry(root, width=30)
table_name_entry.pack(pady=5)

# Upload button
upload_button = tk.Button(root, text="Upload Files", command=upload_files)
upload_button.pack(pady=20)

# Text area for output
output_text = tk.Text(root, wrap=tk.WORD, width=200, height=20)
output_text.pack(pady=10)

# Start the GUI event loop
root.mainloop()
