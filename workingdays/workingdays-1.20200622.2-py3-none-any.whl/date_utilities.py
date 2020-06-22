from datetime import timedelta, datetime
import re

from workingdays._version import version as __version__


def dateCleanup(datevalue, **kwargs):
    '''
    FUNCTION: dateCleanup

    ARGUMENT: datevalue (optionial epoch keyword arg, default is False)
        "datevalue" expected to be Type string unless epoch=True,
        Then datevalue expected to be Type Int

    DESCRIPTION:
        Returns datetime.datetime(y, m, d, h, M, s) of "datevalue".

    EXAMPLES:
        # ---------------------------------------------------------------------
        # Example German date format:
        # ---------------------------------------------------------------------
        >>> dateCleanup('07.04.2020')
        'datetime.datetime(2020, 4, 7, 0, 0)'
        # ---------------------------------------------------------------------
        # Example alpha date short format:
        # ---------------------------------------------------------------------
        >>> dateCleanup('MAR 25 2020')
        datetime.datetime(2020, 3, 25, 0, 0)
        # ---------------------------------------------------------------------
        # Example date with time format:
        # ---------------------------------------------------------------------
        >>> dateCleanup('2020-02-28 12:30:00')
        datetime.datetime(2020, 2, 28, 12, 30)
    '''
    # -------------------------------------------------------------------------
    # Set the Varaibles
    # -------------------------------------------------------------------------
    datelist = []
    epoch = False
    # -------------------------------------------------------------------------
    # check if epoch
    # -------------------------------------------------------------------------
    for key, value in kwargs.items():
        if key == 'epoch':
            epoch = value
    # -------------------------------------------------------------------------
    # set datevalue
    # -------------------------------------------------------------------------
    if epoch:
        datevalue = int(datevalue)
        cleanupdate = datetime.utcfromtimestamp(datevalue / 1000)
    else:
        datevalue = str(datevalue)
        # ---------------------------------------------------------------------
        # use regex to to separate datevalue into "Year, Month, and Day"
        # ---------------------------------------------------------------------
        # German date formats
        # Referencing https://en.wikipedia.org/wiki/Date_format_by_country
        # The format dd.mm.yyyy using dots (which denote ordinal numbering).
        # ---------------------------------------------------------------------
        germanDateFormat = re.match(r'([0-9]{2}\.[0-9]{2}\.[0-9]{4})',
                                    datevalue)
        if germanDateFormat:
            datelist = re.findall(r"[\w':\w':\w']+", datevalue)
            d = int(datelist[0])
            m = int(datelist[1])
            y = int(datelist[2])
            h = 0
            M = 0
            s = 0
            for value in datelist:
                # -------------------------------------------------------------
                # checking for Time patterns
                # -------------------------------------------------------------
                if re.match(r'([0-9]{2}:[0-9]{2}:[0-9])', value):
                    h = int(value[0:2])
                    M = int(value[3:5])
                    s = int(value[6:8])
        else:
            # -----------------------------------------------------------------
            # Clean date string (adding a space between DD & hh)
            # when pattern like 'YYYY-MM-DDhh:mm:ss' to 'YYYY-MM-DD hh:mm:ss'
            # or
            # when pattern like 'YYYY:MM:DDhh:mm:ss' to 'YYYY-MM-DD hh:mm:ss'
            # -----------------------------------------------------------------
            datevalue = re.sub(r'\W', '-',
                               re.sub
                               (r'(?<=[0-9]{4}\W[0-9]{2}\W[0-9]{2})(?=[^\s])',
                                r' ', datevalue), count=2)
            # -----------------------------------------------------------------
            # Splitting patterns into a list
            # -----------------------------------------------------------------
            datelist = re.findall(r"[\w':\w':\w']+", datevalue)
            # -----------------------------------------------------------------
            # datevalue has separators (list of numbers)
            # -----------------------------------------------------------------
            m = 0
            h = 0
            M = 0
            s = 0
            if len(datelist) > 1:
                for value in datelist:
                    # ---------------------------------------------------------
                    # checking for Months written as "alpha"
                    # then convert to number
                    # ---------------------------------------------------------
                    # example: Jan to 1 or March to 3
                    # ---------------------------------------------------------
                    if value.isalpha() is True:
                        m = int(datetime.strptime(value[0:3].capitalize(),
                                                  '%b').month)
                    # ---------------------------------------------------------
                    # checking for Time patterns
                    # ---------------------------------------------------------
                    elif re.match(r'([0-9]{2}:[0-9]{2}:[0-9])', value):
                        h = int(value[0:2])
                        M = int(value[3:5])
                        s = int(value[6:8])
                    # UTC Timezone Format
                    elif re.match(r'(\w[0-9]{2}:[0-9]{2}:[0-9]{2}\w)', value):
                        h = int(value[1:3])
                        M = int(value[4:6])
                        s = int(value[7:9])
                    # ---------------------------------------------------------
                    # checking for Year patterns
                    # ---------------------------------------------------------
                    elif len(value) == 4:
                        y = int(value)
                    # ---------------------------------------------------------
                    # checking for Day patterns
                    # ---------------------------------------------------------
                    elif int(value) > 12 < 31:
                        d = int(value)
                    # ---------------------------------------------------------
                    # checking if the value is <= 12, either Month or Day so if
                    # Month is not allready defined (by alpha pattern) set it
                    # ---------------------------------------------------------
                    elif int(value) <= 12:
                        if m != 0:
                            d = int(value)
                        else:
                            m = int(value)
            # -----------------------------------------------------------------
            # datevalue has no separators (string of numbers)
            # -----------------------------------------------------------------
            elif len(datelist) == 1:
                y = int(datevalue[0:4])
                m = int(datevalue[4:6])
                d = int(datevalue[6:8])
        # ---------------------------------------------------------------------
        # pass the datelist values to the "date" fuction
        # ---------------------------------------------------------------------
        if datevalue != '':
            cleanupdate = datetime(y, m, d, h, M, s)
    return cleanupdate


def workday(datevalue, offset, holidays=[]):
    # -------------------------------------------------------------------------
    # Workday Function
    # -------------------------------------------------------------------------
    # pass datevalue to the "dateCleanup" fuction
    startdate = dateCleanup(str(datevalue)).date()
    # pass all holidays to "dateCleanup" function
    holidays = [dateCleanup(str(dates)).date() for dates in holidays]
    i = 0
    workdays = startdate
    # -------------------------------------------------------------------------
    # iterate through offset to return working days
    # -------------------------------------------------------------------------
    while i < offset:
        # ---------------------------------------------------------------------
        # holiday
        # ---------------------------------------------------------------------
        if workdays + timedelta(days=1) in holidays:
            workdays += timedelta(days=1)
            # holidays don't count for offset, so add 1
            offset += 1
        # ---------------------------------------------------------------------
        # weekday
        # ---------------------------------------------------------------------
        elif workdays.isoweekday() < 5 or workdays.isoweekday() == 7:
            workdays += timedelta(days=1)
        # ---------------------------------------------------------------------
        # weekend
        # ---------------------------------------------------------------------
        else:
            workdays += timedelta(days=1)
            # weekends don't count for offset, so add 1
            offset += 1
        i += 1
    # -------------------------------------------------------------------------
    return workdays.strftime("%Y%m%d")


def workdayStart(datevalue, offset, holidays=[]):
    # -------------------------------------------------------------------------
    # WorkdayStart Function
    # -------------------------------------------------------------------------
    # pass datevalue to the "dateCleanup" fuction
    startdate = dateCleanup(str(datevalue)).date()
    # pass all holidays to "dateCleanup" function
    holidays = [dateCleanup(str(dates)).date() for dates in holidays]
    i = 0
    workdaystart = startdate
    # -------------------------------------------------------------------------
    # iterate through offset to return working days
    # -------------------------------------------------------------------------
    while i < offset:
        # ---------------------------------------------------------------------
        # holiday
        # ---------------------------------------------------------------------
        if workdaystart - timedelta(days=1) in holidays:
            workdaystart -= timedelta(days=1)
            # holidays don't count for offset, so add 1
            offset += 1
        # ---------------------------------------------------------------------
        # weekday
        # ---------------------------------------------------------------------
        elif 1 < workdaystart.isoweekday() < 7:
            workdaystart -= timedelta(days=1)
        # ---------------------------------------------------------------------
        # weekend
        # ---------------------------------------------------------------------
        else:
            workdaystart -= timedelta(days=1)
            # weekends don't count for offset, so add 1
            offset += 1
        i += 1
    # -------------------------------------------------------------------------
    return workdaystart.strftime("%Y%m%d")


def compareWorkingdays(datevalue, comparedate, holidays=[]):
    # -------------------------------------------------------------------------
    # Compare Workday Function
    # -------------------------------------------------------------------------
    # pass datevalue to the "dateCleanup" fuction
    startdate = dateCleanup(str(datevalue)).date()
    comparedate = dateCleanup(str(comparedate)).date()
    # pass all holidays to "dateCleanup" function
    holidays = [dateCleanup(str(dates)).date() for dates in holidays]
    i = 0
    # -------------------------------------------------------------------------
    # iterate through offset to return working days
    # -------------------------------------------------------------------------
    while startdate < comparedate:
        # ---------------------------------------------------------------------
        # holiday
        # ---------------------------------------------------------------------
        if startdate in holidays:
            # holidays don't count for offset, so skip updating "i"
            startdate += timedelta(days=1)
        # ---------------------------------------------------------------------
        # weekday
        # ---------------------------------------------------------------------
        elif startdate.isoweekday() <= 5:
            startdate += timedelta(days=1)
            i += 1
        # ---------------------------------------------------------------------
        # weekend
        # ---------------------------------------------------------------------
        else:
            # weekends don't count for offset, so skip updating "i"
            startdate += timedelta(days=1)
    networkdays = i
    # -------------------------------------------------------------------------
    return networkdays


def lastWorkdayofMonth(datevalue, holidays=[]):
    # -------------------------------------------------------------------------
    # Last Workday of Month Function
    # -------------------------------------------------------------------------
    startdate = dateCleanup(str(datevalue)).date()
    # pass all holidays to "dateCleanup" function
    holidays = [dateCleanup(str(dates)).date() for dates in holidays]
    nextmonth = startdate.replace(day=28) + \
        timedelta(days=4)  # this will never fail
    lastworkday = nextmonth - timedelta(days=nextmonth.day)
    # -------------------------------------------------------------------------
    # holiday
    # -------------------------------------------------------------------------
    if lastworkday in holidays:
        while lastworkday in holidays:
            lastworkday -= timedelta(days=1)
    # -------------------------------------------------------------------------
    # If lastworkday is a weekend then move to Friday
    # -------------------------------------------------------------------------
    # Saturday (subtract 1 day)
    # -------------------------------------------------------------------------
    elif lastworkday.isoweekday() == 6:
        lastworkday -= timedelta(days=1)
    # -------------------------------------------------------------------------
    # Sunday (subtract 2 days)
    # -------------------------------------------------------------------------
    elif lastworkday.isoweekday() == 7:
        lastworkday -= timedelta(days=2)
    # -------------------------------------------------------------------------
    return lastworkday.strftime("%Y%m%d")


def lastWorkdayofQtr(datevalue, holidays=[], **kwargs):
    '''
    FUNCTION: lastWorkdayofQtr

    DESCRIPTION:
        Returns last workday of Qtr for "datevalue" passed.
        Default Qtrs are in "Calendar Years".
        # ---------------------------------------------------------------------
        # Default Qtr list (Calendar Year)
        # ---------------------------------------------------------------------
        Q1 = ['Jan', 'Feb', 'Mar']
        Q2 = ['Apr', 'May', 'Jun']
        Q3 = ['Jul', 'Aug', 'Sep']
        Q4 = ['Oct', 'Nov', 'Dec']
        # ---------------------------------------------------------------------
        # Optional kwarg
        # ---------------------------------------------------------------------
        Optional kwarg can change the Qtr "Months".
        Can be a list or dict.

    RETURNS:
        datestring (%Y%m%d)

    EXAMPLES:
        # ---------------------------------------------------------------------
        # List Example:
        # ---------------------------------------------------------------------
        >>> lastWorkdayofQtr('20200213',Q1=["Nov", "Dec", "Jan"],
                             Q2=["Feb", "Mar", "Apr"])
        '20200430'
        # ---------------------------------------------------------------------
        # Dict Example:
        # ---------------------------------------------------------------------
        >>>quarters =  {"Q1": ["Nov", "Dec", "Jan"],
                        "Q2": ["Feb", "Mar", "Apr"],
                        "Q3": ["May", "Jun", "Jul"],
                        "Q4": ["Aug", "Sep", "Oct"]}
        >>>lastWorkdayofQtr('20200213', key=quarters)
        '20200430'
    '''
    # -------------------------------------------------------------------------
    # checkQtrList
    # -------------------------------------------------------------------------
    def checkQtrList(listobj):
        months = ['Jan', 'Feb', 'Mar',
                  'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep',
                  'Oct', 'Nov', 'Dec']
        qtrcheck = ''
        # ---------------------------------------------------------------------
        if (type(listobj) is list) is True:
            if len(listobj) == 3:
                qtrcheck = True
                qm = 0
                while qm < 2:
                    if listobj[qm] in months:
                        qtrcheck = True
                        qm += 1
                    else:
                        qtrcheck = False
                        qm = 2
            else:
                qtrcheck = False
        return qtrcheck
    # -------------------------------------------------------------------------
    # Last Workday of Qtr Function
    # -------------------------------------------------------------------------
    startdate = dateCleanup(str(datevalue)).date()
    startdate = startdate.replace(day=28)
    # pass all holidays to "dateCleanup" function
    holidays = [dateCleanup(str(dates)).date() for dates in holidays]
    monthNumber = ''
    items = ''
    # -------------------------------------------------------------------------
    # Default Qtr list (Calendar Year)
    # -------------------------------------------------------------------------
    Q1 = ['Jan', 'Feb', 'Mar']
    Q2 = ['Apr', 'May', 'Jun']
    Q3 = ['Jul', 'Aug', 'Sep']
    Q4 = ['Oct', 'Nov', 'Dec']
    # -------------------------------------------------------------------------
    # Set the optional Quarter variables
    # -------------------------------------------------------------------------
    for key, value in kwargs.items():
        if (type(value) is dict) is True:
            items = value.items()
        else:
            items = kwargs.items()
    for key, value in items:
        # ---------------------------------------------------------------------
        # Setting Q1
        # ---------------------------------------------------------------------
        if key == 'Q1':
            qtrcheck = checkQtrList(value)
            if qtrcheck is True:
                Q1 = value
        # ---------------------------------------------------------------------
        # Setting Q2
        # ---------------------------------------------------------------------
        if key == 'Q2':
            qtrcheck = checkQtrList(value)
            if qtrcheck is True:
                Q2 = value
        # ---------------------------------------------------------------------
        # Setting Q3
        # ---------------------------------------------------------------------
        if key == 'Q3':
            qtrcheck = checkQtrList(value)
            if qtrcheck is True:
                Q3 = value
        # ---------------------------------------------------------------------
        # Setting Q4
        # ---------------------------------------------------------------------
        if key == 'Q4':
            qtrcheck = checkQtrList(value)
            if qtrcheck is True:
                Q4 = value
    # -------------------------------------------------------------------------
    # Find End of Qtr Month
    # -------------------------------------------------------------------------
    # Q1 cutoff
    # -------------------------------------------------------------------------
    if startdate.strftime("%b") in Q1:
        monthNumber = datetime.strptime(Q1[2], '%b').month
        # If month is in Nov or Dec, update year by 1
        if startdate.strftime("%b") in ('Nov', 'Dec'):
            startdate = startdate.replace(startdate.year + 1)
        startdate = startdate.replace(month=monthNumber)
    # -------------------------------------------------------------------------
    # Q2 cutoff
    # -------------------------------------------------------------------------
    elif startdate.strftime("%b") in Q2:
        monthNumber = datetime.strptime(Q2[2], '%b').month
        startdate = startdate.replace(month=monthNumber)
    # -------------------------------------------------------------------------
    # Q3 cutoff
    # -------------------------------------------------------------------------
    elif startdate.strftime("%b") in Q3:
        monthNumber = datetime.strptime(Q3[2], '%b').month
        startdate = startdate.replace(month=monthNumber)
    # -------------------------------------------------------------------------
    # Q4 cutoff
    # -------------------------------------------------------------------------
    elif startdate.strftime("%b") in Q4:
        monthNumber = datetime.strptime(Q4[2], '%b').month
        startdate = startdate.replace(month=monthNumber)
    # -------------------------------------------------------------------------
    # Set last day of qtr
    # -------------------------------------------------------------------------
    nextmonth = startdate + timedelta(days=4)  # this will never fail
    lastworkday = nextmonth - timedelta(days=nextmonth.day)
    # -------------------------------------------------------------------------
    # holiday
    # -------------------------------------------------------------------------
    if lastworkday in holidays:
        while lastworkday in holidays:
            lastworkday -= timedelta(days=1)
    # -------------------------------------------------------------------------
    # If lastworkday of qtr is a weekend then move to Friday
    # -------------------------------------------------------------------------
    # Saturday (subtract 1 day)
    # -------------------------------------------------------------------------
    elif lastworkday.isoweekday() == 6:
        lastworkday -= timedelta(days=1)
    # -------------------------------------------------------------------------
    # Sunday (subtract 2 days)
    # -------------------------------------------------------------------------
    elif lastworkday.isoweekday() == 7:
        lastworkday -= timedelta(days=2)
    # -------------------------------------------------------------------------
    return lastworkday.strftime("%Y%m%d")


def lastDayofMonth(datevalue):
    # -------------------------------------------------------------------------
    # Last day of Month Function
    # -------------------------------------------------------------------------
    startdate = dateCleanup(str(datevalue)).date()
    nextmonth = startdate.replace(day=28) + \
        timedelta(days=4)  # this will never fail
    nextmonth = nextmonth - timedelta(days=nextmonth.day)
    # -------------------------------------------------------------------------
    return nextmonth.strftime("%Y%m%d")


def setSortValue(str):
    global sortvalue    # Needed to modify global copy of SortValue
    sortvalue = str


def dateSort(DictObj):
    try:
        return DictObj[sortvalue]
    except BaseException as msg:
        warn = 'Please pass Global "sortvalue" in function ' + \
            '"setSortValue()" first: {}'
        print(warn.format(msg))
        print('Please pass sortvalue in setSortValue(str) function first.')
