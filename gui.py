from tkinter import *

class ChatGUI:

    def __init__(self, form):
        #form.resizable(0,0)
        form.minsize(550, 500)
        form.title('Chat Client UI')

        #Global Padding pad_y and pad_x
        pad_x = 5
        pad_y = 5

        #Create a toplevel menu
        menubar = Menu(form)

        #Displays menu
        form.config(menu = menubar)

        #Create 'send' button control
        label1 = Label(form, text="Label1")
        #textbox1 = Entry(form)
        button1 = Button(form, text='Send')

        """WIDGETS REFERENCE
        --textarea1 - chat threads pane
        --scrollbar1 - scrollbar for textarea1
        --textarea2 - chat participants pane
        --scrollbar2 - scrollbar for textarea2
        --textbox1 - chat entry box
        """
        
        #Chat threads pane and scrollbar
        scrollbar1 = Scrollbar(form)
        textarea1 = Text(form, width=45, height=30)

        textarea1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=textarea1.yview)

        #Chat participant pane and scrollbar
        scrollbar2 = Scrollbar(form)
        textarea2 = Text(form, width=20, height=30)

        textarea2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=textarea2.yview)

        #Chat entry pane (using TEXT instead of ENTRY for size purposes)
        textarea3 = Text(form, width=45, height=2)

        #Align objects to window grid
        textarea1.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky=W)
        scrollbar1.grid(row=0, column=2, padx=pad_x, pady=pad_y, sticky=W)
        #textbox1.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky=W)
        button1.grid(row=1, column=2, padx=pad_x+20, pady=pad_y, sticky=W)

        textarea2.grid(row=0, column=2, padx=pad_x+20, pady=pad_y, sticky=W)
        scrollbar2.grid(row=0, column=3, padx=pad_x, pady=pad_y, sticky=W)

        textarea3.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky=W)

        form.mainloop()

root = Tk()
ChatGUI(root)
