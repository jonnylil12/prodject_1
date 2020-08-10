from tkinter import *
from tkinter.messagebox import *

class simple_calc:

    def __init__(self):
        self.record = []

        self.TK = Tk()

        self.TK.title('Simple Calculator')

        self.label = Label(text='', font=('Arial', '20'), width=12)
        self.label.grid(row=0, column=0, columnspan=2)

        self.entry = Entry(font=('Arial', '20'), width=12)
        self.entry.grid(row=1, column=0, columnspan=2)

        self.button_1 = Button(text='compute', command=self.compute, font=('Arial', '16'))
        self.button_1.grid(row=2, column=0)

        self.button_2 = Button(text='history', command=self.history, font=('Arial', '16'))
        self.button_2.grid(row=2, column=1)

        self.TK.mainloop()

    def compute(self):

        try:
            x = self.entry.get() +  ' = ' + format( eval(self.entry.get()) , ',.2f')
        except:
            showerror('Error 404','Cannot be computed')
        else:
            self.label.config(text = x)
            self.record.append( str(len(self.record)+ 1) + '.\t' + x )

    def history(self):
        print(True)
        showinfo('History','\n\n'.join(self.record))

SC = simple_calc()
