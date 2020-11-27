import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from verige import math_constants, format_results
import mpmath as mp

mp.dps = 1000

# Run to create .exe file pyinstaller --windowed --onefile main_v4.pyw
class Example(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=2)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.labels = []

    def populate(self, combobox, entry, entryN, entryM, checkbutton):
        # See what's selected from combobox.
        if comboBox.get() == "arbitrary":
            # Check if given value for number is of proper type.
            try: 
                num = float(entry.get())
            except ValueError:
                messagebox.showerror(title="Invalid input", message="Input should be a real number.")
                return

        # Make sure that limits for n and m are valid integers.
        try: 
            n = int(entryN.get())
        except ValueError:
            messagebox.showerror(title="Invalid input", message="Number n must be a non zero integer.")
            return

        try: 
            m = int(entryM.get())
        except:
            messagebox.showerror(title="Invalid input", message="Number m must be a non zero integer.")
            return

        # Check if given values for n and m are in proper range.
        if int(entryN.get()) <= 0:
            messagebox.showerror(title="Invalid input", message="Input parameter n must be a non zero integer.")
            return 
        if int(entryM.get()) <= 0: 
            messagebox.showerror(title="Invalid input", message="Input parameter m must be a non zero integer.")
            return 

        # If n is bigger than m show warning about switching them.
        if n > m:
            messagebox.showwarning(title="Warning", message="Range is not proper, will use given n as m and given m as n.")
            m, n = n, m

        # If all is good use them to find approximations.
        if comboBox.get()== "arbitrary":
            num = mp.mpmathify(entry.get())
        else :
            num = math_constants[comboBox.get()]

        frac = format_results(num, n, m, checkbutton.get())

        for l in self.labels:
            l.config(image = "")
            l.grid_forget()
        del self.labels[:]

        for i,f in enumerate(frac):
            l0 = tk.Label(self.frame, text=f[0], font='Helvetica 12', anchor="w")
            l0.grid(row = i, column=0, sticky="w")
            self.labels.append(l0)

            l1 = tk.Label(self.frame, text=f[1], font='Helvetica 12', anchor="w")
            l1.grid(row = i, column=1, sticky="e")
            self.labels.append(l1)

            if f[0][-1] == '*':
                l0.configure(font='Helvetica 12 bold')
                l1.configure(font='Helvetica 12 bold')

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root=tk.Tk()
    root.title("Rational approximations of numbers")

    commandsFrame = tk.Frame(root, highlightbackground="black", highlightthickness=1, border=10)
    commandsFrame.pack(side = "top")
    labelEntry = tk.Label(commandsFrame, text = "Number")
    labelEntry.pack(side="top")

    num = tk.StringVar()
    entry = tk.Entry(commandsFrame, width=70, textvariable=num)
    entry.pack(side="top")

    labelCombo = tk.Label(commandsFrame, text = "Choose mathematical constant")
    labelCombo.pack(side="top")

    comboBox = ttk.Combobox(commandsFrame, 
                                values=["arbitrary"] + list(math_constants.keys()))
    comboBox.pack(side="top")
    comboBox.current(0)

    # Create field for n.
    labelN = tk.Label(commandsFrame, text = "n")
    labelN.pack(side="top")

    n = tk.StringVar()
    entryN = tk.Entry(commandsFrame, width=30, textvariable=n)
    entryN.pack(side="top")

    # Create field for m.
    labelM = tk.Label(commandsFrame, text = "m")
    labelM.pack(side="top")

    m = tk.StringVar()
    entryM = tk.Entry(commandsFrame, width=30, textvariable=m)
    entryM.pack(side="top")

    var1 = tk.IntVar()
    tk.Checkbutton(commandsFrame, text="sort absolute error", variable=var1).pack(side="top")

    # Create buttons - Enter and Quit
    ENTER = tk.Button(commandsFrame, text="ENTER", fg="black", width=20)
                                        
    ENTER.pack(side="top")

    QUIT = tk.Button(commandsFrame, text="QUIT", fg="black",
                                        command=root.destroy, width=20)
    QUIT.pack(side="top")

    example = Example(root)
    example.pack(side="top", fill="both", expand=True)

    ENTER.configure(command = lambda: example.populate(comboBox, entry, entryN, entryM, var1))

    root.mainloop()