import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frame = tk.Frame(self)
        self.frame.pack(side="top", fill="both", expand=True)
        self.label = tk.Label(self, text="Hello, world")
        button1 = tk.Button(self, text="Click to hide label",
                           command=self.hide_label)
        button2 = tk.Button(self, text="Click to show label",
                            command=self.show_label)
        self.label.pack(in_=self.frame)
        button1.pack(in_=self.frame)
        button2.pack(in_=self.frame)

    def show_label(self, event=None):
        self.label.lift(self.frame)

    def hide_label(self, event=None):
        self.label.lower(self.frame)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
