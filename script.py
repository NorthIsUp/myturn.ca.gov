import beepy
from colorama import Fore, Back, Style
import datetime
import json
import os
from pytz import timezone
import sys
import time


date_format='%m/%d/%Y %H:%M:%S %Z'
cookie = '_abck=D6E2EEEA8B7B2DA71A0E04A60F47783D~0~YAAQLiI1F05B4It3AQAAmz9arAW1ngwzNiLzlZTJO9cP8pR5mNRiKI7J3aWh7hnlh8vnEDXxEHW5bycL1E2FFA2IJP75Z3OEUFIWdtnzWFdmz5sP40eAt3vlSVUs7HM1OYQlsx7k35eoY6tV5m2fmhygw4CVdOqQ49xOyDjkII5GkFGgwKXy5VfCH0qMPz88Njy2cNXHrtYTO8ikK+X1JODk5MCdX+Pwu6MQQdvXhwSjCZEKwAhuLGkca3noLmVL0G3nqr8sgbWa48oVEGL+0ztxTqZ7MfXcPxPBYKcDJOG+oNcPQfjDI1UdTqguIxDpDaTcQuYMpH/wNWA2DW25FPik~-1~-1~-1; ak_bmsc=45960D750CC6CF53CAAC1BAFF432ED0817C53316BD5C000060CB33608E9B8709~plPW6uOHybwANPs7ZCsw5dYC+OFcAQssFJSne06I54vpKfmNJc9BdJqjSRwI8/mY0+dph18Aa9MAd9i3XvBh2XD46g2igobZ1KR8PDW3lPMqv2mgIV35EU4vOopU0LdQtSl/LUcmX9xFASbn+tfiDA8/2qzIfHkyUUDVzWb8ts2FOezbmMNJLBPJFJ1TKi4UDZhDrXvVDuJvkho+TLTEhoPS75LegOpUH159Gt5qkMJwhJ3H2NOL6VdqB++RYcR2Va; bm_sz=A8B00929D8D620FACCC624DBA06215B6~YAAQFjPFF7npCbZ3AQAAzW9SygpRvc9h0oR370Shre/uIEWYKBDrfXlLWea//06pA9NfLxtjunW8B9WG0SwKmYIzprWzunL/cQrLf9qXLKoLFSR9183iV+qWtc2mndNztfOgKi0A57DlfpaEIiA6EDv0k1ptQWflwR0ijUx2HXumTHBRI0HYeVjJ2MQ=; bm_sv=97F261B3C6D3F168E303005BD7B5B414~vue5JYfiZuaETTKijh4MBrptK6FC1wCdUic2kxF6BkNEvQk0uFFxv/LEZDBCg+Z89jCwHjDIB8/CQYTB85HlFwUPXdovKpBirYdIeMIx/7O9cRjjppU2p8rllSfFGNCkIFAkS5s8GTnRGsOdnAM1HQ=='
vaccineData = 'WyJhM3F0MDAwMDAwMDFBZExBQVUiXQ=='
locations = {
    "a2ut0000006a92VAAQ": "Alameda County - CalOES (Drive Thru 2)",
    "a2ut0000006a92aAAA": "Alameda County - CalOES (Walk up 2)"
    }

def getLocationQuery(locationId, startDate, endDate):
    return """curl -s 'https://api.myturn.ca.gov/public/locations/""" + locationId + """/availability' \
        -H 'authority: api.myturn.ca.gov' \
        -H 'accept: application/json, text/plain, */*' \
        -H 'x-correlation-id: ee7c62e3-9136-4b44-923c-56f62ceac2bb' \
        -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36' \
        -H 'content-type: application/json;charset=UTF-8' \
        -H 'origin: https://myturn.ca.gov' \
        -H 'sec-fetch-site: same-site' \
        -H 'sec-fetch-mode: cors' \
        -H 'sec-fetch-dest: empty' \
        -H 'referer: https://myturn.ca.gov/' \
        -H 'accept-language: en-US,en;q=0.9' \
        -H 'cookie: """ + cookie + """' \
        --data-raw '{"startDate":\"""" + startDate + """\","endDate":\"""" + endDate + """\","vaccineData":\"""" + vaccineData + """\","doseNumber":1,"url":"https://myturn.ca.gov/appointment-select"}' \
        --compressed"""

def getSlotsQuery(locationId, availableDate):
    return """curl -s 'https://api.myturn.ca.gov/public/locations/"""+ locationId +"""/date/""" + availableDate + """/slots' \
        -H 'authority: api.myturn.ca.gov' \
        -H 'accept: application/json, text/plain, */*' \
        -H 'x-correlation-id: ee7c62e3-9136-4b44-923c-56f62ceac2bb' \
        -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36' \
        -H 'content-type: application/json;charset=UTF-8' \
        -H 'origin: https://myturn.ca.gov' \
        -H 'sec-fetch-site: same-site' \
        -H 'sec-fetch-mode: cors' \
        -H 'sec-fetch-dest: empty' \
        -H 'referer: https://myturn.ca.gov/' \
        -H 'accept-language: en-US,en;q=0.9' \
        -H 'cookie: """ + cookie + """"' \
        --data-raw '{"vaccineData":\"""" + vaccineData + """\","url":"https://myturn.ca.gov/appointment-select"}' \
        --compressed"""

def printColor(string, back, fore, index=0):
    print('\t'*index + back + fore + string + Style.RESET_ALL)

def printSuccess(string, index=0):
    printColor(string, Back.LIGHTGREEN_EX, Fore.RED, index)

def printFail(string, index=0):
    printColor(string, Back.LIGHTYELLOW_EX, Fore.MAGENTA, index)

def printError(string, index=0):
    printColor(string, Back.LIGHTRED_EX, Fore.BLUE, index)

def printNow():
    currentTime = datetime.datetime.now().astimezone(timezone('US/Pacific')).strftime(date_format)
    printColor(currentTime, Back.WHITE, Fore.BLACK)

while True:
    startDate = datetime.date.today()
    endDate = startDate + datetime.timedelta(days=7)
    startDate = startDate.isoformat()
    endDate = endDate.isoformat()
    for locationId, location in locations.items():
        query = getLocationQuery(locationId, startDate, endDate)
        result = os.popen(query).read()
        printNow()
        if 'false' not in result:
            printError("Update Vaccine Data:")
            beepy.beep(sound='robot_error')
            vaccineData = input()
        elif 'true' in result:
            printSuccess("Vaccine Available")
            resultData = json.loads(result)
            for dateAvailability in resultData['availability']:
                if dateAvailability['available']:
                    printSuccess("Date: " + dateAvailability['date'], index=1)
                    query = getSlotsQuery(locationId, dateAvailability['date'])
                    slotResult = os.popen(query).read()
                    slotsData = json.loads(slotResult)
                    for slot in slotsData['slotsWithAvailability']:
                        printSuccess("Time: " + slot['localStartTime'], index=2)
            printSuccess("Location:" + location, index=1)
            beepy.beep(sound='success')
        else:
            printFail("Vaccine Not Available at " + location)
        time.sleep(5)
