from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from pprint import pprint
from ticketmasterapi import search_events

app = Flask(__name__)

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
      
#default home page
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

        event_info= search_events(zip_city, start_date, end_date, query)
        pprint(event_info)
        #return redirect(url_for('results', event_data=event_data))
    
    return render_template('home.html')

@app.route("/results")
def results():
    event_data = request.args.get('event_data')  # Retrieve event_data from query parameters

    print(event_data)# CHANGE TO PROCESS EVENT DATA

    return render_template('results.html', event_data=event_data)


if __name__ == '__main__':
    app.run(debug=True)

