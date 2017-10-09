import requests
from bs4 import BeautifulSoup


def scrapeOptions():
    url = "https://hac31.eschoolplus.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f"
    r = requests.get(url)
    page = BeautifulSoup(r.text, "html5lib")
    options = page.select("option")
    if options:
        return {o.text:o.get("value") for o in options}


def checkOption(o,options=None):
    if options is None:
        options = scrapeOptions()
    else:
        options = options.copy()
    for item in options.items():
        if o.lower() not in item.lower():
            del options[item]
    return options


def printColumns(data,padding=2):
    if isinstance(data, dict):
        title_width = max(len(key) for key in data) + padding
        col_width = max(len(word) for key in data for word in data[key]) + padding
        for key in data:
            print(key.ljust(title_width),end="")
            print("".join(word.ljust(col_width) for word in data[key]))
    else:
        col_width = max(len(word) for row in data for word in row) + padding
        for row in data:
            print("".join(word.ljust(col_width) for word in row))


def scrapeHome(username, password, district):
    payload = {'LogOnDetails.UserName': username, 'LogOnDetails.Password': password, "Database": district}
    url = "https://hac31.eschoolplus.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f"
    p = requests.post(url, data=payload)
    page = BeautifulSoup(p.text, "html5lib")
    tables = page.select("table.sg-homeview-table")
    if tables:
        tds = tables[0].select("td")
        result = [' '.join(td.stripped_strings) for td in tds]
        result = [result[i:i+7] for i in range(0,len(result),7)]
        return result


def scrapeSchedule(username,password, district):
    session = requests.Session()
    payload = {'LogOnDetails.UserName': username, 'LogOnDetails.Password': password, "Database": district}
    url = "https://hac31.eschoolplus.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f"
    session.post(url, data=payload)
    p = session.get("https://hac31.eschoolplus.k12.ar.us/HomeAccess/Content/Student/Classes.aspx")
    page = BeautifulSoup(p.text, "html5lib")
    tables = page.select("table#plnMain_dgSchedule")
    if tables:
        tds = tables[0].select("td")
        result = [' '.join(td.stripped_strings) for td in tds]
        result = [result[i:i+9] for i in range(0, len(result), 9)]
        return result


# data = scrapeHome(input('user: '),input("pass: "))
# print(data)
# printColumns(data)
