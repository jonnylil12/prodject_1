from tkinter import *
from tkinter.messagebox import *
import sqlite3
import re
from datetime import date , timedelta ,datetime

BAR_CODE_LENGTH = 7  # fset the length of user bar codes

print('Hello')

#BACKEND----------------------------------------BACKEND-------------------------------------BACKEND

def DATABASE(query):
    with sqlite3.connect('database.db') as file:
        cursor = file.cursor()            #create connection of main database and submits querys to database
        cursor.execute(query)
        file.commit()
        result = cursor.fetchall()
    return result




def PAGE_ERROR_HANDLER(PAGE):       #decorator that wraps functions with a error catcher
   def OVERRIDED_FUNC(*data):       #accepts parameters if overriden function has them
        try:
            PAGE(*data)     #will return values if ovverriden function returns values
        except:
            pass
   return OVERRIDED_FUNC




def ERROR(code):

    CODES = {
    # 100+    == system errors
    100: ' Invalid command'    ,                                107:' Book is currently unavailable to checkout' ,
    101: ' Ivalid name characters and spaces only',             108:' Book cannot be renewed hold has been placed' ,
    102: ' Invalid email address ',                             109:'  Cannot renew book more than twice ',
    103: ' Email address already exists',                       110:' Borrower has not checked out this book' ,
    104: ' Account not found',                                  111:' Book is avaliable to be checked out ' ,
    105: ' Book(s) not found',                                  112:' Borrower has already checked out this book' ,
    106: ' Balance greater than $5.00 ',                        113:' Borrower already has hold for this book ' ,
    # 200+   ==  system errors
    200:' Bar Code generator has reached max capacity' ,
    201:' There are no books available in the system '

    }
    if code < 200:
            showerror(f"USER ERROR {code}",f"{CODES[code]}")  #return specific exception message with code
    else:
            showerror(f"SYSTEM ERROR {code}",f"{CODES[code]}")




def GENERATE_BAR_CODE():
    ALL_USER_BAR_CODES = DATABASE("select User_ID from Borrowers")
    if ALL_USER_BAR_CODES  :                    #checks if there is no user bar codes in the database
        return ALL_USER_BAR_CODES[-1][0] + 1
    return   int('1' + '0' *( BAR_CODE_LENGTH - 1))    # formula to find smallet bar code of specific length






def EXPIRED_HOLDS():  #remove expired holds
    for record in DATABASE("select * from Queue where Holddate"):
        if  date.today() == datetime.strptime(record[5],"%Y-%m-%d").date() :  #check if hold has expired
            #remove hold from queue and update queue
            DATABASE(f"delete from Queue where Barcode == {record[0]} and User_ID == {record[1]}")
            DATABASE(f"update Queue set Queue_ID = Queue_ID - 1 where Barcode == {record[0]}")
            #gret and set hold date for next in queue
            HOLD_DATE = date.today() + timedelta(weeks=1)
            DATABASE(f"update Queue set Holddate = '{HOLD_DATE}' where Barcode == {record[0]} and Queue_ID = 1")

            # todo alert user that there hold has expired by email



def OVERDUE_BOOKS():  #issue fines
    for record in DATABASE("select * from Queue where Duedate"):
        today , duedate = date.today() , datetime.strptime(record[2], "%Y-%m-%d").date()
        if today > duedate:     #book is overdue
            choice = input(f"Borrower {record[1]} has overdue book \
                           \nEnter 'F= barcode' to issue fine\n: ").split()
            #apply fine
            DATABASE(f"update Borrowers set Balance = Balance + 0.10 where User_ID == {record[1]}")

        elif today == duedate - timedelta(days=3):  # if 3 days before book is due send email
            pass
            #todo email persom



@PAGE_ERROR_HANDLER
def PLACE_HOLD(BOOK,BORROWER,QUEUE):
    assert len(QUEUE) , ERROR(111)  # book isnt checked out
    assert  BORROWER[0] != QUEUE[0][1] and not QUEUE[0][2] , ERROR(112) # borrower cant place hold on book he has
    HOLDERS = [x[0] for x in DATABASE(f"select User_ID from Queue where Barcode == {BOOK[3]}")]
    assert BORROWER[0] not in HOLDERS, ERROR(113)   # borrower already has hold on book
    DATABASE(f"insert into Queue values({BOOK[3]},{BORROWER[0]},NULL,0,{len(QUEUE) + 1},NUll)")
    showinfo("Place hold",f"\nHold has succesfully been placed \nand will expire one week after book has been returned")




@PAGE_ERROR_HANDLER
def RETURN_BOOK(BOOK,BORROWER,QUEUE):
    assert QUEUE, ERROR(110)
    assert QUEUE[0][1] == BORROWER[0] and QUEUE[0][2]  , ERROR(110) # borrower didnt check out book
    DATABASE(f"delete from Queue where Barcode == {BOOK[3]} and User_ID == {BORROWER[0]}")  # remove borrower from queue
    DATABASE(f"update Queue set Queue_ID = Queue_ID - 1 where Barcode == {BOOK[3]}")  # update the queue
    # give holdate to next person in line for one week if there is a queue
    HOLD_DATE = date.today() + timedelta(weeks=1)
    DATABASE(f"update Queue set Holddate  = '{HOLD_DATE}' where Barcode == {BOOK[3]} and Queue_ID = 1")
    DATABASE(f"update Books set Status == 1 where Barcode == {BOOK[3]}")  # update status of book for admin purpose
    showinfo("Return book", f"\nBook succefully returned thank you for your buisness")





@PAGE_ERROR_HANDLER
def CHECK_OUT_BOOK(BOOK,BORROWER,QUEUE):
    DUE_DATE = date.today() + timedelta(weeks=3)  # get the date 3 weeks from today

    assert BORROWER[3] < 5.00 , ERROR(106)  #check if balance requirment is met
    if QUEUE:  # book has been checkout or has holds

        assert QUEUE[0][1] == BORROWER[0],   ERROR(107)  # book is unavaliable to borrower

        if QUEUE[0][5]:  # current borrower has hold on book
            DATABASE(f"update Queue set Duedate = '{DUE_DATE}' ,Holddate = NULL where Barcode == {BOOK[3]} and User_ID == {BORROWER[0]}")
            showinfo("Checkout",f"\nCheckout successfull book {BOOK[3]} is due by {DUE_DATE}.\nYou have 2 renew(s) left for this book")

        else:  # is being renewed
            assert len(QUEUE) == 1,  ERROR(108) # cannot renew book with holds
            assert QUEUE[0][3] <  2 , ERROR(109) # cannot renew book more than twice
            OLD_DATE = DATABASE(f"select Duedate from Queue where Barcode == {BOOK[3]} and User_ID == {BORROWER[0]} ")  # get old date from borrower
            NEW_DATE = (datetime.strptime(OLD_DATE[0][0], "%Y-%m-%d") + timedelta( weeks=3)).date()  # get new date for borrower 3 weeks from old date
            # update borrowewr with new date and increase borrowers renew value
            DATABASE(f"update Queue set Duedate = '{NEW_DATE}' , Renewed = Renewed + 1  where Barcode == {BOOK[3]} and User_ID == {BORROWER[0]} ")
            showinfo("Checkout", f"\nCheckout successfull book {BOOK[3]} has been renewed and is due by {NEW_DATE}. \
                                           \nYou have {2 - (QUEUE[0][3] + 1)} renew(s) left for this book\n")

    else:  # book hasnt been checked out
        DATABASE(f"insert into Queue values({BOOK[3]},{BORROWER[0]},'{DUE_DATE}',0,1,NULL)")
        showinfo("Checkout",
                 f"\nCheckout successfull book {BOOK[3]} is due by {DUE_DATE}.\nYou have 2 renew(s) left for this book\n")

    DATABASE(f"update Books set Status == 0 where Barcode == {BOOK[3]}")  # update status of book for admin purposes




@PAGE_ERROR_HANDLER
def TRANS_RESULTS(BORROWER,text):

        # validate input
        assert '=' in text, ERROR(100)
        text = text.split('=')
        text[0] = text[0].strip().upper()
        assert text[0] in 'CRH', ERROR(100)


        #reformat input for more accurate results
        text[1] = text[1].strip().split()
        text[1] = ''.join(text[1])

        BOOK = DATABASE(f"select * from Books where Barcode == '{text[1]}' ")  # query database for books
        assert BOOK, ERROR(105)  # check if books exits

        QUEUE = DATABASE(f"select * from Queue where Barcode == {BOOK[0][3]} ")  # returns entire queue of the book
        if text[0] == 'C':
            CHECK_OUT_BOOK(BOOK[0], BORROWER[0], QUEUE)

        elif text[0] == 'R':
            RETURN_BOOK(BOOK[0], BORROWER[0], QUEUE)

        elif text[0] == 'H':
            PLACE_HOLD(BOOK[0], BORROWER[0], QUEUE)





@PAGE_ERROR_HANDLER
def ACCOUNT_CREATION(name,email):

        assert all(x.isalpha() or x.isspace() for x in name), ERROR(101)  #invalid name
        assert re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email),ERROR(102)  #regex email validate
        assert email not in (record[0] for record in DATABASE("select Email from Borrowers") + [[None]]),ERROR(103) # if email is taken raise error

        USER_BAR_CODE = GENERATE_BAR_CODE()  # generate a bar code for borrower
        DATABASE(f"insert into Borrowers values({USER_BAR_CODE},'{name}','{email}',0.00)")  # add borrower to database
        showinfo("Account creation", f'\nYour account was successfully created and your ID number is \n{USER_BAR_CODE}')





@PAGE_ERROR_HANDLER
def LOGIN_RESULTS(barcode):
    BORROWER = DATABASE(f"select * from Borrowers where User_ID == '{barcode}'")  # check for account at specific code entered
    assert BORROWER, ERROR(104)
    showinfo("Login results", f"Login successfull welcome back {BORROWER[0][1]}")
    STACK.push(TRANSACTIONS_PAGE(BORROWER))  # if login succesfull load the transactions page




@PAGE_ERROR_HANDLER
def SEARCH_RESULTS(text):
         # validate input
        assert '=' in text,ERROR(100)
        text = text.split('=')
        text[0] = text[0].strip().upper()
        assert text[0] in 'ATS' ,ERROR(100)

        #reformat search for more accurate results
        text[1] = text[1].strip().split()
        text[1] = ' '.join(text[1])

        if text[0] == "A":
            BOOKS = DATABASE(f"select * from Books where Author == '{text[1]}' ")
        elif text[0] == "T":
            BOOKS = DATABASE(f"select * from Books where Title == '{text[1]}' ")
        else:
            BOOKS = DATABASE(f"select * from Books where Subject == '{text[1]}' ")

        assert BOOKS,ERROR(105)

        x = {1: 'Avaliable', 0: 'Unavaliable'}
        # show results to screen using generator
        showinfo("Search Results", ''.join(
                                    [f'\nTitle: {record[0]} \
                                       \nAuthor: {record[1]} \
                                       \nSubject: {record[2]}  \
                                      \nBarcode: {record[3]}   \
                                    \nStatus: {x[record[4]]}\n' \
                                     for record in BOOKS]))











#FRONTEND----------------------------------------------FRONTEND-----------------------------------FRONTEND



class PAGES: #abstract base class for pages to be inherit


    def load(self):  # load the page
        for obj in self.widgets:
            obj.grid(row=self.widgets[obj][0],
                     column=self.widgets[obj][1],
                     padx=self.widgets[obj][2],
                     pady=self.widgets[obj][3] ,
                     columnspan = self.widgets[obj][4])

    def unload(self):  # unload the page
        for obj in self.widgets:
            obj.destroy()

    def Return(self):  # quit program or go back
        STACK.pop()





class Stack:

    def __init__(self,first_page):

        self.stack = [first_page]  #create the stack and initiate the first page
        self.stack[0].load()      #load the first page
        print('Stack:',[str(o) for o in self.stack])

    def push(self,NEXT_PAGE):
        self.stack[-1].unload()   #unload current page
        self.stack.append(NEXT_PAGE)   #add next page to stack
        NEXT_PAGE.load()             #load next page
        print('Stack:',[str(o) for o in self.stack])

    def pop(self):
       self.stack[-1].unload()      #unload current page
       self.stack.pop()             #remove current page from stack
       self.stack[-1] = type(self.stack[-1])() #refresh previous page to be loaded
       self.stack[-1].load()          #load previous page
       print('Stack:',[str(o) for o in self.stack])




class TRANSACTIONS_PAGE(PAGES):

    def __init__(self,BORROWER):
        self.BORROWER = BORROWER  #barcode received from login results

        self.label = Label(text='\n\tEnter "C = barcode" to checkout or renew book\n \
                                \n\tEnter "R = barcode" to return book \n \
                                \n\tEnter "H = barcode" to place hold on a book ' \
                           , font=("arial", 18), justify='left', width=45)
        # store widgets of page and there postions for loading and unloading
        self.entry = Entry(font=("arial", 18), width=20)

        self.button_1 = Button(text="Scan", command=lambda:TRANS_RESULTS(BORROWER,self.entry.get()),
                               font=("arial", 18), fg="blue", bg="snow", width=10)

        self.button_2 = Button(text="Log out", command=self.Return, \
                               fg="red", bg="snow", font=("arial", 18))

        self.widgets = {self.label: [0, 1, None, 10, None],
                        self.entry: [1, 1, None, 1, None],
                        self.button_1: [2, 1, None, 10, None],
                        self.button_2: [3, 0, None, None, None]}


    def __str__(self):
        return 'TRANSACTION_PAGE'






class CREATE_ACCOUNT_PAGE(PAGES):

    def __init__(self):
        #create all widgets of the page and there specifics
        self.label_1  = Label(text = "\t\t To create a free library account  \
                                      \n\t\t please enter your full name and email",
                                      font = ("arial",18),justify = "left" ,width =30)

        self.label_2 = Label(text = "Name:",font = ("arial",18),width = 5)
        self.label_3 =Label(text = "Email:",font = ("arial",18),width = 5)
        self.entry_1 = Entry(font = ("arial",18),width= 20)
        self.entry_2 = Entry(font = ("arial",18),width = 20)

        self.button_1 = Button(text = "Create",command = lambda :ACCOUNT_CREATION(self.entry_1.get(),self.entry_2.get()), \
                             fg = "blue",bg ="snow",font = ("arial",18),width = 15)

        self.button_2 =Button(text = "Return",command = self.Return ,\
                              fg = "red", bg = "snow",font = ("arial",15) )

        # store widgets of page in dictionary for loading and unloading
        self.widgets = {   self.label_1:[0,1,None,10,2] ,
                         self.label_2:[1,1,None,10,None] , self.entry_1:[1,2,None,10,None],
                         self.label_3:[2,1,None,10,None] , self.entry_2:[2,2,None,10,None]
                        ,self.button_1:[3,1,None,5,2] ,self.button_2:[4,0,None,None,None]}




    def __str__(self):
        return "CREATE_ACCOUNT_PAGE"





class LOGIN_ACCOUNT_PAGE(PAGES):


    def __init__(self):
        # create all widgets of the page and there specifics
        self.label = Label(text='\n\tScan the Bar Code found on your ID to login ' \
                           , font=("arial", 17), justify='left', width=30)

        self.entry = Entry(font=("arial", 18), width=20)

        self.button_1 = Button(text="Scan", command = lambda:LOGIN_RESULTS(self.entry.get().strip()),
                               font=("arial", 18), fg="blue", bg="snow", width=10)

        self.button_2 = Button(text="Return", command=self.Return, \
                               fg="red", bg="snow", font=("arial", 18))
        # store widgets of page and there postions for loading and unloading
        self.widgets = { self.label:[0,1,None,10,None] ,
                         self.entry:[1,1,None,1,None] ,
                         self.button_1:[2,1,None,10,None],
                        self.button_2:[3,0,None,None,None] }



    def __str__(self):
         return  'LOGIN_PAGE'





class SEARCH_PAGE(PAGES):

    def __init__(self):
        # create all widgets of the page and there specifics
        self.label = Label(text = '\n\tEnter "A = author name" to search by name\n \
                                  \n\tEnter "T = book title" to search by title\n \
                                  \n\tEnter "S = subject" to search by subject ' \
                                    ,font=("arial",17) , justify = 'left',width = 42)
        # store widgets of page and there postions for loading and unloading
        self.entry = Entry(font = ("arial",18),width = 20)

        self.button_1 = Button(text = "Search",command = lambda :SEARCH_RESULTS(self.entry.get()) ,
                             font = ("arial",18),fg ="blue",bg ="snow",width = 10)

        self.button_2 = Button(text = "Return",command = self.Return, \
                               fg = "red",bg ="snow" ,font = ("arial",18))

        self.widgets = { self.label:[0,1,None,10,None] ,
                         self.entry:[1,1,None,1,None] ,
                         self.button_1:[2,1,None,10,None],
                        self.button_2:[3,0,None,None,None]}


    def __str__(self):
        return "SEARCH_PAGE"






class MAIN_PAGE(PAGES):

    def __init__(self):
         #create all widgets of the page and there specifics
         self.label = Label(TK,text = "Welcome to the CSL library system ",font = ("arial",18))
         self.button_1 = Button(TK,text = "CREATE ACCOUNT",command = self.choice_1,font = ("arial",18),fg ='blue' ,bg ='snow')
         self.button_2 = Button(TK,text = "LOGIN ACCOUNT",command = self.choice_2,font = ("arial",18),fg ='blue' ,bg ='snow')
         self.button_3 = Button(TK,text = "SEARCH BOOKS",command = self.choice_3,font = ("arial",18),fg ='blue' ,bg ='snow')
         self.button_4 = Button(TK,text = "QUIT",command = self.exit,font = ("arial",18) ,fg ='red' ,bg ='snow')
         #store widgets of page and there positions for loading and unloading
         self.widgets = { self.label:[0,1,None,10,None]  ,
                          self.button_1:[1,1,None,10,None]  ,
                         self.button_2:[2,1,None,10,None]  ,
                          self.button_3:[3,1,None,10,None]  ,
                          self.button_4:[4,0,None,None,None] }

   #depeding on button create a instance of page and push in unto the stack
    def choice_1(self):
        STACK.push(CREATE_ACCOUNT_PAGE())

    def choice_2(self):
        STACK.push(LOGIN_ACCOUNT_PAGE())

    def choice_3(self):
        STACK.push(SEARCH_PAGE())


    def exit(self):
        TK.destroy()

    def __str__(self):      #for debugging purposes
        return "MAIN_PAGE"







TK = Tk() #create window and title
TK.title("CSL Library")

# raise fatal error if no more bar codes can be generated for new accounts
assert len(DATABASE("select User_ID from Borrowers")) !=  int('9' + '0' * (BAR_CODE_LENGTH - 1)) , ERROR(200)
# raise fatal error if library has no books in database
assert DATABASE("select * from Books") , ERROR(201)
EXPIRED_HOLDS()  # independent auto service
OVERDUE_BOOKS()  # independent auto service

STACK = Stack(MAIN_PAGE())  # create the history stack to keep track of the current page

mainloop()  #loop window
