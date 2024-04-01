#Password Generator Project
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters= int(input("How many letters would you like in your password?\n")) 
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

#Eazy Level - Order not randomised:
#e.g. 4 letter, 2 symbol, 2 number = JduE91&!


#Hard Level - Order of characters randomised:
#e.g. 4 letter, 2 symbol, 2 number = g^2jk8&P

total=nr_letters+nr_symbols+nr_numbers
password=""
cont_let=0
cont_sym=0
cont_num=0
array = []

for m in range(0, nr_letters):
    rm_letters=random.randint(0,len(letters)-1)
    password+=letters[rm_letters]
    
for i in range(0,nr_symbols):
    rm_symbols=random.randint(0,len(symbols)-1)
    password+=symbols[rm_symbols]
        
for j in range(0, nr_letters):
    rm_numbers=random.randint(0,len(numbers)-1)
    password+=numbers[rm_numbers]
    
array=list(password)

random.shuffle(array)
password=""
for i in range(0,len(array)-1):
    password+=array[i]

print(password)

