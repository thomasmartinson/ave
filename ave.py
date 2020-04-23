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
        'date': 'April 23, 2020',
        'role': 'lector'
    },
    {
        'volunteer': 'Charlie C.',
        'date': 'April 24, 2020',
        'role': 'lector'
    }
]


# rendering the home page
@app.route('/')
def home():
    # returns a dict for the month in ideal format to display on homepage
    # the returned month corresponds to the given datetime object
    def make_month_dict(time):
        month = { 
            'title': '{} {}'.format(time.strftime('%B'), time.year),
            'weeks': [],
            'last_day': calendar.monthrange(time.year, time.month)[1] # day of month
        }

        first_day = time.replace(day=1).weekday() # day of week
        
        # insert the week lists
        for wk in range(7):
            month['weeks'].append([i - first_day + 7 * wk for i in range(7)])
            if month['weeks'][-1][-1] >= month['last_day']:
                break # avoid empty weeks

        return month

    now = datetime.now()
    month = make_month_dict(now)

    # display next month if less than a certain number of days away
    next_month = {}
    if (month['last_day'] - HEADS_UP_DAYS <= now.day):
        next_month = make_month_dict(now.replace(day=1).replace(month=now.month % 12 + 1))

    return render_template('home.html', shifts=shifts, month=month, next_month=next_month)


# extra test page
@app.route('/mean/')
def get_lost():
    return 'Get Lost, stupid!'


if __name__ == '__main__':
    app.run(debug=True)