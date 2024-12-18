"""Web app."""
import flask
from flask import Flask, render_template, request, redirect, url_for

import pickle
import base64
from training import prediction
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = flask.Flask(__name__)

data = [{'name':'Delhi', "sel": "selected"}, {'name':'Mumbai', "sel": ""}, {'name':'Kolkata', "sel": ""}, {'name':'Bangalore', "sel": ""}, {'name':'Chennai', "sel": ""}]
# data = [{'name':'India', "sel": ""}]
months = [{"name":"May", "sel": ""}, {"name":"June", "sel": ""}, {"name":"July", "sel": "selected"}]
cities = [{'name':'Delhi', "sel": "selected"}, {'name':'Mumbai', "sel": ""}, {'name':'Kolkata', "sel": ""}, {'name':'Bangalore', "sel": ""}, {'name':'Chennai', "sel": ""}, {'name':'New York', "sel": ""}, {'name':'Los Angeles', "sel": ""}, {'name':'London', "sel": ""}, {'name':'Paris', "sel": ""}, {'name':'Sydney', "sel": ""}, {'name':'Beijing', "sel": ""}]

model = pickle.load(open("model.pickle", 'rb'))
print(model)
@app.route("/")
@app.route('/index.html')
def index() -> str:
    """Base page."""
    return flask.render_template("index.html")

@app.route('/plots.html')
def plots():
    return render_template('plots.html')

@app.route('/heatmaps.html')
def heatmaps():
    return render_template('heatmaps.html')

@app.route('/my_plant_reading.html')
def my_plat_reading():
    return render_template('my_plant_reading.html')

@app.route('/satellite.html')
def satellite():
    direc = "processed_satellite_images\Delhi_July.png"
    with open(direc, "rb") as image_file:
        image = base64.b64encode(image_file.read())
    image = image.decode('utf-8')
    return render_template('satellite.html', data=data, image_file=image, months=months, text="Delhi in January 2020")

@app.route('/satellite.html', methods=['GET', 'POST'])
def satelliteimages():
    place = request.form.get('place')
    date = request.form.get('date')
    data = [{'name':'Delhi', "sel": ""}, {'name':'Mumbai', "sel": ""}, {'name':'Kolkata', "sel": ""}, {'name':'Bangalore', "sel": ""}, {'name':'Chennai', "sel": ""}]
    months = [{"name":"May", "sel": ""}, {"name":"June", "sel": ""}, {"name":"July", "sel": ""}]
    for item in data:
        if item["name"] == place:
            item["sel"] = "selected"
    
    for item in months:
        if item["name"] == date:
            item["sel"] = "selected"

    text = place + " in " + date + " 2020"

    direc = "processed_satellite_images\{}_{}.png".format(place, date)
    with open(direc, "rb") as image_file:
        image = base64.b64encode(image_file.read())
    image = image.decode('utf-8')
    return render_template('satellite.html', data=data, image_file=image, months=months, text=text)

@app.route('/predicts.html')
def predicts():
    return render_template('predicts.html', cities=cities, cityname="Information about the city")

@app.route('/predicts.html', methods=["GET", "POST"])
def get_predicts():
    try:
        cityname = request.form["city"]
        cities = [{'name':'Delhi', "sel": ""}, {'name':'Mumbai', "sel": ""}, {'name':'Kolkata', "sel": ""}, {'name':'Bangalore', "sel": ""}, {'name':'Chennai', "sel": ""}, {'name':'New York', "sel": ""}, {'name':'Los Angeles', "sel": ""}, {'name':'London', "sel": ""}, {'name':'Paris', "sel": ""}, {'name':'Sydney', "sel": ""}, {'name':'Beijing', "sel": ""}]
        for item in cities:
            if item['name'] == cityname:
                item['sel'] = 'selected'
        print(cityname)

        URL = "https://geocode.search.hereapi.com/v1/geocode"
        print(URL)
        API_KEY='wRXOXpuB7mFGMSHWCARdDELdakdVJYYe2SWSoRwIGdw'
        PARAMS = {
            'q': cityname,
            'limit': 4,
            'apiKey': API_KEY

        }
        # sending get request and saving the response as response object 
        r = requests.get(url = URL, params = PARAMS) 
        print(r)
        print(r.json())
        data = r.json()
        latitude = data['items'][0]['position']['lat']
        longitude = data['items'][0]['position']['lng']
        print(latitude)
        print(longitude)
        final = prediction.get_data(latitude, longitude)
        final[4] *= 15
        if str(model.predict([final])[0]) == "0":
            pred = "Safe"
        else:
            pred = "Unsafe"

        sender_email = "sanjayr33318@gmail.com"  # Replace with your Gmail
        sender_password = "hnzb bwrf qpdw sryf"  # Replace with your Gmail password or app password
        subject = f"Flood Prediction Results"
        body = f"""
        Here are the prediction results for {cityname}:

        Temperature: {round(final[0], 2)}°C
        Max Temperature: {round(final[1], 2)}°C
        Wind Speed: {round(final[2], 2)} km/h
        Cloud Cover: {round(final[3], 2)}%
        Precipitation: {round(final[4], 2)} mm
        Humidity: {round(final[5], 2)}%
        Prediction: {pred}

        Stay safe,
        FloodML Team
        """

        # Sending email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = 'varshithamunegowda@gmail.com'
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return render_template('predicts.html', cityname="Information about " + cityname, cities=cities, temp=round(final[0], 2), maxt=round(final[1], 2), wspd=round(final[2], 2), cloudcover=round(final[3], 2), percip=round(final[4], 2), humidity=round(final[5], 2), pred=pred)
    except Exception as e:
        print(e)
        return render_template('predicts.html', cities=cities, cityname="Oops, we weren't able to retrieve data for that city.")



if __name__ == "__main__":
    app.run(debug=True)