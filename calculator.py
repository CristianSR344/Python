#Calculator

#Add

def add(n1,n2):
    """Adds both numbers"""
    return n1 + n2

#Substract
def substract(n1,n2):
    """Substracts both numbers"""
    return n1 - n2

#Multiply
def multiply(n1,n2):
    """Multiplies two numbers"""
    return n1 * n2

#Divide

def divide(n1,n2):
    """Divides two numbers"""
    return n1 / n2

operations={
    "+":add,
    "-":substract,
    "*":multiply,
    "/":divide,
}

num1=int(input("What's the first number? "))

for i in operations:
    print (i)
    
num2=int(input("What's the second number? "))
operation_symbol=input(" Pick an operation from the line above: ")
calculation_function=operations[operation_symbol]
answer = calculation_function(num1,num2)

print(f"{num1} {operation_symbol} {num2} = {answer}")

