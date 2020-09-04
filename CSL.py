import sqlite3
import re

class Database:

    def __init__(self):
        self.file = sqlite3.connect('database.db')          #database object class establise a connection
        self.cursor  = self.file.cursor()

    def query(self,query):                               #runs querys and return data if applicable
        self.cursor.execute(query)
        self.file.commit()
        return self.cursor.fetchall()

    def close(self):
        self.file.close()

DB = Database()         #create connection of main database






class Error(Exception):

    codes = {100:' Please specify a command ' ,           # Specific error codes for easier debugging
             101:' Please enter a valid command' ,

             102:' Please specify your name',                           # 100+    == user errors
             103:' Please specify a email addresss ',
             104:' Please specify your age'     ,
             105:' Please specify your address' ,

             106:' Name must contain only characters and spaces' ,                          # 200+    == system errors
             107:' Please enter a valid email address ' ,
             108:' Email address already exists',
             109:' Please enter a valid age' ,
             110:' Minors are ineligable for adult library card' ,
             111:' Please enter a valid home address  ' ,
             112:' Account not found' ,
             113:' Book not found' ,


             200:' Database Bar Code generator has reached max capacity  \
                  \nAdmin must increase length to generate new bar codes'}

    def __init__(self,code):
        self.code = code          #error code saved when other code raises a error

    def __str__(self):
        if self.code < 200:
            return f'USER ERROR {self.code}:{Error.codes[self.code]}'
        else:                               #return specific exception message with code
            return f'SYSTEM ERROR {self.code}:{Error.codes[self.code]}'






def CHECK_OUT_PAGE(Borrower):
    print(f'\nWelcome back {Borrower[1]}!')
    print('Command C = checkout  , Command R = return\n')
    DONE = False
    while not DONE:
        book = input('Enter the books bar code: ')
        command = input('Enter a command: ')
        ALL_BOOK_BAR_CODES_ = [x[0] for x in DB.query('select Bar_Code from Books')]  #query database for all book bar codes
        try:
            assert book in  ALL_BOOK_BAR_CODES_, Error(113)






def generate_bar_code():
    BAR_CODE_LENGTH = 1          #for easier admin debugging manually set the length of user bar codes

    ALL_USER_BAR_CODES = DB.query("select ID from Borrowers")

    assert len(ALL_USER_BAR_CODES) != 10 ** BAR_CODE_LENGTH, Error(200)  # this checks if all possible code combinations have been saved

    if ALL_USER_BAR_CODES  :                    #checks if there is no user bar codes in the database
        return ALL_USER_BAR_CODES[-1][0] + 1

    return 40 * BAR_CODE_LENGTH ** 2 - 110 * BAR_CODE_LENGTH + 70  # formula to find smallet bar code of specific length









def CREATE_ACCOUNT_PAGE():
    print("\nTo create a free library account please enter your name , home address ,age  and valid email. \
          \nMinors under the age of 16 are inelible for adult cards \
          \nA unique Bar code will then be generated for you\n ")

    taken_emails = DB.query("select Email from Borrowers")
    name = input('Enter your full first and last name: ')
    email = input('Enter your email address: ')
    age = input('Enter your age: ')
    address = input('Enter your full address in street,city,state,zip code format:  ')
    try:
        assert name , Error(102)                     #make sure no fields left blank
        assert email , Error(103)
        assert age , Error(104)
        assert address,  Error(105)

        assert all(x.isalpha() or x.isspace() for x in name) ,Error(106)
        assert re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email) , Error(107)       #regex email validate
        assert email not in (x[0] for x in taken_emails ), Error(108)
        assert age.isdigit() , Error(109)
        assert int(age) >= 16, Error(110)
        assert address.count(',') == 3 , Error(111)                 #validate name address and age


    except Exception as e:                                          #back button for main menu or try again
        print(f'\n{e}')

        if input('Enter 0 to go to main menu: ') != '0':
             return CREATE_ACCOUNT_PAGE()
        return True

    else:
        USER_BAR_CODE = generate_bar_code()             #generate a bar code for borrower
        DB.query(f"insert into Borrowers values({USER_BAR_CODE},'{name}', \
                                            '{email}',{age},'{address}',0.00)")       #add borrower to database
        print(f'\nYour account was successfully created and your bar code is \n{USER_BAR_CODE}\n')
        return True








def LOGIN__ACCOUNT_PAGE():
                                                                       #login page to access account
    BAR_CODE = input('\nEnter your Bar Code found on your ID: ')

    Borrower = DB.query(f"select * from Borrowers where ID in ({BAR_CODE})")[0]                                                #check for account at specific code entered

    try:
        assert Borrower , Error(112)            #error code for account not found

    except Exception as e:
        print(f'\n{e}')

        if input('Enter 0 to go to main menu: ') != '0':            #back button for main menu or try again
            return LOGIN__ACCOUNT_PAGE()
        return True

    else:
        return CHECK_OUT_PAGE(Borrower)





def SEARCH_PAGE():
    print("\nWelcome to the search database")

    choice = input("Enter 'A= author' to search by authors name \
                            \nEnter 'T= title' to search by book title \
                            \nEnter 'S= subject' to search by subject area \
                            \n: ")

    command, selection = choice[:2], choice[2:].strip()             #split the entry into the command and selection for verification

    x = {'A=': 'Author', 'T=': 'Title', 'S=': 'Subject'}

    Books = DB.query(f"select * from Books where {x[command]} == '{selection}' ")   #find books are those parameters

    try:
        assert command in 'A=T=S=', Error(101)      #verify command

    except Exception as e:
        print(f'\n{e}')
        if input('Enter 0 to go to main menu: ') != '0':         # back button for main menu or try again
            return SEARCH_PAGE()
        return True

    else:

        if Books:                 # if books where found return them
            for book in Books:
                print(f'Title: {book[0]} , Author: {book[1]} , \
                      \nSubject: {book[2]} , Bar Code: {book[3]}\n')
        else:
            print('No books found')

        return True







def MAIN_PAGE():

    while (CSL_ACTIVE:=True):           #CSL program is running

        choice = input("Welcome to the CSL library system ! \
                           \nHere you can check in and out books or Search for books \
                           \nEnter 1 to create a new account  \
                           \nEnter 2 for log into your account \
                           \nEnter 3 to search the database for books \
                           \nPress 0 to quit \
                           \n: ")
        try:
            assert choice, Error(100)
            assert choice in '0123' , Error(101)

            if choice == '1':

                CSL_ACTIVE = CREATE_ACCOUNT_PAGE()  # next pages depeding on choice

            elif choice == '2':
                CSL_ACTIVE = LOGIN__ACCOUNT_PAGE()

            elif choice == '3':
                CSL_ACTIVE = SEARCH_PAGE()

            else:
                DB.close()
                break

        except Exception as e:
            print(f'\n{e}\n')


MAIN_PAGE()