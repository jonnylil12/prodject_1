import sqlite3
import re
from datetime import date , timedelta ,datetime


def DATABASE(query):
    with sqlite3.connect('database.db') as file:
        cursor = file.cursor()                          #create connection of main database and submits querys to database
        cursor.execute(query)
        file.commit()
        result = cursor.fetchall()
    return result




def PAGE_ERROR_HANDLER(PAGE):       #decorator that wraps functions with a error catcher

   def OVERRIDED_FUNC(*data):       #accepts parameters if overriden function has them
        try:
            return PAGE(*data)     #will return values if ovverriden function returns values
        except Exception:
            if input(f'Enter 0 to return to previous page\nEnter any key to try again: ') != '0':
                OVERRIDED_FUNC(*data)

   return OVERRIDED_FUNC



def ERROR(code):
                 # 100+    == system errors

    CODES = {    100:' Please enter a valid command'    ,
                #create account page codes
                 101:' Please enter valid name characters and spaces only' ,
                 102:' Please enter a valid email address ' ,
                 103:' Please enter a valid age' ,
                 104:' Minors are ineligable for adult library card' ,
                 105:' Please enter a valid home address  ' ,
                 106:' Email address already exists',
                #login page codes
                 107:' Account not found' ,
                #search page codes
                 108:' Book(s) not found' ,
                #check out page codes
                 109:' Balance greater than $5.00 ' ,
                 110:' Book is currently unavailable to checkout' ,
                 111:' Cannot renew book more than twice ',
                 112:' Borrower not next in Queue for this book ' ,
                 113:' Book cannot be renewed hold has been placed',
                 #return page codes
                 114:' Borrower has not checked out this book' ,


                # 200+    == system errors
                 200:' Account creation failed Bar Code generator has reached max capacity' ,
                 201:' There are no books available in the system at this moment check back later'}

                                                          #error code saved when other code raises a error

    if code < 200:
            print(f'\nUSER ERROR {code}: {CODES[code]}\n')
    else:                                                 #return specific exception message with code
            print(f'\nSYSTEM ERROR {code}: {CODES[code]}\n')




@PAGE_ERROR_HANDLER
def GENERATE_BAR_CODE():
    BAR_CODE_LENGTH = 7          #for easier admin debugging manually set the length of user bar codes

    ALL_USER_BAR_CODES = DATABASE("select ID from Borrowers")

    assert len(ALL_USER_BAR_CODES) != int('9' + '0' * ( BAR_CODE_LENGTH - 1)) , ERROR(200)    # this checks if all possible code combinations have been saved

    if ALL_USER_BAR_CODES  :                    #checks if there is no user bar codes in the database
        return ALL_USER_BAR_CODES[-1][0] + 1

    return   int('1' + '0' *( BAR_CODE_LENGTH - 1))                            # formula to find smallet bar code of specific length


def PLACE_HOLD(BOOK,BORROWER,QUEUE):
    pass

@PAGE_ERROR_HANDLER
def RETURN_BOOK(BOOK,BORROWER,QUEUE):
    assert QUEUE[1] == BORROWER[0], ERROR(114)
    DATABASE(f"delete from Queue where Book_Bar_Code == {BOOK[3]} and User_ID == {BORROWER[0]}")
    DATABASE(f"update Books set Status == 1 where Barcode == {BOOK[3]}") # update status of book for admin purposes
    print("Book succefully returned thank you for your buisness")


def CHECK_OUT_BOOK(BOOK,BORROWER,QUEUE):
    assert BORROWER[5] <= 5.00 ,ERROR(109)         #check if balance requirment is met

    if len(QUEUE) == 1:   #book has been checked out  this statement also lets borrowers renew books
        assert QUEUE[1] == BORROWER[0] , ERROR(110)  #book is already checked out
        assert QUEUE[3] < 2, ERROR(111)  # cannot renew book more than twice

        #get old date from borrower
        OLD_DATE = DATABASE(f"select Duedate from Queue where Book_Bar_Code == {BOOK[3]} and User_ID == {BORROWER[0]} ")
        # get new date for borrower 3 weeks from old date
        NEW_DATE = ( datetime.strptime(OLD_DATE[0][0],"%Y-%m-%d") + timedelta(weeks=3) ).date()
        #update borrowewr with new date
        DATABASE(f"update Queue set Duedate = '{NEW_DATE}' where Book_Bar_Code == {BOOK[3]} and User_ID == {BORROWER[0]} ")
        #increase the borrowers renews
        DATABASE(f"update Queue set Renewed = Renewed + 1 where Book_Bar_Code == {BOOK[3]} and User_ID == {BORROWER[0]} ")

        print(f"\nCheckout successfull book {BOOK[3]} is due by {NEW_DATE}\nYou have {2 - (QUEUE[3]+1)} renews left for this book")

    elif len(QUEUE) > 1:   #book has holds
        assert QUEUE[1] == BORROWER[0], ERROR(112)  #borrower is not next in line
        assert QUEUE[2] == 'HOLD' ,ERROR(113)     #cannot renew book with holds

        DUE_DATE = date.today() + timedelta(weeks=3)  # get the date 3 weeks from today
        DATABASE(f"update Queue set Duedate = '{DUE_DATE}' where Book_Bar_Code == {BOOK[3]} and User_ID == {BORROWER[0]} ")
        print(f"\nCheckout successfull book {BOOK[3]} in due by {DUE_DATE}")

    else:   # book hasnt been checked out
        DUE_DATE = date.today() + timedelta(weeks=3)  # get the date 3 weeks from today
        DATABASE(f"insert into Queue values({BOOK[3]},{BORROWER[0]},'{DUE_DATE}',0)")
        print(f"\nCheckout successfull book {BOOK[3]} in due by {DUE_DATE}\nyou have 2 renews left for this book")
        #1 means avalible 0 means unavailable

    DATABASE(f"update Books set Status == 0 where Barcode == {BOOK[3]}")
    # update status of book for admin purposes


@PAGE_ERROR_HANDLER
def TRANSACTIONS_PAGE(BORROWER):

    choice = input("\nEnter 'C= barcode' to checkout book  \
                    \nEnter 'R= barcode' to return book   \
                    \nEnter 'H= barcode' to place hold on a book \
                    \n: ")

    command, barcode = choice[:2], choice[2:].strip()
    assert command in 'C=R=H=' and command !='',ERROR(100)

    BOOK = DATABASE(f"select * from Books where Barcode == '{barcode}' ")  # query database for book
    assert BOOK, ERROR(108)  # book not found

    QUEUE = DATABASE(f"select * from Queue where Book_Bar_Code == {BOOK[0][3]} ")# returns entire queue of the book

    if command == 'C=':
        CHECK_OUT_BOOK(BOOK[0], BORROWER, QUEUE[0])

    elif command == 'R=':
        RETURN_BOOK(BOOK[0], BORROWER, QUEUE[0])

    elif command == 'H=':
        PLACE_HOLD(BOOK[0], BORROWER, QUEUE)








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
    print(f'\nYour account was successfully created and your bar code is \n{USER_BAR_CODE}\n')



@PAGE_ERROR_HANDLER
def LOGIN_ACCOUNT_PAGE():
        assert (BOOKS := DATABASE("select * from Books")), ERROR(201) #check if the book database is empty if so raise system error
        ID_number = input('\nScan the Bar Code found on your ID to login\n: ').strip()

        BORROWER = DATABASE(f"select * from Borrowers where ID == {ID_number}")             #check for account at specific code entered

        assert BORROWER , ERROR(107)             # error code for account not found

        print(f"\nLogin succesfull welcome back {BORROWER[0][1]}")

        TRANSACTIONS_PAGE(BORROWER[0])





@PAGE_ERROR_HANDLER
def SEARCH_PAGE():

    assert (BOOKS:=DATABASE("select * from Books")) , ERROR(201)    #check if the book database is empty if so raise system error

    choice = input("\nEnter 'A= author' to search by authors name \
                    \nEnter 'T= title' to search by book title \
                    \nEnter 'S= subject' to search by subject area \
                    \nEnter 0 to show all Books \
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
    for book in BOOKS:
        print(f'Title: {book[0]} , Author: {book[1]} , \
             \nSubject: {book[2]} , Bar Code: {book[3]}\n')  # if books where found return them







def MAIN_PAGE():

    while True:           #main LCS program running
        choice = input("\nWelcome to the CSL library system ! \
                           \nEnter 1 to create a new account  \
                           \nEnter 2 for log into your account \
                           \nEnter 3 to search the database for books \
                           \nPress 0 to quit \
                           \n: ")



        if choice == '1':

            CREATE_ACCOUNT_PAGE()               # next pages depeding on choice

        elif choice == '2':
            LOGIN_ACCOUNT_PAGE()

        elif choice == '3':
            SEARCH_PAGE()

        elif choice == '0':
            break

        else:
            ERROR(100)


MAIN_PAGE()



