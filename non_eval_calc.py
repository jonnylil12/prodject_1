precedence = { '+':1 , '-':1 ,'*':2 , '/':2 , '//':2 ,'%':2 ,'**':3}

def solver(x,y,z):
    if y == '+':
        return float(x) + float(z)
    elif y == '-':
        return float(x) - float(z)
    elif y == '/':
        return float(x) / float(z)
    elif y == '*':
        return float(x) * float(z)
    elif y == '%':
        return float(x) % float(z)
    elif y == '**':
        return float(x) ** float(z)
    elif y == '//':
        return float(x) // float(z)


def grouper(express):
    box ,pair ,FLAG = [] ,'' ,False
    for value in express + '!':
        if value.isdigit() or value == '.':
            pair += value
        elif value in '*/' and FLAG and pair[-2] in '*/':
            pair = pair.rstrip() + value + ' '
        elif value in '+-*/%!' and  not FLAG:
            pair += f' {value} '
            FLAG = True
        elif value in '+-*/%!' and FLAG:
            pair = pair.split()
            box.append([pair[0], pair[1], pair[2]])
            pair = f'{pair[2]} {value} '
    return box




def calculator(box):
    solution = first = location = None
    while box:
         #return solution and location
        solution = solver(*max(box, key = lambda x :precedence[x[1]]))
        location = box.index(max(box, key = lambda x :precedence[x[1]]))
            # if only one pair exists in expression
        if len(box) == 1:
            del box[location]
            # if pair at beginning of expression
        elif location == 0 and len(box) > 1:
            box[location + 1][0] = solution
            del box[location]
            #if pair at the end of expression
        elif location == len(box) - 1 and len(box) > 1:
            box[location - 1][2] = solution
            del box[location]
            #if pair somewhere in middle of expression
        else:
            box[location - 1][2] = solution
            box[location + 1][0] = solution
            del box[location]
    return solution


def not_valid(express):
    #checks for only valid characters
    if not all(x.isdigit() or x.isspace() or x in '+-/*%.' for x in express):
        return True
    #checks for charaters in right order
    express = ' ' + express + ' '
    FLAG = 0
    for k in range(len(express)):
        if express[k] in '+-/*%' and (express[:k].isspace() or  express[k+1:].isspace()):
             return True
        elif express[k].isdigit() or express[k] =='.':
             FLAG = 0
        elif express[k] in '+-/*%':
             FLAG += 1
             if FLAG > 2:
                 return True
             elif FLAG == 2:
                 if (express[k] == '*' and express[k - 1] == '*') or \
                        (express[k] == '/' and express[k - 1] == '/') or \
                        express[k] == ' ':
                    pass
                 else:
                    return True
    return False


def main():
     while not_valid(express:=input('Enter a expression: ')):
         print('\nInvalid entry\n')
     print(f"{None} = {format(calculator(grouper(express)),',.2f')} " )
     main()
main()