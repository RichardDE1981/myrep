##############################################
# Date Loop
#
# Script generates a list of dates using today´s date as a starting point - reaching back until 1st of january of prev-year
#
#############################################

from datetime import date, timedelta



Pyear = date.today().year -1
#print(type(Pyear))

Cdate = date(date.today().year, date.today().month, date.today().day)
PDate = date(date.today().year-1, 1,1)

delta = Cdate-PDate
#print(delta.days)

new_date = (PDate + timedelta(days = 0))

for x in range(delta.days):
    
    print(new_date)
    new_date = (new_date + timedelta(days = 1))

