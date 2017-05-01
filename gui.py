from tkinter import *

class Application:

    def __init__(self, form):
        #form.resizable(0,0)
        form.minsize(500, 500)
        form.title('Chat Client UI')

        # Global Padding pady and padx
        pad_x = 5
        pad_y = 5

        # create a toplevel menu
        menubar = Menu(form)
        #command= parameter missing.
        #menubar.add_command(label="Menu1")
        #command= parameter missing.
        #menubar.add_command(label="Menu2")
        #command= parameter missing.
        #menubar.add_command(label="Menu3")

        #Displays menu
        form.config(menu = menubar)

        # Create controls
        label1 = Label(form, text="Label1")
        textbox1 = Entry(form)
        #command= parameter missing.
        textbox2 = Entry(form)
        button1 = Button(form, text='Send')

        #Chat history box and scrollbar
        scrollbar1 = Scrollbar(form)
        textarea1 = Text(form, width=50, height=30)

        textarea1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=textarea1.yview)

        #Chat participant list and scrollbar
        scrollbar2 = Scrollbar(form)
        textarea2 = Text(form, width=10, height=30)

        textarea2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=textarea2.yview)




        textarea1.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky=W)
        scrollbar1.grid(row=0, column=2, padx=pad_x, pady=pad_y, sticky=W)
        textbox1.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky=W)
        button1.grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky=W)

        textarea2.grid(row=0, column=2, padx=pad_x, pady=pad_y, sticky=W)
        scrollbar2.grid(row=0, column=3, padx=pad_x, pady=pad_y, sticky=W)
        textbox2.grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky=W)

        form.mainloop()

root = Tk()
Application(root)
