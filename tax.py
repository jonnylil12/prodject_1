
#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 5.6
#  in conjunction with Tcl version 8.6
#    Nov 09, 2020 07:00:14 PM EST  platform: Windows NT

import sys

def __no():

    print('no')


try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import tax_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    tax_support.set_Tk_var()
    top = Toplevel1 (root)
    tax_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    tax_support.set_Tk_var()
    top = Toplevel1 (w)
    tax_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = 'wheat'  # X11 color: #f5deb3
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font9 = "-family {DejaVu Sans Mono} -size 14"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font=font9)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1304x651+629+516")
        top.minsize(232, 1)
        top.maxsize(3004, 1959)
        top.resizable(0,  0)
        top.title("New Toplevel")
        top.configure(background="wheat")
        top.title('Turbotax')

        self.Label1 = tk.Label(top)
        self.Label1.place(x=170, y=40, height=118, width=1000)
        self.Label1.configure(background="wheat")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="-family {Arial} -size 24")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='\t\tWelcome to Turbo tax \
                              \nPlease enter your taxable income and Filing Status!')

        self.Button1 = tk.Button(top)
        self.Button1.place(x=480, y=510, height=112, width=391)
        self.Button1.configure(activebackground="#f4bcb2")
        self.Button1.configure(activeforeground="#ff0000")
        self.Button1.configure(background="#ffffff")
        self.Button1.configure(command=tax_support.tax)
        self.Button1.configure(cursor="fleur")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font="-family {Arial} -size 24")
        self.Button1.configure(foreground="#ff0000")
        self.Button1.configure(highlightbackground="wheat")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Calculate tax''')

        self.Entry1 = tk.Entry(top)
        self.Entry1.place(x=500, y=230, height=56, width=354)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="-family {Arial} -size 24")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(textvariable=tax_support.income_var)

        self.Label2 = tk.Label(top)
        self.Label2.place(x=300, y=230, height=58, width=200)
        self.Label2.configure(background="wheat")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Arial} -size 24")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text= "Income:\t  $" )


        self.Label3 = tk.Label(top)
        self.Label3.place(x=290, y=370, height=60, width=200)
        self.Label3.configure(background="wheat")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font="-family {Arial} -size 24")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Filling status:''')

        self.TCombobox1 = ttk.Combobox(top)
        self.TCombobox1.place(x=500, y=370, height=58, width=360)
        self.TCombobox1.configure(font="-family {Segoe UI} -size 24")
        self.TCombobox1.configure(textvariable=tax_support.filling_var)
        self.TCombobox1.configure(takefocus="")

if __name__ == '__main__':
    vp_start_gui()





