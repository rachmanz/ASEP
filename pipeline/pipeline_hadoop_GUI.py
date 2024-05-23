import tkinter as tk
from tkinter import filedialog
from hdfs import InsecureClient
import pandas as pd
import os

def show_dataset():
    filename = filedialog.askopenfilename()
    if not filename:
        return  # User canceled file selection
    # Read the file content and display in the text widget
    df = pd.read_csv(filename)  # Assuming CSV file, modify as needed
    dataset_text.delete(1.0, tk.END)  # Clear previous content
    dataset_text.insert(tk.END, df.to_string())

def upload_to_hadoop():
    filename = filedialog.askopenfilename()
    if not filename:
        return  # User canceled file selection
    # Connect to Hadoop HDFS
    client = InsecureClient('http://hadoop-master:50070', user='hadoop')
    # Determine the destination path in Hadoop
    destination_path = "/home/miroslav/hasil_data" + os.path.basename(filename)
    # Upload file to Hadoop HDFS
    with open(filename, 'rb') as f:
        client.write(destination_path, f)
    print(f"File '{filename}' uploaded to Hadoop HDFS at '{destination_path}'")

# Create GUI
root = tk.Tk()
root.title("Hadoop File Upload")
root.geometry("800x400")

# Panel to display dataset content
dataset_panel = tk.Frame(root)
dataset_panel.pack(fill=tk.BOTH, expand=True)
dataset_label = tk.Label(dataset_panel, text="Dataset Content:")
dataset_label.pack()
dataset_text = tk.Text(dataset_panel, wrap=tk.WORD)
dataset_text.pack(fill=tk.BOTH, expand=True)

show_dataset_button = tk.Button(root, text="Select File and Show Dataset", command=show_dataset)
show_dataset_button.pack(pady=10)

upload_button = tk.Button(root, text="Upload File to Hadoop", command=upload_to_hadoop)
upload_button.pack(pady=10)

root.mainloop()