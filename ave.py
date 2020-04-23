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

# takes in a datetime object
# returns the volunteers for that month
def get_volunteers_for(time):
    return [i for i in shifts if i['date'].split()[0] == time.strftime('%B')]


# takes in a datetime object
# returns a dict for that month in ideal format to display on homepage
def make_month_dict(time):
    month = { 
        'title': '{} {}'.format(time.strftime('%B'), time.year),
        'weeks': [],
        'last_day': calendar.monthrange(time.year, time.month)[1], # day of month
        'volunteers': get_volunteers_for(time)
    }

    first_day = time.replace(day=1).weekday() # day of week
    
    # insert the week lists
    for wk in range(7):
        month['weeks'].append([i - first_day + 7 * wk for i in range(7)])
        if month['weeks'][-1][-1] >= month['last_day']:
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
    if (this_month['last_day'] - HEADS_UP_DAYS <= dt_now.day):
        next_month = make_month_dict(dt_next_month)

    return render_template('home.html', month=this_month, next_month=next_month)


# extra test page
@app.route('/mean/')
def get_lost():
    return 'Get Lost, stupid!'


if __name__ == '__main__':
    app.run(debug=True)