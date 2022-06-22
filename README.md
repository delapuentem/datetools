# Datetools Python Library
Custom library of tools for working with dates in any format in Python 3.x

## How to use

Make sure that import the library and get two dates.

```python
#!/usr/bin/env python3
import datetools

date1 = '2022-05-20T17:32:11'
date2 = '2022-05-31 23:35:11'
```

### normalize_date
From a string containing a date that matches the specified regex, applies the time zone and returns the normalized date. By default, the output format is %Y-%m-%d %H:%M:%S, but any output format can be specified. By default, the time zone is +0, but it can be set to positive or negative numbers.

```python
print(f"Normalize date: {date1} -> {normalize_date(stringdate=date1)}")
```

**Custom output format**
By default the output format is `%Y-%m-%d %H:%M:%S` but you can set custom output format.

```python
normalize_date(stringdate=date1, output_format='%d %H:%M:%S')
```

**Custom timezone**
Add or subtract hours based on time zone.

```python
normalize_date(stringdate=date1, time_zone=+5)
```

### tag_date
Returns a MONTH-YEAR date in English or Spanish in string format. By default it is in Spanish.

```python
tag_date(stringdate=date1)
tag_date(stringdate=date1, language='en')
```

### different_days
Returns True or False if it is the same day or not.

```python
print(f"¿Are {date1} y {date2} the same day? -> {different_days(stringdate1=date1, stringdate2=date2)}")
```

### subtract_dates
Subtracts two dates from the past and returns the difference in days, hours, minutes, or seconds. By default it returns a value in seconds.

```python
subtract_dates(stringdate1=date1, stringdate2=date2, unit='second')
subtract_dates(stringdate1=date1, stringdate2=date2, unit='min')
subtract_dates(stringdate1=date1, stringdate2=date2, unit='hour')
subtract_dates(stringdate1=date1, stringdate2=date2, unit='day')
```

### weekday_num
Returns the number of the day of the week. 0 is Monday.

```python
weekday_num(stringdate=date1)
```

### weekday_name
Returns the day of the week in English or Spanish in string format. By default it is in Spanish.

```python
weekday_name(stringdate=date1)
weekday_name(stringdate=date1, language='en')
```

### weekday_counter
Knowing the day of the week in which we are, and the difference in days between two dates, it counts the days of the week that are in between (not including beginning and end). By default it is in Spanish.

```python
weekday_counter(weekday_num(date1), days_between=subtract_dates(date1, date2, unit='day'))
weekday_counter(weekday_num(date1), days_between=subtract_dates(date1, date2, unit='day'), language='en')
```