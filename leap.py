def is_leap(year):
  flag=False
  if year % 4 == 0:
    if year % 100 == 0:
      if year % 400 == 0:
        flag=True
      else:
        flag=False
    else:
      flag=True
  else:
    flag=False
  return flag
  
# TODO: Add more code here 👇
def days_in_month(year,month):
  month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] 
  if is_leap(year):
      month_days[1]=29

  return month_days[month-1]
  
  
#🚨 Do NOT change any of the code below 
year = int(input()) # Enter a year
month = int(input()) # Enter a month
days = days_in_month(year, month)
print(days)

