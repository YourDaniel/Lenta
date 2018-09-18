from datetime import datetime
now = datetime.today()
print(now)
'''
%y - year
%m - month
%d - day
%b - month name short
%Y - full year
%A - day of the week
%B - month name full
%H - hours
%M - minutes
%S - seconds
'''

print(now.strftime("The file has created at %H:%M on %d.%m.%y"))
