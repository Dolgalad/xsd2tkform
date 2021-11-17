"""Some Entry widgets with validation depending on type
"""
import tkinter as tk


class FloatEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent)
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.configure(validate="all", validatecommand=vcmd)

    def validate(self, *args):
        try:
            i=float(args[2])
            self.config(fg="black")
            return True
        except:
            self.config(fg="red")
            return True
    def get(self, *args, **kwargs):
        return float(self.get(*args, **kwargs))
    def set(self, value):
        self.delete(0, tk.END)
        self.insert(0, value)


class IntEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent)
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.configure(validate="all", validatecommand=vcmd)
    def set(self, value):
        self.delete(0, tk.END)
        self.insert(0, value)
    def get(self, *args, **kwargs):
        return int(self.get(*args, **kwargs))


    def validate(self, *args):
        try:
            i=int(args[2])
            self.config(fg="black")
            return True
        except:
            self.config(fg="red")
            return True

class BoolEntry(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)#highlightbackground="bleu", highlightthickness=2)
        vals = ["true", "false"]
        labels=["True", "False"]
        self.var = tk.StringVar()
        self.var.set(vals[0])
        for i in range(2):
            tk.Radiobutton(self, variable=self.var, text=labels[i], value=vals[i]).pack(side=tk.LEFT, fill=tk.X, expand=1)
    def get(self, *args):
        return self.var.get()
    def set(self, value):
        self.var.set(value)

if __name__=="__main__":
    root = tk.Tk()

    float_entry = FloatEntry(root)
    float_entry.pack(side=tk.TOP, fill=tk.X, expand=1)

    int_entry = IntEntry(root)
    int_entry.pack(side=tk.TOP, fill=tk.X, expand=1)

    root.mainloop()
