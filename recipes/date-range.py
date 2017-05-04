#!/usr/bin/python3
# Finding the Date Range for the Current Month

from datetime import datetime, date, timedelta
import calendar

def get_month_range(start_date=None):
	if start_date is None:
		start_date = date.today().replace(day=1)

	_, days_in_month = calendar.monthrange(start_date.year, start_date.month)
	end_date = start_date + timedelta(days=days_in_month)
	return (start_date, end_date)

def date_range(start, stop, step):
	while start < stop:
		yield start
		start += step


if __name__ == '__main__':
	for d in date_range(datetime.today(), datetime.today() + timedelta(days=1), timedelta(hours=6)):
		print(d)