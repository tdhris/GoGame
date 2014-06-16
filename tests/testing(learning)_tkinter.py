import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["fg"] = "dark green"
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["relief"] = "raised"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.QUIT.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
root.geometry('650x600+100+100')
root.title('GoGame 2014')

app = Application(master=root)
app.mainloop()
