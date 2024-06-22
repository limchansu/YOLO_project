# counter_ui.py

import tkinter as tk
from tkinter import messagebox
from counter import Counter

class CounterUI:
    def __init__(self, root, counter):
        self.counter = counter
        self.root = root
        self.root.title("Counter")

        self.create_widgets()
        self.configure_grid()

    def create_widgets(self):
        row = 0
        tk.Button(self.root, text="Display Payment Records", command=self.display_payment_records).grid(row=row, columnspan=2, sticky="nsew")
        row += 1
        tk.Button(self.root, text="Check Mismatched Times", command=self.check_mismatched_times).grid(row=row, columnspan=2, sticky="nsew")

    def configure_grid(self):
        for i in range(2):  # Adjust the number based on the number of rows
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(2):  # Adjust the number based on the number of columns
            self.root.grid_columnconfigure(i, weight=1)

        self.root.geometry("400x200")  # Set initial size of the window
        self.root.minsize(300, 150)    # Set minimum size of the window

    def display_payment_records(self):
        records_text = self.counter.display_payment_records()
        if records_text:
            messagebox.showinfo("Payment Records", records_text)
        else:
            messagebox.showinfo("Payment Records", "No payment records found.")
    
    def check_mismatched_times(self):
        mismatched = self.counter.list_mismatched_times()
        if mismatched:
            records_text = ""
            for start_time, end_time in mismatched:
                records_text += f"Start: {start_time}, End: {end_time}\n"
            messagebox.showwarning("Mismatched Times", records_text)
        else:
            messagebox.showinfo("Mismatched Times", "All payment times match with CCTV records.")

def main():
    counter = Counter()
    root = tk.Tk()
    app = CounterUI(root, counter)
    root.mainloop()

if __name__ == "__main__":
    main()
