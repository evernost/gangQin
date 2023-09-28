from tkinter import *

def mychoicebox(choicelist):
    global result

    def buttonfn():
        global result
        result = var.get()
        choicewin.quit()

    choicewin = Tk()
    choicewin.resizable(False, False)
    choicewin.title("ChoiceBox")

    Label(choicewin, text="Select an item:").grid(row=0, column=0, sticky="W")

    var = StringVar(choicewin)
    var.set("No data")  # default option
    popupMenu = OptionMenu(choicewin, var, *choicelist)
    popupMenu.grid(sticky=N + S + E + W, row=1, column=0)

    Button(choicewin, text="Done", command=buttonfn).grid(row=2, column=0)
    choicewin.mainloop()
    return result

# Testing:

reply = mychoicebox(["one", "two", "three"])
print("reply:", reply)