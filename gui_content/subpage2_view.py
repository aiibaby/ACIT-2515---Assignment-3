import tkinter
import tkinter.ttk
import requests
import json


class SubPage2:
    """ SubPage2 Class"""

    def __init__(self, type, value, exist_value):
        """ Initializes the SubPage2 """
        self.tk = tkinter.Toplevel()
        self.value = value
        self.type = type
        self.exist_value = exist_value
        self.tk.geometry('270x335')
        self.button1 = tkinter.Button(self.tk, text="Submit", width=15, command=self.send)
        self.button1.place(x=10, y=300)
        self.button2 = tkinter.Button(self.tk, text="Close", width=15, command=self.tk.destroy)
        self.button2.place(x=150, y=300)
        if self.type == 2:
            self.tk.title("Find Pressure Reading")
            self.id_label = tkinter.Label(self.tk, text="ID", width=15)
            self.id_label.place(x=10, y=10)
            self.id_entry = tkinter.Entry(self.tk, width=23)
            self.id_entry.place(x=110, y=10)

        elif self.type == 1:
            self.tk.title("Update Pressure Reading")
            self.id_label = tkinter.Label(self.tk, text="ID", width=15)
            self.id_label.place(x=10, y=10)
            self.id_entry = tkinter.Entry(self.tk, width=23)
            self.id_entry.place(x=110, y=10)
            self.date_label = tkinter.Label(self.tk, text="Timestamp", width=15)
            self.date_label.place(x=10, y=40)
            self.date_entry = tkinter.Entry(self.tk, width=23)
            self.date_entry.place(x=110, y=40)
            self.model_label = tkinter.Label(self.tk, text="Model", width=15)
            self.model_label.place(x=10, y=70)
            self.model_entry = tkinter.Entry(self.tk, width=23)
            self.model_entry.place(x=110, y=70)
            self.min_label = tkinter.Label(self.tk, text="Min_reading", width=15)
            self.min_label.place(x=10, y=100)
            self.min_entry = tkinter.Entry(self.tk, width=23)
            self.min_entry.place(x=110, y=100)
            self.avg_label = tkinter.Label(self.tk, text="Avg_reading", width=15)
            self.avg_label.place(x=10, y=130)
            self.avg_entry = tkinter.Entry(self.tk, width=23)
            self.avg_entry.place(x=110, y=130)
            self.max_label = tkinter.Label(self.tk, text="Max_reading", width=15)
            self.max_label.place(x=10, y=160)
            self.max_entry = tkinter.Entry(self.tk, width=23)
            self.max_entry.place(x=110, y=160)
            self.status_label = tkinter.Label(self.tk, text="Status", width=15)
            self.status_label.place(x=10, y=190)
            self.status_entry = tkinter.Entry(self.tk, width=23)
            self.status_entry.place(x=110, y=190)
            if self.exist_value != "":
                self.id_entry.insert(tkinter.END, self.exist_value[0])
                self.date_entry.insert(tkinter.END, self.exist_value[1])
                self.model_entry.insert(tkinter.END, self.exist_value[2])
                self.min_entry.insert(tkinter.END, self.exist_value[3])
                self.avg_entry.insert(tkinter.END, self.exist_value[4])
                self.max_entry.insert(tkinter.END, self.exist_value[5])
                self.status_entry.insert(tkinter.END, self.exist_value[6])
        else:
            self.tk.title("Add Pressure Reading")
            self.date_label = tkinter.Label(self.tk, text="Timestamp", width=15)
            self.date_label.place(x=10, y=10)
            self.date_entry = tkinter.Entry(self.tk, width=23)
            self.date_entry.place(x=110, y=10)
            self.model_label = tkinter.Label(self.tk, text="Model", width=15)
            self.model_label.place(x=10, y=40)
            self.model_entry = tkinter.Entry(self.tk, width=23)
            self.model_entry.place(x=110, y=40)
            self.min_label = tkinter.Label(self.tk, text="Min_reading", width=15)
            self.min_label.place(x=10, y=70)
            self.min_entry = tkinter.Entry(self.tk, width=23)
            self.min_entry.place(x=110, y=70)
            self.avg_label = tkinter.Label(self.tk, text="Avg_reading", width=15)
            self.avg_label.place(x=10, y=100)
            self.avg_entry = tkinter.Entry(self.tk, width=23)
            self.avg_entry.place(x=110, y=100)
            self.max_label = tkinter.Label(self.tk, text="Max_reading", width=15)
            self.max_label.place(x=10, y=130)
            self.max_entry = tkinter.Entry(self.tk, width=23)
            self.max_entry.place(x=110, y=130)
            self.status_label = tkinter.Label(self.tk, text="Status", width=15)
            self.status_label.place(x=10, y=160)
            self.status_entry = tkinter.Entry(self.tk, width=23)
            self.status_entry.place(x=110, y=160)

    def send(self):
        """ Send requests to API """
        if self.type == 2:
            # Find one Reading
            try:
                self.code = requests.get(
                    f"http://127.0.0.1:5000/sensor/pressure/reading/{self.id_entry.get()}").status_code
                response = requests.get(f"http://127.0.0.1:5000/sensor/pressure/reading/{self.id_entry.get()}").json()
                self.pass_massage = str(self.code) + ".  Find reading successfully."
                self.value([response["id"], response["timestamp"], response["model"], response["min_reading"],
                            response["avg_reading"],
                            response["max_reading"], response["status"]], self.pass_massage)
                self.tk.destroy()
            except:
                self.pass_massage = str(self.code) + ".  Find reading unsuccessfully."
                self.value("", self.pass_massage)
                self.tk.destroy()

        elif self.type == 1:
            # Update Readings
            self.update_message = {
                "timestamp": self.date_entry.get(),
                "model": self.model_entry.get(),
                "min_reading": self.min_entry.get(),
                "avg_reading": self.avg_entry.get(),
                "max_reading": self.max_entry.get(),
                "status": self.status_entry.get()
            }
            headers = {"content-type": "application/json"}
            self.code = requests.put(f"http://127.0.0.1:5000/sensor/pressure/reading/{self.id_entry.get()}",
                                     json=self.update_message, headers=headers).status_code
            if self.code == 200:
                self.pass_massage = str(self.code) + ".  Update reading successfully"
                self.value(self.pass_massage)
                self.tk.destroy()
            else:
                self.pass_massage = str(self.code) + ".  Update reading unsuccessfully"
                self.value(self.pass_massage)
                self.tk.destroy()
        else:
            # Add Readings
            self.add_message = {
                "timestamp": self.date_entry.get(),
                "model": self.model_entry.get(),
                "min_reading": self.min_entry.get(),
                "avg_reading": self.avg_entry.get(),
                "max_reading": self.max_entry.get(),
                "status": self.status_entry.get()
            }
            headers = {"content-type": "application/json"}
            self.code = requests.post("http://127.0.0.1:5000/sensor/pressure/reading", json=self.add_message,
                                      headers=headers).status_code
            if self.code == 200:
                self.pass_massage = str(self.code) + ".  Add reading successfully"
                self.value(self.pass_massage)
                self.tk.destroy()
            else:
                self.pass_massage = str(self.code) + ".  Add reading unsuccessfully"
                self.value(self.pass_massage)
                self.tk.destroy()
