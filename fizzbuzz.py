# Write your code here 👇
target = int(input()) # Enter a number between 0 and 100

for number in range(1,100+1):
  if number %5==0 and number %3==0:
      print("FizzBuzz")
  elif number %3==0:
      print("Fizz")
  elif number %5==0:
      print("Buzz")
  else:
      print(number)  
       
      