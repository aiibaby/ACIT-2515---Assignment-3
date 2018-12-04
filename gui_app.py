import tkinter as tk
import tkinter.ttk
from gui_content.subpage1_view import SubPage1
from gui_content.subpage2_view import SubPage2
import requests
import json

API_ENDPOINT = "http://127.0.0.1:5000/log"
API_ENDPOINT_get_all_readings = "http://127.0.0.1:5000/sensor/temperature/reading/all"


class Page(tk.Frame):
    """ Page Frame Class """

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class TemperaturePage(Page):
    """ TemperaturePage Class"""

    def __init__(self, *args, **kwargs):
        """ Initializes the TemperaturePage """
        Page.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="Temperature Sensor Controller")
        self.label.place(x=350, y=0)
        self.addBtn = tkinter.Button(self, text="Add", width=15, command=lambda: SubPage1(0, self.displayall, ""))
        self.delBtn = tkinter.Button(self, text="Delete", width=15, command=self.delete)
        self.updBtn = tkinter.Button(self, text="Update", width=15, command=lambda: SubPage1(1, self.displayall,
                                                                                             self.displaywindow.item(
                                                                                                 self.displaywindow.focus())[
                                                                                                 "values"]))
        self.getBtn = tkinter.Button(self, text="Find One", width=15, command=lambda: SubPage1(2, self.insertvalue, ""))
        self.allBtn = tkinter.Button(self, text="Display All", width=15, command=self.int_displayall)
        self.addBtn.place(x=10, y=30)
        self.delBtn.place(x=10, y=80)
        self.updBtn.place(x=10, y=130)
        self.getBtn.place(x=10, y=180)
        self.allBtn.place(x=10, y=230)

        self.displaywindow = tkinter.ttk.Treeview(self, columns=(
            "id", "date", "model", "min_reading", "avg_reading", "max_reading", "status"))
        self.displaywindow["show"] = "headings"
        self.displaywindow.column("id", width=40, anchor="center")
        self.displaywindow.heading("id", text="ID")
        self.displaywindow.column("date", width=100, anchor="center")
        self.displaywindow.heading("date", text="Timestamp")
        self.displaywindow.column("model", width=80, anchor="center")
        self.displaywindow.heading("model", text="Model")
        self.displaywindow.column("min_reading", width=89, anchor="center")
        self.displaywindow.heading("min_reading", text="Min_reading")
        self.displaywindow.column("avg_reading", width=79, anchor="center")
        self.displaywindow.heading("avg_reading", text="Avg_reading")
        self.displaywindow.column("max_reading", width=79, anchor="center")
        self.displaywindow.heading("max_reading", text="Max_reading")
        self.displaywindow.column("status", width=79, anchor="center")
        self.displaywindow.heading("status", text="Status")
        self.displaywindow.place(x=150, y=30)
        self.scrollbar = tkinter.ttk.Scrollbar(self, orient="vertical", command=self.displaywindow.yview)
        self.scrollbar.place(x=40 + 100 + 80 + 80 + 79 + 79 + 79 + 150, y=30, height=230)
        self.statuslabel = tkinter.Label(self, text="Status Code : N/A", width=40)
        self.statuslabel.place(x=275, y=270)
        self.displaywindow.configure(yscrollcommand=self.scrollbar.set)

    def insertvalue(self, value, code):
        """ Callback function for insert value to treeview table """
        self.displaywindow.delete(*self.displaywindow.get_children())
        self.displaywindow.insert("", "end", value=value)
        self.statuslabel["text"] = "Status Code :  " + str(code)

    def delete(self):
        """ Delete readings """
        self.delete_id = self.displaywindow.item(self.displaywindow.focus())["values"][0]
        self.code = requests.delete(f"http://127.0.0.1:5000/sensor/temperature/reading/{self.delete_id}").status_code
        self.statuslabel["text"] = "Status Code :  " + str(self.code) + ". Delete Successfully."
        self.displaywindow.delete(*self.displaywindow.get_children())
        response = requests.get("http://127.0.0.1:5000/sensor/temperature/reading/all").json()
        for item in response:
            self.displaywindow.insert("", "end", values=[item["id"], item["timestamp"], item["model"],
                                                         item["min_reading"], item["avg_reading"],
                                                         item["max_reading"], item["status"]])

    def displayall(self, code):
        """ Callback function for Display all readings """
        self.displaywindow.delete(*self.displaywindow.get_children())
        response = requests.get("http://127.0.0.1:5000/sensor/temperature/reading/all").json()
        for item in response:
            self.displaywindow.insert("", "end", values=[item["id"], item["timestamp"], item["model"],
                                                         item["min_reading"], item["avg_reading"],
                                                         item["max_reading"], item["status"]])

        self.statuslabel["text"] = "Status Code :  " + str(code)

    def int_displayall(self):
        """ Display all readings from reading """
        self.displaywindow.delete(*self.displaywindow.get_children())
        response = requests.get("http://127.0.0.1:5000/sensor/temperature/reading/all").json()
        self.code = requests.get("http://127.0.0.1:5000/sensor/pressure/reading/all").status_code
        for item in response:
            self.displaywindow.insert("", "end", values=[item["id"], item["timestamp"], item["model"],
                                                         item["min_reading"], item["avg_reading"],
                                                         item["max_reading"], item["status"]])
        self.statuslabel["text"] = "Status Code :  " + str(self.code) + ".  Display all readings successfully"

class PressurePage(Page):
    """ PressurePage Class"""

    def __init__(self, *args, **kwargs):
        """ Initializes the PressurePage """
        Page.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="Pressure Sensor Controller")
        self.label.place(x=350, y=0)
        self.addBtn = tkinter.Button(self, text="Add", width=15, command=lambda: SubPage2(0, self.displayall, ""))
        self.delBtn = tkinter.Button(self, text="Delete", width=15, command=self.delete)
        self.updBtn = tkinter.Button(self, text="Update", width=15,
                                     command=lambda: SubPage2(1, self.displayall, self.displaywindow.item(
                                         self.displaywindow.focus())[
                                         "values"]))
        self.getBtn = tkinter.Button(self, text="Find One", width=15, command=lambda: SubPage2(2, self.insertvalue, ""))
        self.allBtn = tkinter.Button(self, text="Display All", width=15, command=self.int_displayall)
        self.addBtn.place(x=10, y=30)
        self.delBtn.place(x=10, y=80)
        self.updBtn.place(x=10, y=130)
        self.getBtn.place(x=10, y=180)
        self.allBtn.place(x=10, y=230)

        self.displaywindow = tkinter.ttk.Treeview(self, columns=(
            "id", "model", "date", "min_reading", "avg_reading", "max_reading", "status"))
        self.displaywindow["show"] = "headings"
        self.displaywindow.column("id", width=40, anchor="center")
        self.displaywindow.heading("id", text="ID")
        self.displaywindow.column("model", width=100, anchor="center")
        self.displaywindow.heading("model", text="Timestamp")
        self.displaywindow.column("date", width=80, anchor="center")
        self.displaywindow.heading("date", text="Model")
        self.displaywindow.column("min_reading", width=89, anchor="center")
        self.displaywindow.heading("min_reading", text="Min_reading")
        self.displaywindow.column("avg_reading", width=79, anchor="center")
        self.displaywindow.heading("avg_reading", text="Avg_reading")
        self.displaywindow.column("max_reading", width=79, anchor="center")
        self.displaywindow.heading("max_reading", text="Max_reading")
        self.displaywindow.column("status", width=79, anchor="center")
        self.displaywindow.heading("status", text="Status")
        self.displaywindow.place(x=150, y=30)
        self.scrollbar = tkinter.ttk.Scrollbar(self, orient="vertical", command=self.displaywindow.yview)
        self.scrollbar.place(x=40 + 100 + 80 + 80 + 79 + 79 + 79 + 150, y=30, height=230)
        self.statuslabel = tkinter.Label(self, text="Status Code : N/A", width=40)
        self.statuslabel.place(x=275, y=270)
        self.displaywindow.configure(yscrollcommand=self.scrollbar.set)

    def insertvalue(self, value, code):
        """ Callback function for insert value to treeview table """
        self.displaywindow.delete(*self.displaywindow.get_children())
        self.displaywindow.insert("", "end", value=value)
        self.statuslabel["text"] = "Status Code :  " + str(code)

    def delete(self):
        """ Delete readings """
        self.delete_id = self.displaywindow.item(self.displaywindow.focus())["values"][0]
        self.code = requests.delete(f"http://127.0.0.1:5000/sensor/pressure/reading/{self.delete_id}").status_code
        self.statuslabel["text"] = "Status Code :  " + str(self.code) + ". Delete Successfully."
        self.displaywindow.delete(*self.displaywindow.get_children())
        response = requests.get("http://127.0.0.1:5000/sensor/pressure/reading/all").json()
        for item in response:
            self.displaywindow.insert("", "end", values=[item["id"], item["timestamp"], item["model"],
                                                         item["min_reading"], item["avg_reading"],
                                                         item["max_reading"], item["status"]])

    def displayall(self, code):
        """ Callback function for Display all readings """
        self.displaywindow.delete(*self.displaywindow.get_children())
        response = requests.get("http://127.0.0.1:5000/sensor/pressure/reading/all").json()
        for item in response:
            self.displaywindow.insert("", "end", values=[item["id"], item["timestamp"], item["model"],
                                                         item["min_reading"], item["avg_reading"],
                                                         item["max_reading"], item["status"]])
        self.statuslabel["text"] = "Status Code :  " + str(code)

    def int_displayall(self):
        """ Display all readings from reading """
        self.displaywindow.delete(*self.displaywindow.get_children())
        response = requests.get("http://127.0.0.1:5000/sensor/pressure/reading/all").json()
        self.code = requests.get("http://127.0.0.1:5000/sensor/pressure/reading/all").status_code
        for item in response:
            self.displaywindow.insert("", "end", values=[item["id"], item["timestamp"], item["model"],
                                                         item["min_reading"], item["avg_reading"],
                                                         item["max_reading"], item["status"]])
        self.statuslabel["text"] = "Status Code :  " + str(self.code) + ".  Display all readings successfully"

class MainView(tk.Frame):
    """ MainView Class """

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = TemperaturePage(self)
        p2 = PressurePage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Temperature", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Pressure", command=p2.lift)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("745x330")
    root.title("Restful Sensor API")
    root.mainloop()
