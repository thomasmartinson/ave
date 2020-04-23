from flask import Flask, render_template, url_for
from datetime import datetime

import calendar

app = Flask(__name__)

HEADS_UP_DAYS = 15

shifts = [
    {
        'volunteer': 'Alice A.',
        'date': 'April 22, 2020',
        'role': 'lector'
    },
    {
        'volunteer': 'Bob B.',
        'date': 'March 23, 2020',
        'role': 'lector'
    },
    {
        'volunteer': 'Charlie C.',
        'date': 'April 24, 2020',
        'role': 'lector'
    }
]


volunteers = [
    {
        'name': 'Alice A.',
        'netid': 'aaa',
        'days': [0, 1, 3],
        'roles': ['lector', 'collection'],
        'shifts': []
    },
    {
        'name': 'Bob B.',
        'netid': 'bbb',
        'days': [0, 2, 4, 5],
        'roles': ['lector', 'collection'],
        'shifts': []
    },
    {
        'name': 'Charlie C.',
        'netid': 'ccc',
        'days': [0],
        'roles': ['lector', 'collection'],
        'shifts': []
    },
    {
        'name': 'Diana D.',
        'netid': 'ddd',
        'days': [0],
        'roles': ['lector', 'collection'],
        'shifts': []
    }
]


# takes in datetime object
# returns the days in 
def get_services_for_day(date):
    # no events in July or August
    if date.month in (7, 8):
        return []

    # weekday Masses
    if date.weekday() in range(1, 5):
        return [
            {
                'title': '12 PM Daily Mass',
                'time': date.replace(hour=12, minute=0),
                'roles': [
                    {
                        'title': 'Lector',
                        'type': 'lector',
                        'num': 1
                    }
                ]
            }
        ]

    # Sunday Masses
    if date.weekday() is 0: 
        return [
            {
                'title': '4:30 PM Sunday Mass',
                'time': date.replace(hour=16, minute=30),
                'roles': [
                    {
                        'title': '1st Reading',
                        'type': 'lector',
                        'num': 1
                    },
                    {
                        'title': '2nd Reading',
                        'type': 'lector',
                        'num': 1
                    },
                    {
                        'title': 'Collection',
                        'type': 'collection',
                        'num': 2
                    }
                ]
            },
            {
                'title': '10 PM Sunday Mass',
                'time': date.replace(hour=22, minute=0),
                'roles': [
                    {
                        'title': '1st Reading',
                        'type': 'lector',
                        'num': 1
                    },
                    {
                        'title': '2nd Reading',
                        'type': 'lector',
                        'num': 1
                    },
                    {
                        'title': 'Collection',
                        'type': 'collection',
                        'num': 2
                    }
                ]
            }
        ]


# takes in a datetime object
# assigns volunteers to each shift in the month
# def make_assignments_for(date):
#     days = []
    
#     this_day = date.replace(day=1)
#     while this_day.day <= days_in_month(date):
#         services = services = get_services_for(this_day)
#         days.append(services)
#         # for service in services:
#         #     for role in service['roles']:
#         #         assignments.append(
#         #             {
#         #                 'title': role['title'],
#         #                 'volunteers': ['none' for i in range(role['num'])]
#         #             }
#         #         )
    
#     return 
            

# takes in a datetime object
# returns the number of days in its month
def days_in_month(date):
    return calendar.monthrange(date.year, date.month)[1]


# takes in a datetime object
# returns the volunteers for that month
def get_services_for_month(date):
    days = []

    for day in range(1, days_in_month(date)):
        this_day = date.replace(day=day)
        events = get_services_for_day(this_day)
        days.append(events)

    return days



# takes in a datetime object
# returns a dict for that month in ideal format to display on homepage
def make_month_dict(date):
    month = { 
        'title': '{} {}'.format(date.strftime('%B'), date.year),
        'weeks': [],
        'num_days': days_in_month(date), # day of month
        'services': get_services_for_month(date)
    }

    first_day = date.replace(day=1).weekday() # day of week
    
    # insert the week lists
    for wk in range(7):
        month['weeks'].append([i - first_day + 7 * wk for i in range(7)])
        if month['weeks'][-1][-1] >= days_in_month(date):
            break # avoid empty weeks
    
    return month


# rendering the home page
@app.route('/')
def home():
    dt_now = datetime.now()
    dt_next_month = dt_now.replace(day=1).replace(month=dt_now.month % 12 + 1)

    this_month = make_month_dict(dt_now)
    next_month = {}

    # display next month if less than a certain number of days away
    if (this_month['num_days'] - HEADS_UP_DAYS <= dt_now.day):
        next_month = make_month_dict(dt_next_month)

    return render_template('home.html', month=this_month, next_month=next_month)


# extra test page
@app.route('/mean/')
def get_lost():
    return 'Get Lost, stupid!'


if __name__ == '__main__':
    app.run(debug=True)