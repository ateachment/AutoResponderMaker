import json
import urllib.request
import ssl

from datetime import datetime, date, timedelta
import calendar
import dateutil

ssl._create_default_https_context = ssl._create_unverified_context

def getHoliday(year: str, germanCountryCode: str):

    dates = []

    # single holidays

    source_url = f"https://feiertage-api.de/api/?jahr={year}&nur_land={germanCountryCode}"
    with urllib.request.urlopen(source_url) as url:
        data: str = json.loads(url.read().decode())

    print(json.dumps(data, indent = 4, sort_keys=True))


    for holiday in data:         # iterate
        dates.append(data[holiday]['datum'])
        print (data[holiday]['datum'])


    # school holidays 
    
    source_url = f"https://ferien-api.de/api/v1/holidays/{germanCountryCode}/{year}"
    with urllib.request.urlopen(source_url) as url:
        data: str = json.loads(url.read().decode())

    print(json.dumps(data, indent = 4, sort_keys=True))

    datesOfYear = [datetime(int(year), 1, 1) + timedelta(days=idx) for idx in range(400)]
    #for dt in datesOfYear:
        #print(type(dt))
    #print(datesOfYear)
    for holiday in data:         # iterate
        for dt in datesOfYear:
            #print(datetime.fromisoformat(holiday['start'].split('T')[0]))
            if datetime.fromisoformat(holiday['start'].split('T')[0]) <= dt and datetime.fromisoformat(holiday['end'].split('T')[0]) >= dt:
                if dates.count(str(dt.date())) == 0:
                    dates.append(str(dt.date()))
                    print(dt.date())

    

    # weekends
    A=calendar.TextCalendar(calendar.SUNDAY)
    for b in range(1,13):
        for k in A.itermonthdays(int(year),b):
            if k!=0:
                day=datetime(int(year),b,k)
                if day.weekday()==5 or day.weekday()==6:
                    #print("%d-%d-%s" % (k,b,year))
                    if dates.count(str(day.date())) == 0:
                        dates.append(str(day.date()))
                        print(day.date())

    dates.sort()
    print(dates)

if __name__ == '__main__':
    getHoliday("2022", "HE")