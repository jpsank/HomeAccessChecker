# HomeAccessChecker
Application that lets you more easily login to ESchool Home Access Center to view your grades/schedule

# About
You can use this app to view your grades and schedule on [ESchool HAC](https://hac31.eschoolplus.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f). If you just want to quickly check something, this is much easier to use than the website.

# Prerequisites
You will need [requests](http://docs.python-requests.org/en/master/), [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and [Pillow](https://python-pillow.org). You can use pip to get them

    pip install requests beautifulsoup4 Pillow

# Usage
To run, type

    python main.py

And it will ask you for your school district, username, and password. Once you enter these, they will be saved, so you don't have to enter them again!

