from collections import deque

operators = ["+", "-", "/", "*", "~"]

def calculate(line:str) -> int:
    result = 0
    stack = deque()
    for val in line.split(" "):
    
        if val in operators:
            r = int(stack.pop())
            l = int(stack.pop())
            match val:
                case "+":
                   stack.append(l + r)
                case "-":
                   stack.append(l - r) 
                case "*":
                   stack.append(l * r) 
                case "/":
                   stack.append(l / r)
                case "~":
                    if l != 0 and r != 0:
                        stack.append(abs(l - r))
                    else:
                        stack.append((sum([int(val) for val in stack]) + r + l)**2)
        else:
            stack.append(val)
                    
                    


    return stack.pop()

    