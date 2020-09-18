from ArrayStack import ArrayStack

#this function removes 2 values from value stack and one operator from operator ..
#then performs operation with them then push answer unto value stack.
def doOp (valStack, opStack):
    y = valStack.pop ()
    x = valStack.pop ()
    op = opStack.pop ()
    # this checks to see what operation should be done based on operator
    if op == '+':
        valStack.push (x + y)
    elif op == '-':
        valStack.push (x - y)
    else:
        valStack.push (x * y)

#this function returns interger value representing precedence of the operator
def prec (op):
    ops = '*+-$'
    precs = [2,1,1,0]
    return precs [ops.index (op)]

#this function will continualy preform operations as long as value stack has 2 values ...
#and the current token precedence is less than or equal to the top of operator stack precedence
def repeatOps (valStack, opStack, refOp):
    while len (valStack) > 1 and prec (refOp) <= prec (opStack.top ()):
        doOp (valStack, opStack)


def evaluate (expression):
    # create two stacks to hold the interger token and operator tokens
    valStack = ArrayStack()
    opStack = ArrayStack()

    # this for loop iterates over every token in the expression
    for token in expression:

        # if token is a digit push it unto the value stack converted to interger
        if token.isdigit():
            valStack.push(int(token))

        # if token is a operator call the repeatop function to perform a operation if possible ...
        # ... then push the operator unto the operator stack
        else:
            repeatOps(valStack,opStack,token)
            opStack.push(token)

    # call the repeatops function to push end token and preform any remaining operations
    repeatOps(valStack,opStack,'$')

    # return the final answer from value stack
    return valStack.pop()
