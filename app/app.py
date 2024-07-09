from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

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

        # return redirect(url_for('results'))
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)

