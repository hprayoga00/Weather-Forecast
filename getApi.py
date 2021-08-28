#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def jPrint(obj):
	#create a fromatted string of the Python JSON object
	text = json.dumps(obj, indent = 4)
	print(text)

def get_weather_data(city):
    url = "https://api.openweathermap.org/data/2.5/forecast?q={}&units=imperial&appid=c79b0f396d599f9c214529ba1ce9fa61"
    r = requests.get(url.format(city)).json()
    return r


@app.route('/', methods=['GET', 'POST'])
def index():
	city = ''
	weather_data = []
	err_msg = ''
	currentWeather = ''
	graphTempCelcius = []
	graphTempFarenheit = []
	graphHumidity = []
	graphTime = []
	if(request.method == 'POST'):
		city = request.form.get('city')
		if(city == ''):
			return render_template("index.html", weather_data=weather_data, current_weather=currentWeather)

		# Ambil Beberapa Jam ke Depan
		url = "https://api.openweathermap.org/data/2.5/forecast?q={}&units=imperial&appid=c79b0f396d599f9c214529ba1ce9fa61"
		dataApi = requests.get(url.format(city)).json()

		jPrint(dataApi)
		# dataApi = get_weather_data(city)

		if(dataApi['cod'] == "200"):
			counter = 0 # hitung cuaca yang diambil
			for data in dataApi['list']:
				date_time = datetime.datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
				current_time = datetime.datetime.now()
				if(date_time > current_time):
					temperatureCelcius = str(round(float((data['main']['temp'] - 32) * 5 / 9), 2))
					weather = {
						'city' : dataApi['city']['name'],
						'temperatureFarenheit' : data['main']['temp'],
						'temperatureCelcius' : temperatureCelcius,
						'description' : data['weather'][0]['description'],
						'icon' : data['weather'][0]['icon'],
						'time' : datetime.datetime.strptime(str(data['dt_txt']), '%Y-%m-%d %H:%M:%S').strftime("%H:%M %d-%m-%Y"),
						'timeHour' : datetime.datetime.strptime(str(data['dt_txt']), '%Y-%m-%d %H:%M:%S').strftime("%H:%M"),
						'timeDate' : datetime.datetime.strptime(str(data['dt_txt']), '%Y-%m-%d %H:%M:%S').strftime("%d-%b-%Y"),
					}
					# print(weather)
					graphTempCelcius.append(temperatureCelcius)
					graphTempFarenheit.append(data['main']['temp'])
					graphHumidity.append(data['main']['humidity'])
					weather_data.append(weather)
					graphTime.append(datetime.datetime.strptime(str(data['dt_txt']), '%Y-%m-%d %H:%M:%S').strftime("%H:%M"))
					counter += 1
				if(counter > 8):
					break
			
			# print("BERHASIL")
			# return render_template("index.html", weather_data=weather_data)

		else:
			print("GAGAL")
			err_msg = 'City does not exist in the world!'
		
		if err_msg:
			flash(err_msg, 'error')
		else:
			flash('City loaded succesfully!')
		
		# return render_template("index.html", weather_data=weather_data)

		# Ngambil current weather
		url2 = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c79b0f396d599f9c214529ba1ce9fa61"
		currentData = requests.get(url2.format(city)).json()
		# jPrint(currentData)

		if(currentData['cod'] == 200):
			temperatureCelciusCurrent = str(round(float((currentData['main']['temp'] - 32) * 5 / 9), 2))
			current_time = datetime.datetime.now()
			timeNow = datetime.datetime.strptime(str(current_time), '%Y-%m-%d %H:%M:%S.%f').strftime("%d-%b-%Y %H:%M")
			currentWeather = {
				'city' : currentData['name'],
				'temperatureCelcius' : temperatureCelciusCurrent,
				'temperatureFarenhait' : currentData['main']['temp'],
				'description' : currentData['weather'][0]['description'],
				'icon' : currentData['weather'][0]['icon'],
				'windSpeed' : currentData['wind']['speed'],
				'humidity' : currentData['main']['humidity'],
				'pressure' : currentData['main']['pressure'],
				'currentTime' : timeNow, 
			}
			# print(currentWeather)
			# print(graphTime)

	print(graphTempCelcius)
	return render_template("index.html", weather_data=weather_data,
											currentWeather=currentWeather,
											graphTempCelcius=graphTempCelcius,
											graphTempFarenheit=graphTempFarenheit,
											graphTime=graphTime,
											graphHumidity=graphHumidity)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=17131, debug=True)
