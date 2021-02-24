import beepy
from collections import OrderedDict
from colorama import Fore, Back, Style
import datetime
import json
import os
from pprint import pprint
from pytz import timezone
import sys
import time
from enum import Enum


class IdTypeValue:
    def __init__(self, id, type, value=None):
        self.id = id
        self.type = type
        if value is not None:
            self.value = value

# Change 3rd Parameter in each IdTypeEnum() for each enum
class PatientEligibilityData(Enum):
    AGE_CHECK = IdTypeValue("q.screening.18.yr.of.age", "multi-select", ["q.screening.18.yr.of.age"])
    HEALTH_DATA = IdTypeValue("q.screening.health.data", "multi-select", ["q.screening.health.data"])
    PRIVACY_STATEMENT = IdTypeValue("q.screening.privacy.statement", "multi-select", ["q.screening.privacy.statement"])
    AGE_RANGE = IdTypeValue("q.screening.eligibility.age.range", "single-select", "16 - 49")
    INDUSTRY = IdTypeValue("q.screening.eligibility.industry", "single-select", "Education and childcare")
    COUNTY = IdTypeValue("q.screening.eligibility.county", "single-select", "Almeda")
    CODE = IdTypeValue("q.screening.accessibility.code", "text")

# Change 3rd Parameter in each IdTypeEnum() for each enum
class PatientData(Enum):
    FIRST_NAME = IdTypeValue("q.patient.firstname", "text", "Jane")
    LAST_NAME = IdTypeValue("q.patient.lastname", "text", "Doe")
    SUFFIX = IdTypeValue("q.patient.suffix", "text")
    BIRTHDAY = IdTypeValue("q.patient.birthday", "date", "1980-01-01")
    MOTHERS_FIRST_NAME = IdTypeValue("q.patient.mothersfirstname", "text", "Mommy")
    GENDER = IdTypeValue("q.patient.gender", "single-select", "Female")
    RACE = IdTypeValue("q.patient.race", "single-select", "Asian Indian")
    ETHNICITY = IdTypeValue("q.patient.ethnicity", "single-select", "Not of Hispanic, Latino or Spanish origin")
    EMAIL = IdTypeValue("q.patient.email", "email", "jane.doe@gmail.com")
    MOBILE = IdTypeValue("q.patient.mobile", "mobile-phone", "+19876543210")
    ADDRESS = IdTypeValue("q.patient.address", "address-lookup", "1 JaneDoe St")
    CITY = IdTypeValue("q.patient.city", "text", "San Francisco")
    ZIP_CODE = IdTypeValue("q.patient.zip.code", "text", "94108")
    HEALTH_INSURANCE = IdTypeValue("q.patient.health.insurance", "single-select", "No")
    SICK_TODAY = IdTypeValue("q.patient.sick.today", "single-select", "No")
    SERIOUS_REACTION = IdTypeValue("q.patient.serious.reaction", "single-select", "No")
    LONG_TERM_HEALTH_ISSUE = IdTypeValue("q.patient.long.term.health.issue", "single-select", "No")
    IMMUNE_SYSTEM_PROBLEM = IdTypeValue("q.patient.immune.system.problem", "single-select", "No")
    FAMILIAL_IMMUNE_SYSTEM_ISSUE = IdTypeValue("q.patient.immune.system.issue", "single-select", "No")
    IMMUNE_SYSTEM_MEDICATION = IdTypeValue("q.patient.immune.system.medication", "single-select", "No")
    NERVOUS_SYSTEM_ISSUE = IdTypeValue("q.patient.nervous.system.issue", "single-select", "No")
    BLOOD_TRANSFUSION = IdTypeValue("q.patient.blood.transfusion", "single-select", "No")
    PREGNANT = IdTypeValue("q.patient.pregnant", "single-select", "No")
    RECENTLY_VACCINATED = IdTypeValue("q.patient.recently.vaccinated", "single-select", "No")
    ALLERGIES = IdTypeValue("q.patient.allergies", "single-select", "No")

# Specify User's Latitude and Longitude
LAT = "37.791904699999996"
LNG = "-122.4078356"

DEBUG = False
FIRST_DATE_OFFSET_HOURS = 24
date_format='%m/%d/%Y %H:%M:%S %Z'
query_date_format='%Y-%m-%d'
cookie = '_abck=D6E2EEEA8B7B2DA71A0E04A60F47783D~0~YAAQLiI1F05B4It3AQAAmz9arAW1ngwzNiLzlZTJO9cP8pR5mNRiKI7J3aWh7hnlh8vnEDXxEHW5bycL1E2FFA2IJP75Z3OEUFIWdtnzWFdmz5sP40eAt3vlSVUs7HM1OYQlsx7k35eoY6tV5m2fmhygw4CVdOqQ49xOyDjkII5GkFGgwKXy5VfCH0qMPz88Njy2cNXHrtYTO8ikK+X1JODk5MCdX+Pwu6MQQdvXhwSjCZEKwAhuLGkca3noLmVL0G3nqr8sgbWa48oVEGL+0ztxTqZ7MfXcPxPBYKcDJOG+oNcPQfjDI1UdTqguIxDpDaTcQuYMpH/wNWA2DW25FPik~-1~-1~-1; ak_bmsc=45960D750CC6CF53CAAC1BAFF432ED0817C53316BD5C000060CB33608E9B8709~plPW6uOHybwANPs7ZCsw5dYC+OFcAQssFJSne06I54vpKfmNJc9BdJqjSRwI8/mY0+dph18Aa9MAd9i3XvBh2XD46g2igobZ1KR8PDW3lPMqv2mgIV35EU4vOopU0LdQtSl/LUcmX9xFASbn+tfiDA8/2qzIfHkyUUDVzWb8ts2FOezbmMNJLBPJFJ1TKi4UDZhDrXvVDuJvkho+TLTEhoPS75LegOpUH159Gt5qkMJwhJ3H2NOL6VdqB++RYcR2Va; bm_sz=A8B00929D8D620FACCC624DBA06215B6~YAAQFjPFF7npCbZ3AQAAzW9SygpRvc9h0oR370Shre/uIEWYKBDrfXlLWea//06pA9NfLxtjunW8B9WG0SwKmYIzprWzunL/cQrLf9qXLKoLFSR9183iV+qWtc2mndNztfOgKi0A57DlfpaEIiA6EDv0k1ptQWflwR0ijUx2HXumTHBRI0HYeVjJ2MQ=; bm_sv=97F261B3C6D3F168E303005BD7B5B414~vue5JYfiZuaETTKijh4MBrptK6FC1wCdUic2kxF6BkNEvQk0uFFxv/LEZDBCg+Z89jCwHjDIB8/CQYTB85HlFwUPXdovKpBirYdIeMIx/7O9cRjjppU2p8rllSfFGNCkIFAkS5s8GTnRGsOdnAM1HQ=='
vaccineData = 'WyJhM3F0MDAwMDAwMDFBZExBQVUiXQ=='

locations = OrderedDict()
# Arrange below enteries in decreasing order of priority for a location
locations["a2ut0000006a8t9AAA"] = "San Francisco Moscone Center (SOUTH)"
locations["a2ut0000006a92VAAQ"] = "Alameda County - CalOES (Drive Thru 2)"
locations["a2ut0000006a92aAAA"] = "Alameda County - CalOES (Walk up 2)"

def getEligibityQuestionResponse():
    return json.dumps([e.value.__dict__  for e in PatientEligibilityData])

def getPersonalDetails():
    return json.dumps([e.value.__dict__  for e in PatientData])

def prepareHeaders():
    return """-H 'authority: api.myturn.ca.gov' \
        -H 'accept: application/json, text/plain, */*' \
        -H 'x-correlation-id: 099e3439-9243-4d3b-bd51-0d28956714a0' \
        -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36' \
        -H 'content-type: application/json;charset=UTF-8' \
        -H 'origin: https://myturn.ca.gov' \
        -H 'sec-fetch-site: same-site' \
        -H 'sec-fetch-mode: cors' \
        -H 'sec-fetch-dest: empty' \
        -H 'referer: https://myturn.ca.gov/' \
        -H 'accept-language: en-US,en;q=0.9' \
        -H 'cookie: """ + cookie + """'"""

def getCurlQuery(url, payload):
    return """curl -s '""" + url + """' \
        """ + prepareHeaders() + """ \
        --data-raw '""" + payload + """' \
        --compressed"""

def getSearchQuery(startDate):
    return getCurlQuery(
        """https://api.myturn.ca.gov/public/locations/search""",
        """{"location":{"lat":""" + LAT + ""","lng":""" + LNG + """},"fromDate":\"""" + startDate + """\","vaccineData":\"""" + vaccineData + """\","locationQuery":{"includePools":["default"]},"url":"https://myturn.ca.gov/location-select"}"""
    )

def getLocationQuery(locationId, startDate, endDate, doseNumber=1):
    return getCurlQuery(
        """https://api.myturn.ca.gov/public/locations/""" + locationId + """/availability""",
        """{"startDate":\"""" + startDate + """\","endDate":\"""" + endDate + """\","vaccineData":\"""" + vaccineData + """\","doseNumber":""" + str(doseNumber) + ""","url":"https://myturn.ca.gov/appointment-select"}"""
    )

def getSlotsQuery(locationId, availableDate):
    return getCurlQuery(
        """https://api.myturn.ca.gov/public/locations/"""+ locationId +"""/date/""" + availableDate + """/slots""",
        """{"vaccineData":\"""" + vaccineData + """\","url":"https://myturn.ca.gov/appointment-select"}"""
    )

def getReserveQuery(locationId, availableDate, availableSlot, doseNumber=1):
    return getCurlQuery(
        """https://api.myturn.ca.gov/public/locations/""" + locationId + """/date/""" + availableDate + """/slots/reserve""",
        """{"dose":""" + str(doseNumber) + ""","locationExtId":\"""" + locationId + """\","date":\"""" + availableDate + """\","localStartTime":\"""" + availableSlot + """\","vaccineData":\"""" + vaccineData + """\","url":"https://myturn.ca.gov/appointment-select"}"""
    )

def getIssueQuery(dose1ReservationId):
    return getCurlQuery(
        """https://api.myturn.ca.gov/public/onetimecode/issue""",
        """{
            "personalDetails":
            """ + getPersonalDetails() + """,
            "locale":"en_US",
            "context":{"type":"reservation","value":\"""" + dose1ReservationId + """\"},
            "url":"https://myturn.ca.gov/verify-identity"}"""
    )

def getAppointmentQuery(issueId, oneTimeCode, dose1ReservationId, dose2ReservationId):
    return getCurlQuery(
        """https://api.myturn.ca.gov/public/appointments""",
        """{
            "eligibilityQuestionResponse":
            """ + getEligibityQuestionResponse() + """,
            "personalDetails":
            """ + getPersonalDetails() + """,
            "additionalQuestionsResponse":[],
            "oneTime":{"id":\"""" + issueId + """\","code":\"""" + str(oneTimeCode) + """\"},
            "reservationIds":[\"""" + dose1ReservationId + """\",\"""" + dose2ReservationId + """\"],
            "locale":"en_US",
            "url":"https://myturn.ca.gov/verify-identity"
            }"""
    )

def getQueryResult(query):
    result = json.loads(os.popen(query).read())
    if DEBUG:
        pprint(query)
        pprint(result)
    return result

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

def getReservation(locationId, availableDate, doseNumber=1):
    slotQuery = getSlotsQuery(locationId, availableDate)
    slotsData = getQueryResult(slotQuery)
    for slot in slotsData['slotsWithAvailability']:
        reserveQuery = getReserveQuery(locationId, availableDate, slot['localStartTime'], doseNumber=doseNumber)
        reserveData = getQueryResult(reserveQuery)
        reservationId = reserveData['reservationId']
        minBetween = reserveData['vaccineDetails']['daysBetweenDoses']['min']
        maxBetween = reserveData['vaccineDetails']['daysBetweenDoses']['max']
        return reservationId, minBetween, maxBetween
    return None, None, None

def getFirstAvailableDateForLocation(locationId, startDate, endDate, doseNumber=1):
    locationQuery = getLocationQuery(locationId, startDate.strftime(query_date_format), endDate.strftime(query_date_format), doseNumber)
    locationResult = os.popen(locationQuery).read()
    if 'available' not in locationResult:
        printError("Update Vaccine Data:")
        beepy.beep(sound='robot_error')
        vaccineData = input()
    elif 'true' in locationResult:
        locationData = json.loads(locationResult)
        for dateAvailability in locationData['availability']:
            if dateAvailability['available']:
                return dateAvailability['date']
    return None

def getFirstAvailableDate(startDate, range=7):
    endDate = startDate + datetime.timedelta(days=range)
    for locationId, location in locations.items():
        availableDate = getFirstAvailableDateForLocation(locationId, startDate, endDate)
        if availableDate:
            return locationId, availableDate
    return None, None

def getFirstAvailableDateFromToday():
    startDate = datetime.datetime.now().astimezone(timezone('US/Pacific')) + datetime.timedelta(hours=FIRST_DATE_OFFSET_HOURS)
    return getFirstAvailableDate(startDate)

def bookAppointment(dose1ReservationId, dose2ReservationId):
    issueQuery = getIssueQuery(dose1ReservationId)
    issueData = getQueryResult(issueQuery)
    beepy.beep(sound='ping')
    oneTimeCode = int(input("Check Email or Mobile. Enter One Time Code: "))
    appointmentQuery = getAppointmentQuery(issueData['id'], oneTimeCode, dose1ReservationId, dose2ReservationId)
    appointmentData = getQueryResult(appointmentQuery)
    print(appointmentData)
    if 'confirmationCode' not in appointmentData:
        printFail("Incorrect One Time Code or Error: " + appointmentData['errorType'])
        return None
    return appointmentData['confirmationCode']

def getOffsetDate(date, offset):
    return datetime.datetime.strptime(date, query_date_format) + datetime.timedelta(days=offset)

def makeAppointment():
    locationId, firstAvailableDate = getFirstAvailableDateFromToday()
    if locationId:
        dose1ReservationId, minBetween, maxBetween = getReservation(locationId, firstAvailableDate, doseNumber=1)
        if dose1ReservationId:
            dose2DateMin = getOffsetDate(firstAvailableDate, minBetween)
            dose2DateMax = getOffsetDate(firstAvailableDate, maxBetween)
            dose2Date = getFirstAvailableDateForLocation(locationId, dose2DateMin, dose2DateMax, doseNumber=2)
            if dose2Date:
                dose2ReservationId, _, __ = getReservation(locationId, dose2Date, doseNumber=2)
                if dose2ReservationId:
                    confirmationCode = bookAppointment(dose1ReservationId, dose2ReservationId)
                    if confirmationCode:
                        printSuccess("Appointment Booked! Confirmation Code: " + confirmationCode)
                        return True
    printFail("Retry!")
    return False

def attemptAppointments():
    printNow()
    while not makeAppointment():
        time.sleep(5)
        printNow()

def monitorAvailability():
    while True:
        startDate = datetime.datetime.now().astimezone(timezone('US/Pacific')) + datetime.timedelta(hours=FIRST_DATE_OFFSET_HOURS)
        endDate = startDate + datetime.timedelta(days=7)
        startDate = startDate.strftime(query_date_format)
        endDate = endDate.strftime(query_date_format)
        for locationId, location in locations.items():
            locationQuery = getLocationQuery(locationId, startDate, endDate)
            locationResult = os.popen(locationQuery).read()
            printNow()
            if 'available' not in locationResult:
                printError("Update Vaccine Data:")
                beepy.beep(sound='robot_error')
                vaccineData = input()
            elif 'true' in locationResult:
                printSuccess("Vaccine Available")
                searchQuery = getSearchQuery(startDate)
                searchResult = os.popen(searchQuery).read()
                searchData = json.loads(searchResult)
                if len(searchData['locations']) > 0:
                    printSuccess('Searchable on Web')
                    beepy.beep(sound='success')
                else:
                    printFail('Unsearchable on Web')
                locationData = json.loads(locationResult)
                for dateAvailability in locationData['availability']:
                    if dateAvailability['available']:
                        printSuccess("Date: " + dateAvailability['date'], index=1)
                        query = getSlotsQuery(locationId, dateAvailability['date'])
                        slotResult = os.popen(query).read()
                        slotsData = json.loads(slotResult)
                        for slot in slotsData['slotsWithAvailability']:
                            printSuccess("Time: " + slot['localStartTime'], index=2)
                printSuccess("Location:" + location, index=1)
            else:
                printFail("Vaccine Not Available at " + location)
            time.sleep(5)

monitorAvailability()

# attemptAppointments()
