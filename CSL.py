import sqlite3
import re
from datetime import date , timedelta ,datetime

BAR_CODE_LENGTH = 7  # fset the length of user bar codes


def DATABASE(query):
    with sqlite3.connect('database.db') as file:
        cursor = file.cursor()            #create connection of main database and submits querys to database
        cursor.execute(query)
        file.commit()
        result = cursor.fetchall()
    return result


def PAGE_ERROR_HANDLER(PAGE):       #decorator that wraps functions with a error catcher
   def OVERRIDED_FUNC():       #accepts parameters if overriden function has them
        try:
            PAGE()     #will return values if ovverriden function returns values
        except:
            if input(f'Enter 0 to return to main menu \
                    \nor any key to try again: ') != '0':
                OVERRIDED_FUNC()
   return OVERRIDED_FUNC



def ERROR(code):


    CODES = {
    # 100+    == system errors
    100: ' Invalid command'    ,                                107:' Book is currently unavailable to checkout' ,
    101: ' Ivalid name characters and spaces only',             108:' Book cannot be renewed hold has been placed' ,
    102: ' Ivalid email address ',                              109:'  Cannot renew book more than twice ',
    103: ' Email address already exists',                       110:' Borrower has not checked out this book' ,
    104: ' Account not found',                                  111:' Book is avaliable to be checked out ' ,
    105: ' Book(s) not found',                                  112:' Borrower has already checked out this book' ,
    106: ' Balance greater than $5.00 ',                        113:' Borrower already has hold for this book ' ,
    # 200+   ==  system errors
    200:' Bar Code generator has reached max capacity' ,
    201:' There are no books available in the system '

    }
    if code < 200:
            print(f'\nUSER ERROR {code}: {CODES[code]}\n')  #return specific exception message with code
    else:
            print(f'\nSYSTEM ERROR {code}: {CODES[code]}\n')



def GENERATE_BAR_CODE():
    ALL_USER_BAR_CODES = DATABASE("select User_ID from Borrowers")
    if ALL_USER_BAR_CODES  :                    #checks if there is no user bar codes in the database
        return ALL_USER_BAR_CODES[-1][0] + 1
    return   int('1' + '0' *( BAR_CODE_LENGTH - 1))    # formula to find smallet bar code of specific length



def PLACE_HOLD(BOOK,BORROWER,QUEUE):
    assert QUEUE , ERROR(111)  #book isnt checked out
    HOLDERS = [x[0] for x in DATABASE(f"select User_ID from Queue where Barcode == {BOOK[3]}")]
    assert BORROWER[0] != QUEUE[0][1] and not QUEUE[0][2], ERROR(112)  # borrower cant place hold on book he has
    assert BORROWER[0] not in HOLDERS , ERROR(113)   #borrower already has hold on book
    DATABASE(f"insert into Queue values({BOOK[3]},{BORROWER[0]},NULL,0,{len(QUEUE) + 1},NUll)")
    print(f"\nHold has succesfully been placed \nand will expire one week after book has been returned \n")



def RETURN_BOOK(BOOK,BORROWER,QUEUE):
    assert QUEUE , ERROR(110)  #no one has check out book
    assert QUEUE[0][1] == BORROWER[0] and QUEUE[0][2], ERROR(110)  #borrower didnt check out book
    DATABASE(f"delete from Queue where Barcode == {BOOK[3]} and User_ID == {BORROWER[0]}")  #remove borrower from queue
    DATABASE(f"update Queue set Queue_ID = Queue_ID - 1 where Barcode == {BOOK[3]}")  #update the queue
    # give holdate to next person in line for one week if there is a queue
    HOLD_DATE = date.today() + timedelta(weeks=1)
    DATABASE(f"update Queue set Holddate  = '{HOLD_DATE}' where Barcode == {BOOK[3]} and Queue_ID = 1")


    DATABASE(f"update Books set Status == 1 where Barcode == {BOOK[3]}")  # update status of book for admin purpose
    print("\nBook succefully returned thank you for your buisness\n")



def CHECK_OUT_BOOK(BOOK,BORROWER,QUEUE):
    DUE_DATE = date.today() + timedelta(weeks=3)  # get the date 3 weeks from today

    assert BORROWER[3] <= 5.00 ,ERROR(106)         #check if balance requirment is met
    if QUEUE:  # book has been checkout or has holds
        assert QUEUE[0][1] == BORROWER[0], ERROR(107)  # book is unavaliable to borrower

        if QUEUE[0][5]:  # book has hold
            DATABASE(f"update Queue set Duedate = '{DUE_DATE}' ,Holddate = NULL where Barcode == {BOOK[3]} and User_ID == {BORROWER[0]}")
            print(f"\nCheckout successfull book {BOOK[3]} is due by {DUE_DATE}.\nYou have 2 renew(s) left for this book\n")

        else:  # book has been checkout and is being renewed
            assert len(QUEUE) == 1, ERROR(108)  # cannot renew book with holds
            assert QUEUE[0][3] < 2, ERROR(109)  # cannot renew book more than twice

            OLD_DATE = DATABASE(f"select Duedate from Queue where Barcode == {BOOK[3]} and User_ID == {BORROWER[0]} ")  # get old date from borrower
            NEW_DATE = (datetime.strptime(OLD_DATE[0][0], "%Y-%m-%d") + timedelta(weeks=3)).date()  # get new date for borrower 3 weeks from old date
            # update borrowewr with new date and increase borrowers renew value
            DATABASE(f"update Queue set Duedate = '{NEW_DATE}' , Renewed = Renewed + 1  where Barcode == {BOOK[3]} and User_ID == {BORROWER[0]} ")
            print(f"\nCheckout successfull book {BOOK[3]} has been renewed and is due by {NEW_DATE}. \
                    \nYou have {2 - (QUEUE[0][3] + 1)} renew(s) left for this book\n")

    else:   # book hasnt been checked out
           DATABASE(f"insert into Queue values({BOOK[3]},{BORROWER[0]},'{DUE_DATE}',0,1,NULL)")
           print(f"\nCheckout successfull book {BOOK[3]} is due by {DUE_DATE}.\nYou have 2 renew(s) left for this book\n")

    DATABASE(f"update Books set Status == 0 where Barcode == {BOOK[3]}") # update status of book for admin purposes



@PAGE_ERROR_HANDLER
def TRANSACTIONS_PAGE():

    ID_number = input('\nScan the Bar Code found on your ID to login\n: ').strip()
    BORROWER = DATABASE(f"select * from Borrowers where User_ID == {ID_number}")  # check for account at specific code entered

    assert BORROWER, ERROR(104)  # error code for account not found

    choice = input("\nEnter 'C= barcode' to checkout or renew book  \
                    \nEnter 'R= barcode' to return book   \
                    \nEnter 'H= barcode' to place hold on a book \
                    \n: ").split()

    BOOK = DATABASE(f"select * from Books where Barcode == '{choice[1]}' ")# query database for book

    assert len(choice) == 2 , ERROR(100)     #invalid input
    assert choice[0] in 'C=R=H=' ,ERROR(100)
    assert BOOK,  ERROR(105)  # query database for book

    QUEUE = DATABASE(f"select * from Queue where Barcode == {BOOK[0][3]} ")# returns entire queue of the book

    if choice[0] == 'C=':
        CHECK_OUT_BOOK(BOOK[0], BORROWER[0], QUEUE)

    elif choice[0] == 'R=':
        RETURN_BOOK(BOOK[0], BORROWER[0], QUEUE)

    elif choice[0] == 'H=':
        PLACE_HOLD(BOOK[0], BORROWER[0], QUEUE)



@PAGE_ERROR_HANDLER
def CREATE_ACCOUNT_PAGE():

    TAKEN_EMAILS =  DATABASE("select Email from Borrowers")

    name = input('\nEnter your full first and last namen\n: ')
    email = input('Enter your email address\n: ')

    assert all(x.isalpha() or x.isspace() for x in name), ERROR(101)
    assert re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email), ERROR(102)  # regex email validate

    if TAKEN_EMAILS:
      assert email not in (x[0] for x in TAKEN_EMAILS), ERROR(103)  #email address already taken

    USER_BAR_CODE = GENERATE_BAR_CODE()  # generate a bar code for borrower
    DATABASE(f"insert into Borrowers values({USER_BAR_CODE},'{name}','{email}',0.00)")  # add borrower to database
    print(f'\nYour account was successfully created and your ID number is \n{USER_BAR_CODE}\n')




@PAGE_ERROR_HANDLER
def SEARCH_PAGE():

    choice = input("\nEnter 'A= author' to search by authors name \
                    \nEnter 'T= title' to search by book title \
                    \nEnter 'S= subject' to search by subject area \
                    \n: ").split()

    assert len(choice) > 1 and choice[0] in 'A=T=S=' ,ERROR(100)

    if choice[0] == 'A=':
        BOOKS = DATABASE(f"select * from Books where Author == '{''.join(choice[1:])}' ")
    elif choice[0] == 'T=':
        BOOKS = DATABASE(f"select * from Books where Title == '{''.join(choice[1:])}' ")
    else:
        BOOKS = DATABASE(f"select * from Books where Subject == '{''.join(choice[1:])}' ")

    assert BOOKS, ERROR(105)    #checks if books where found
    x = {1: 'Avaliable', 0: 'Unavaliable'}
    for record in BOOKS:
        print(f'Title: {record[0]} \
                      \nAuthor: {record[1]} \
                      \nSubject: {record[2]}  \
                      \nBarcode: {record[3]}   \
                      \nStatus: {x[record[4]]} \n')




def EXPIRED_HOLDS():
    for record in DATABASE("select * from Queue where Holddate"):
        if  date.today() == datetime.strptime(record[5],"%Y-%m-%d").date() :  #check if hold has expired
            #remove hold from queue and update queue
            DATABASE(f"delete from Queue where Barcode == {record[0]} and User_ID == {record[1]}")
            DATABASE(f"update Queue set Queue_ID = Queue_ID - 1 where Barcode == {record[0]}")
            #gret and set hold date for next in queue
            HOLD_DATE = date.today() + timedelta(weeks=1)
            DATABASE(f"update Queue set Holddate = '{HOLD_DATE}' where Barcode == {record[0]} and Queue_ID = 1")

            # todo alert user that there hold has expired by email


def OVERDUE_BOOKS():
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




def MAIN_PAGE():

    # raise fatal error if no more bar codes can be generated for new accounts
    assert len(DATABASE("select User_ID from Borrowers")) != int('9' + '0' * (BAR_CODE_LENGTH - 1)), ERROR(200)

    # raise fatal error if library has no books in database
    assert DATABASE("select * from Books"), ERROR(201)

    while True:           #main LCS program running
        choice = input("Welcome to the CSL library system ! \
                        \nEnter 1 to create a new account  \
                        \nEnter 2 for log into your account \
                        \nEnter 3 to search the database for books \
                        \nPress 0 to quit \
                        \n: ")

        if choice == '1':
            CREATE_ACCOUNT_PAGE()

        elif choice == '2':
            TRANSACTIONS_PAGE()

        elif choice == '3':
            SEARCH_PAGE()

        elif choice == '0':
            break

        else:
            ERROR(100)


EXPIRED_HOLDS() #auto remove expired holds
OVERDUE_BOOKS() #add fines to overdue books
MAIN_PAGE()    #run program and handle fatal errors

