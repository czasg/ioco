import re
import datetime

MIN_T = [1970, 1, 1, 0, 0, 0]
MAX_T = [2100, 12, 31, 23, 59, 59]


class TimeManager(object):
    def __init__(self, data=None):
        if isinstance(data, datetime.datetime):
            self._string = self.time2str(data)
        elif isinstance(data, str):
            self._datetime = self.str2time(data)
        else:
            raise Exception("input error!")

    @classmethod
    def from_str(cls, string):
        cls._string = string
        return cls(string)

    @classmethod
    def from_time(cls, datetime):
        cls._datetime = datetime
        return cls(datetime)

    @property
    def time(self):
        return self._datetime

    @time.setter
    def time(self, _time):
        self._time = _datetime

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, _string):
        self._string = _string

    def _time2str(self, _datetime=None):
        return datetime.datetime.strftime(_datetime, "%Y-%m-%d %H:%M:%S.%f")

    def time2str(self, _datetime=None):
        _datetime = _datetime if _datetime else self._datetime
        return self._time2str(_datetime)

    def _str2time(self, string=None, format=None, **kwargs):
        res = None
        args = kwargs.get('args', None)
        if args:
            res = datetime.datetime(*args)
        if not res:
            res = datetime.datetime.strptime(string, format)
        return res

    def str2time(self, string, format=None):
        if format:
            res = self._str2time(string, format)
        elif re.match('\d{8}$', string):
            res = self._str2time(string, '%Y%m%d')
        else:
            reRule = """(\d{4}|\d{2})[^\d]*(\d*)[^\d]*(\d*)[^\d]*(\d*)[^\d]*(\d*)[^\d]*(\d*)"""
            timeGroup = re.search(reRule, string)
            res = MIN_T[:]
            for i in range(6):
                groupValue = timeGroup.group(i + 1)
                if groupValue:
                    groupValue = '20' + groupValue if i == 0 and len(groupValue) == 2 else groupValue
                    t = int(groupValue)
                    if t > MAX_T[i] or t < MIN_T[i]:
                        break
                    res[i] = t
            res = self._str2time(args=res)
        return res

    def add(self, **kwargs):
        self._datetime = self._datetime + datetime.timedelta(**kwargs)
        return self


if __name__ == "__main__":
    # create by string
    TM = TimeManager.from_str('hello, cza 1995-09-17')
    print('TMS', TM.string)
    print('TMS', TM.time)
    print('TMS', TM.time2str())
    print('TMS', TM.add(days=1).add(hours=1).time)
    # create by datetime.datetime
    now = datetime.datetime.now()
    TM = TimeManager.from_time(now)
    print('TMT', TM.time)
    print('TMT', TM.string)
    print('TMT', TM.add(days=1).add(hours=1).time)
