from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from pprint import pprint
from ticketmasterapi import search_events
from flask_session import Session
import git


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Configure session to use the filesystem
Session(app)

def validateInput(zip_city, start_date, end_date):
    #checks if zip_city is a zipcode
    if zip_city.isdigit():
        if len(zip_city) != 5:
            return "Error: Zipcode must be 5 digits"
    
    #check start_date and end_date formats
    try:
        datetime.strptime(start_date, "%m/%d/%Y")
        datetime.strptime(end_date, "%m/%d/%Y")

    except ValueError:
        return "Please enter the date in the correct format"
    
    start = datetime.strptime(start_date, "%m/%d/%Y")
    end = datetime.strptime(end_date, "%m/%d/%Y")

    if end < start:
        return "Error: start date must be before end date"

# Custom Jinja2 filter
def format_date(value):
    date_obj = datetime.strptime(value, "%Y-%m-%d")
    return date_obj.strftime("%m-%d-%Y")

app.jinja_env.filters['format_date'] = format_date
   
# Default home page
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        zip_city = request.form.get("zip_city")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        query = request.form.get("query")
        
        errorstring = validateInput(zip_city, start_date, end_date)
        if errorstring:
            return render_template('home.html', error=errorstring)

        event_info = search_events(zip_city, start_date, end_date, query)
        session['event_info'] = event_info
        return redirect(url_for('results'))

    return render_template('home.html')

@app.route("/results", methods=["GET", "POST"])
@app.route("/results/<int:page>", methods=["GET", "POST"])
def results(page=1):
    if request.method == "POST":
        if request.form['button'] == 'prevPage':
            page = max(page - 1, 1)
        elif request.form['button'] == 'nextPage':
            page += 1
        return redirect(url_for("pagination", pageNumber=page))
    
    # Handle GET request to show results page
    event_info = session.get('event_info')
    return render_template('results.html', event_info=event_info, page=page)

@app.route("/results/<int:pageNumber>", methods=["POST"])
def pagination(pageNumber):
    zip_city = session['event_info']['zip_city']
    start_date = session['event_info']['start_date']
    end_date = session['event_info']['end_date']
    query = session['event_info']['query']
    
    errorstring = validateInput(zip_city, start_date, end_date)
    if errorstring:
        return render_template('results.html', error=errorstring)

    event_info = search_events(zip_city, start_date, end_date, query, pageNumber)
    session['event_info'] = event_info
    return redirect(url_for('results', page=pageNumber))

if __name__ == '__main__':
    app.run(debug=True)