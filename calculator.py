#Calculator
from calculator_art import logo
import os


clear=lambda: os.system('cls')

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

def calculator():
    print(calculator_art().logo)
    
    num1=float(input("What's the first number? "))
    for i in operations:
        print (i)
    flag=True

    while flag:
        
        operation_symbol=input(" Pick an operation: ")
        num2=float(input("What's the next number? "))

        
        calculation_function=operations[operation_symbol]
        answer = calculation_function(num1,num2)
        print(f"{num1} {operation_symbol} {num2} = {answer}")
        
        if input(f"Type 'y' to continue calculating with {answer}, or type 'n to start a new calculation.:")=="y":
            num1= answer
        else:
            flag=False
            clear()
            calculator()
        
calculator()


