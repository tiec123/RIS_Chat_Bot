import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pandas as pd
import random
import os
import matplotlib.pyplot as plt
import pickle

class AppointmentScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Scheduler")
        self.root.geometry("1600x600")
        
        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # prediction model
        model_filename = "patient_no_show_xgb_model.sav"
        with open(model_filename, 'rb') as file:
            self.prediction_model = pickle.load(file)
        self.perdiction_features = ["Gender", "Age", "WaitingTime" ,   "Discount" , "Diabetes" ,  "Alcoholism" ,  "Handicap"]

        
        self.create_input_tab()
        self.create_view_tab()

    def create_input_tab(self):
        self.input_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.input_tab, text='New Appointment')

        # Input fields
        ttk.Label(self.input_tab, text="Patient ID:", font=('Helvetica', 12)).grid(row=0, column=0, padx=10, pady=10)
        self.patient_id_entry = ttk.Entry(self.input_tab, font=('Helvetica', 12))
        self.patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.input_tab, text="Name:", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(self.input_tab, font=('Helvetica', 12))
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.input_tab, text="Age:", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=10)
        self.age_entry = ttk.Entry(self.input_tab, font=('Helvetica', 12))
        self.age_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.input_tab, text="Gender:", font=('Helvetica', 12)).grid(row=3, column=0, padx=10, pady=10)
        self.gender_var = tk.StringVar(value='Male')
        ttk.Combobox(self.input_tab, textvariable=self.gender_var, values=["Male", "Female"], font=('Helvetica', 12)).grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(self.input_tab, text="Address:", font=('Helvetica', 12)).grid(row=4, column=0, padx=10, pady=10)
        self.address_entry = ttk.Entry(self.input_tab, font=('Helvetica', 12))
        self.address_entry.grid(row=4, column=1, padx=10, pady=10)

        ttk.Label(self.input_tab, text="Scheduled Date:", font=('Helvetica', 12)).grid(row=5, column=0, padx=10, pady=10)
        self.scheduled_date_entry = DateEntry(self.input_tab, font=('Helvetica', 12))
        self.scheduled_date_entry.grid(row=5, column=1, padx=10, pady=10)

        ttk.Label(self.input_tab, text="Appointment Date:", font=('Helvetica', 12)).grid(row=6, column=0, padx=10, pady=10)
        self.appointment_date_entry = DateEntry(self.input_tab, font=('Helvetica', 12))
        self.appointment_date_entry.grid(row=6, column=1, padx=10, pady=10)

        ttk.Label(self.input_tab, text="Discount:", font=('Helvetica', 12)).grid(row=7, column=0, padx=10, pady=10)
        self.discount_var = tk.StringVar(value='No')
        ttk.Combobox(self.input_tab, textvariable=self.discount_var, values=["Yes", "No"], font=('Helvetica', 12)).grid(row=7, column=1, padx=10, pady=10)

        ttk.Label(self.input_tab, text="Disabilities:", font=('Helvetica', 12)).grid(row=8, column=0, padx=10, pady=10)
        self.disabilities_var = {
            "Hypertension": tk.IntVar(),
            "Diabetes": tk.IntVar(),
            "Alcoholism": tk.IntVar(),
            "Handicap": tk.IntVar()
        }
        for i, (label, var) in enumerate(self.disabilities_var.items()):
            tk.Checkbutton(self.input_tab, text=label, variable=var).grid(row=8, column=i+1, padx=10, pady=10)

        self.submit_button = ttk.Button(self.input_tab, text="Submit", command=self.submit_appointment)
        self.submit_button.grid(row=9, columnspan=2, pady=20)

    def submit_appointment(self):
        # Gather input data
        patient_id = self.patient_id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_var.get()
        address = self.address_entry.get()
        scheduled_date = self.scheduled_date_entry.get()
        appointment_date = self.appointment_date_entry.get()
        discount = self.discount_var.get()

        # Validate input data
        if not patient_id or not name or not age or not address:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return
        if not age.isdigit() or int(age) <= 0:
            messagebox.showerror("Input Error", "Please enter a valid age.")
            return

        # Calculate waiting time in hours
        scheduled_dt = pd.to_datetime(scheduled_date)
        appointment_dt = pd.to_datetime(appointment_date)
        waiting_time = (appointment_dt - scheduled_dt).total_seconds() / 3600

        # Create a data entry
        data = {
            "Patient ID": patient_id,
            "Name": name,
            "Gender": 1 if gender == "Male" else 0,
            "Age": age,
            "Address": address,
            "Scheduled Date": scheduled_date,
            "Appointment Date": appointment_date,
            "Discount": 1 if discount == "Yes" else 0,
            "Hypertension": self.disabilities_var["Hypertension"].get(),
            "Diabetes": self.disabilities_var["Diabetes"].get(),
            "Alcoholism": self.disabilities_var["Alcoholism"].get(),
            "Handicap": self.disabilities_var["Handicap"].get(),
            "WaitingTime": waiting_time,
            "No_show": 0  # Placeholder for No_show
        }

        # Append data to CSV
        df = pd.DataFrame([data])
        file_exists = os.path.isfile('appointments.csv')
        df.to_csv('appointments.csv', mode='a', index=False, header=not file_exists)

        messagebox.showinfo("Success", "Appointment submitted successfully!")

    def create_view_tab(self):
        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_tab, text='View Appointments')

        ttk.Label(self.view_tab, text="Select Appointment Date:", font=('Helvetica', 12)).grid(row=0, column=0, padx=10, pady=10)
        self.view_date_entry = DateEntry(self.view_tab, font=('Helvetica', 12))
        self.view_date_entry.grid(row=0, column=1, padx=10, pady=10)

        self.view_button = ttk.Button(self.view_tab, text="View Appointments", command=self.view_appointments)
        self.view_button.grid(row=0, column=2, padx=10, pady=10)

        self.appointment_list = ttk.Treeview(self.view_tab, columns=("Patient ID", "Name", "Gender", "Age", "Scheduled Date", "Appointment Date", "No Show Probability"), show='headings')
        self.appointment_list.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        for col in self.appointment_list["columns"]:
            self.appointment_list.heading(col, text=col)

        # Slider for threshold
        ttk.Label(self.view_tab, text="No Show Probability Threshold:", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=10)
        self.threshold_slider = tk.Scale(self.view_tab, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
        self.threshold_slider.set(0.5)
        self.threshold_slider.grid(row=2, column=1, padx=10, pady=10)

        self.plot_button = ttk.Button(self.view_tab, text="Show Pie Chart", command=self.plot_pie_chart)
        self.plot_button.grid(row=2, column=2, padx=10, pady=10)

    def view_appointments(self):
        date = self.view_date_entry.get()
        self.date = date
        self.appointment_list.delete(*self.appointment_list.get_children())

        if os.path.isfile('appointments.csv'):
            df = pd.read_csv('appointments.csv')
            filtered_df = df[df['Appointment Date'] == date]
            
            for _, row in filtered_df.iterrows():
                # Generate the probability for no-show
                X_pred = row[self.perdiction_features].values.reshape(1, -1)
                print(X_pred)
                no_show_probability = self.prediction_model.predict_proba(X_pred)[0][1]
                no_show_probability = random.uniform(0, 1)  # Placeholder for your model
                self.appointment_list.insert("", "end", values=(
                    row["Patient ID"], row["Name"], row["Gender"],
                    row["Age"], row["Scheduled Date"], row["Appointment Date"],
                    f"{no_show_probability:.2f}"))

                # Update No_show column in the CSV
                df.loc[_, 'No_show'] = no_show_probability
            
            df.to_csv('appointments.csv', index=False)

    def plot_pie_chart(self):
        # Get the probability threshold from the slider
        threshold = self.threshold_slider.get()
        if os.path.isfile('appointments.csv'):
            df = pd.read_csv('appointments.csv')
            date_df = df[df['Appointment Date'] == self.date]
            filtered_df = date_df[(date_df['No_show'] >= threshold) ]

            no_show_count = len(filtered_df)
            total_count = len(date_df)

            if total_count > 0:
                plt.figure(figsize=(6, 6))
                plt.pie([no_show_count, total_count - no_show_count], labels=['No Show', 'Show'], autopct='%1.1f%%', startangle=140)
                plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                plt.title("No Show Probability Distribution")
                plt.show()
            else:
                messagebox.showinfo("No Data", "No appointments found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentScheduler(root)
    root.mainloop()
