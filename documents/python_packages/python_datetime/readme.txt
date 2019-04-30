from datetime import datetime
now_time = datetime.now()  -> return now time, it is a <class datetime.datetime> type

dt = datetime(2019, 4, 28, 21, 51)  -> in this case you can create a time of datetime format

timestamp = dt.timestamp()  -> you can transform a datetime format for a timestamp
import time
time.time()  -> it also return a timestamp

dt = datetime.fromtimestamp(timestamp)  -> on the contrary, transform timestamp for a datetime
dt  -> it's local time rather UTC time

str2datetime = datetime.strptime('2018-1-1', '%Y-%m-%d')  -> strptime, string to datetime

datetime2str = now_time.strftime('%Y-%m-%d')  -> on the contrary, datetime to str

from datetime import datetime, timedelta
delay_time = now_time + timedelta(days=1, hours=1)
