import tkinter as tk
from tkcalendar import DateEntry

class DatetimeEntry(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # add the date selection
        self.date = DateEntry(self, date_pattern = "y-mm-dd")

        # pack the hours, minutes and seconds in a frame
        self.time_frame = tk.Frame(self)

        # hours, minutes, seconds
        self.hours = tk.Spinbox(self.time_frame,from_=0,to=23, wrap=True, format="%02.0f", width=3)
        self.minutes= tk.Spinbox(self.time_frame,from_=0,to=59, wrap=True, format="%02.0f", width=3)
        self.seconds = tk.Spinbox(self.time_frame,from_=0,to=59, wrap=True, format="%02.0f", width=3)

        #self.hours.grid(row=0, column=0)
        #self.minutes.grid(row=0, column=1)
        #self.seconds.grid(row=0, column=2)
        self.hours.pack(side=tk.LEFT, fill=tk.X, expand=0)
        self.minutes.pack(side=tk.LEFT, fill=tk.X, expand=0)
        self.seconds.pack(side=tk.LEFT, fill=tk.X, expand=0)

        # pack it up
        #self.date.grid(row=0, column=0)
        #self.time_frame.grid(row=0, column=1)
        self.date.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.time_frame.pack(side=tk.LEFT, fill=tk.X, expand=1)
    def get(self):
        # return time value
        return "{}T{}:{}:{}Z".format(self.date.get(), self.hours.get(), self.minutes.get(), self.seconds.get())
    def set(self, content):
        content=content.strip()
        from datetime import datetime
        if content.endswith("Z"):
            if "." in content:
                d=datetime.strptime(content, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                d=datetime.strptime(content, "%Y-%m-%dT%H:%M:%SZ")
        else:
            if "." in content:
                d=datetime.strptime(content, "%Y-%m-%dT%H:%M:%S.%f")
            else:
                d=datetime.strptime(content, "%Y-%m-%dT%H:%M:%S")


        self.date.set_date(d)
        t=d.time()
        self.hours.delete(0,"end")
        self.minutes.delete(0,"end")
        self.seconds.delete(0,"end")
        self.hours.insert(0, "{0:02d}".format(t.hour))
        self.minutes.insert(0, "{0:02d}".format(t.minute))
        self.seconds.insert(0, "{0:02d}".format(t.second))

