from tkinter import *
from tkinter.messagebox import *

#BACK-END-------------------BACK-END-------------------------------BACK-END-------------------------------------BACK-END

record = []

def compute():

    global record

    try:
        x = entry.get() +  ' = ' + format( eval(entry.get()) , ',.2f')
    except:
        showerror('Error 404','Cannot be computed')
    else:
        label.config(text = x)
        record.append( str(len(record)+ 1) + '.\t' + x )

def history():

    showinfo('History','\n\n'.join(record))

#FRONT-END -------------------FRONT-END-------------------------------FRONT-END--------------------------------FRONT-END

TK = Tk()

TK.title('Simple Calculator')

label = Label(text = '', font = ('Arial', '20'), width = 12)
label.grid(row = 0, column = 0, columnspan = 2)

entry = Entry(font = ('Arial', '20'), width =12)
entry.grid(row = 1, column = 0, columnspan = 2)

button_1 = Button(text = 'compute',command = compute,font = ('Arial','16'))
button_1.grid(row = 2,column = 0)

button_2 = Button(text = 'history',command = history,font = ('Arial','16'))
button_2.grid(row = 2 ,column =1)

TK.mainloop()