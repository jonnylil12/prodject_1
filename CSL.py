import sqlite3
import re
from datetime import date , timedelta ,datetime

BAR_CODE_LENGTH = 7  # for easier admin debugging manually set the length of user bar codes


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
                 # 100+    == system errors
                 # 200+   ==  system errors
    CODES = {

    100:' Please enter a valid command'    ,                    110:' Book is currently unavailable to checkout' ,
    101: ' Please enter valid name characters and spaces only', 111:' Cannot renew book more than twice ',
    102: ' Please enter a valid email address ',                113:' Book cannot be renewed hold has been placed',
    103: ' Please enter a valid age',                           114:' Borrower has not checked out this book' ,
    104: ' Minors are ineligable for adult library card',       115:' Book is avaliable to be checked out ' ,
    105: ' Please enter a valid home address  ',                116:' Borrower has already checked out this book' ,
    106: ' Email address already exists',                       117:' Borrower already has hold for this book ' ,
    107: ' Account not found',
    108: ' Book(s) not found',                                  200:' Bar Code generator has reached max capacity' ,
    109: ' Balance greater than $5.00 ' ,                       201:' There are no books available in the system '

    }
    if code < 200:
            print(f'\nUSER ERROR {code}: {CODES[code]}\n')  #return specific exception message with code
    else:
            print(f'\nSYSTEM ERROR {code}: {CODES[code]}\n')



def GENERATE_BAR_CODE():
    ALL_USER_BAR_CODES = DATABASE("select ID from Borrowers")
    if ALL_USER_BAR_CODES  :                    #checks if there is no user bar codes in the database
        return ALL_USER_BAR_CODES[-1][0] + 1
    return   int('1' + '0' *( BAR_CODE_LENGTH - 1))                            # formula to find smallet bar code of specific length



def PLACE_HOLD(BOOK,BORROWER,QUEUE):
    assert len(QUEUE) , ERROR(115)  #book isnt checked out
    HOLDERS = [x[0] for x in DATABASE(f"select User_ID from Queue where Barcode == {BOOK[3]}")]
    assert not QUEUE[0][2], ERROR(116)  # borrower cant place hold on book he has
    assert BORROWER[0] not in HOLDERS , ERROR(117)   #borrower already has hold on book
    DATABASE(f"insert into Queue values({BOOK[3]},{BORROWER[0]},NULL,0,{len(QUEUE) + 1},NUll)")
    print(f"\nHold has succesfully been placed \nand will expire one week after book has been returned \n")



def RETURN_BOOK(BOOK,BORROWER,QUEUE):
    assert QUEUE[0][1] == BORROWER[0] and QUEUE[0][2], ERROR(114)  #borrower didnt check out book
    DATABASE(f"delete from Queue where Barcode == {BOOK[3]} and User_ID == {BORROWER[0]}")  #remove borrower from queue
    DATABASE(f"update Queue set Queue_ID = Queue_ID - 1 where Barcode == {BOOK[3]}")  #update the queue

    if QUEUE: # if the queue still exits
        #get and set hold expire date for next borrower
        HOLD_DATE = date.today() + timedelta(weeks=1)
        DATABASE(f"update Queue set Holddate  = '{HOLD_DATE}' where Barcode == {BOOK[3]} and Queue_ID = 1")

    DATABASE(f"update Books set Status == 1 where Barcode == {BOOK[3]}")  # update status of book for admin purpose
    print("\nBook succefully returned thank you for your buisness\n")



def CHECK_OUT_BOOK(BOOK,BORROWER,QUEUE):
    DUE_DATE = date.today() + timedelta(weeks=3)  # get the date 3 weeks from today

    assert BORROWER[5] <= 5.00 ,ERROR(109)         #check if balance requirment is met
    if QUEUE:  # book has been checkout or has holds
        assert QUEUE[0][1] == BORROWER[0], ERROR(110)  # book is unavaliable to borrower

        if QUEUE[0][5]:  # book has hold
            DATABASE(f"update Queue set Duedate = '{DUE_DATE}' ,Holddate = NULL where Barcode == {BOOK[3]} and User_ID == {BORROWER[0]}")
            print(f"\nCheckout successfull book {BOOK[3]} is due by {DUE_DATE}.\nYou have 2 renew(s) left for this book\n")

        else:  # book has been checkout and is being renewed
            assert len(QUEUE) == 1, ERROR(113)  # cannot renew book with holds
            assert QUEUE[0][3] < 2, ERROR(111)  # cannot renew book more than twice

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

    assert BORROWER, ERROR(107)  # error code for account not found

    print(f"\nLogin succesfull welcome back {BORROWER[0][1]}")

    choice = input("\nEnter 'C= barcode' to checkout book  \
                    \nEnter 'R= barcode' to return book   \
                    \nEnter 'H= barcode' to place hold on a book \
                    \n: ")

    command, barcode = choice[:2], choice[2:].strip()
    assert command in 'C=R=H=' and command !='',ERROR(100)  #uinvalid command

    BOOK = DATABASE(f"select * from Books where Barcode == '{barcode}' ")  # query database for book
    assert BOOK, ERROR(108)  # book not found

    QUEUE = DATABASE(f"select * from Queue where Barcode == {BOOK[0][3]} ")# returns entire queue of the book

    if command == 'C=':
        CHECK_OUT_BOOK(BOOK[0], BORROWER[0], QUEUE)

    elif command == 'R=':
        RETURN_BOOK(BOOK[0], BORROWER[0], QUEUE)

    elif command == 'H=':
        PLACE_HOLD(BOOK[0], BORROWER[0], QUEUE)



@PAGE_ERROR_HANDLER
def CREATE_ACCOUNT_PAGE():
    print("\nTo create a free library account please enter your name , home address ,age  and valid email. \
          \nMinors under the age of 16 are inelible for adult cards \
          \nA unique Bar code will then be generated for you\n ")

    TAKEN_EMAILS =  DATABASE("select Email from Borrowers")

    name = input('Enter your full first and last name\n: ')
    age = input('Enter your age\n: ')
    address = input('Enter your full address in street,city,state,zip code format\n:  ')
    email = input('Enter your email address\n: ')

    assert all(x.isalpha() or x.isspace() for x in name), ERROR(101)
    assert re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email), ERROR(102)  # regex email validate

    assert age.isdigit(), ERROR(103)
    assert int(age) >= 16, ERROR(104)
    assert address.count(',') == 3, ERROR(105)  # validate name address and age
    if not TAKEN_EMAILS:
      assert email not in (x[0] for x in TAKEN_EMAILS), ERROR(106)

    USER_BAR_CODE = GENERATE_BAR_CODE()  # generate a bar code for borrower
    DATABASE(f"insert into Borrowers values({USER_BAR_CODE},'{name}','{email}',{age},'{address}',0.00)")  # add borrower to database
    print(f'\nYour account was successfully created and your ID number is \n{USER_BAR_CODE}\n')




@PAGE_ERROR_HANDLER
def SEARCH_PAGE():

    choice = input("\nEnter 'A= author' to search by authors name \
                    \nEnter 'T= title' to search by book title \
                    \nEnter 'S= subject' to search by subject area \
                    \n: ")

    command, selection = choice[:2], choice[2:].strip()             #split the entry into the command and selection for verification

    if command == 'A=':
        BOOKS = DATABASE(f"select * from Books where Author == '{selection}' ")
    elif command == 'T=':
        BOOKS = DATABASE(f"select * from Books where Title == '{selection}' ")
    elif command == 'S=':
        BOOKS = DATABASE(f"select * from Books where Subject == '{selection}' ")
    else:
        raise ERROR(100)    #invalid command

    assert BOOKS, ERROR(108)    #checks if books where found

    x = {1:'Avaliable' , 0:'Unavaliable'}
    for book in BOOKS:
        print(f'Title: {book[0]} \
              \nAuthor: {book[1]} \
              \nSubject: {book[2]}  \
              \nBarcode: {book[3]}   \
              \nStatus: {x[book[4]]} \n')


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

try:
    MAIN_PAGE()   #run program and handle fatal errors
except:
    pass