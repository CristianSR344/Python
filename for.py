#For Loop with Range
#(begining, end, step)
# for number in range(1,11, 3):
#     print(number)

target = int(input()) # Enter a number between 0 and 1000
# 🚨 Do not change the code above ☝️

# Write your code here 👇
total=0

for even in range(0,target,2):
  total+=even

if target%2==0:
    total+=target
  
print(total)

even_sum = 0
for number in range(2, target + 1, 2):
  even_sum += number
print(even_sum)

# alternative_sum = 0
# for number in range(1, target + 1):
#   if number % 2 == 0:
#     alternative_sum += number
# print(alternative_sum)
    