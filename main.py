from requests import get
import dash
import datetime
import plotly
import pandas as pd
from flask import Flask, render_template, request, jsonify
cords = []
key_loc = ""
app = Flask(__name__)
@app.route('/', methods=['PUT', 'GET', 'POST'])
def hey():
    if request.method == 'GET':
        return render_template('Hello.html')
@app.route('/add', methods=['PUT', 'GET', 'POST'])
def first():
    if request.method == 'GET':
        return render_template('LotButtons.html')
    else:
        try:
            a = abs(float(request.form['lat']))
            b = abs(float(request.form['lon']))
            name = request.form['name']
        except ValueError:
            return "Координаты введены в неправильном формате. Что бы успешно добавить точку снова перейди на /add и введи координаты в формате числа с разделенной точкой дробной частью. Если твоя точка в южном или западном полушарии, то вводи соответсвующие координаты с минусом."

        except TypeError:
            return "Координаты введены в неправильном формате. Что бы успешно добавить точку снова перейди на /add и введи координаты в формате числа с разделенной точкой дробной частью. Если твоя точка в южном или западном полушарии, то вводи соответсвующие координаты с минусом."
        if (a <= 90 and b <= 180):
            cords.append({'latitude': request.form['lat'], 'longitude': request.form['lon']})
            params = {
                'apikey': "AXzY1NnfgY5CsA1twPZYeeGm1TJkcJgU",
                'q': str(a) + ',' + str(b)
            }
            r = get('http://dataservice.accuweather.com/locations/v1/cities/geoposition/search', params=params)
            if r.status_code == 200:
                key_loc = r.json()['Key']
                apik = "AXzY1NnfgY5CsA1twPZYeeGm1TJkcJgU"
                url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + key_loc
                forecast = get(url, params={'apikey':apik, 'details':'true', 'metric':'true'}).json()['DailyForecasts']
                temp_data_max = []
                temp_data_min = []
                wind_data = []
                gust_data = []
                date = []
                print(forecast)
                for t in forecast:
                    temp_data_max.append(t['Temperature']['Maximum']['Value'])
                    temp_data_min.append(t['Temperature']['Minimum']['Value'])
                    wind_data.append(t['Day']['Wind']['Speed']['Value'])
                    gust_data.append(t['Day']['WindGust']['Speed']['Value'])
                    date.append(datetime.datetime.fromisoformat(t['Date']).strftime("%d.%m"))

                tmpmax = plotly.graph_objects.Figure()
                tmpmax.add_trace(plotly.graph_objects.Scatter(x=date, y=temp_data_max, mode='lines+markers', name='Линия'))
                tmpmax.update_layout(title='График максимальной температуры по дням', xaxis_title='День', yaxis_title='Температура, °C')
                graph_html1 = plotly.io.to_html(tmpmax, full_html=False)

                tmpmin = plotly.graph_objects.Figure()
                tmpmin.add_trace(plotly.graph_objects.Scatter(x=date, y=temp_data_min, mode='lines+markers', name='Линия'))
                tmpmin.update_layout(title='График минимальной температуры по дням', xaxis_title='День', yaxis_title='Температура, °C')
                graph_html2 = plotly.io.to_html(tmpmin, full_html=False)

                wnd = plotly.graph_objects.Figure()
                wnd.add_trace(
                    plotly.graph_objects.Scatter(x=date, y=wind_data, mode='lines+markers', name='Линия'))
                wnd.update_layout(title='График средней скорости ветра по дням', xaxis_title='День',
                                     yaxis_title='Средняя скорость, км/ч')
                graph_html3 = plotly.io.to_html(wnd, full_html=False)

                gst = plotly.graph_objects.Figure()
                gst.add_trace(
                    plotly.graph_objects.Scatter(x=date, y=gust_data, mode='lines+markers', name='Линия'))
                gst.update_layout(title='График средней скорости порывов ветра по дням', xaxis_title='День',
                                  yaxis_title='Средняя скорость порывов ветра, км/ч')
                graph_html4 = plotly.io.to_html(gst, full_html=False)

                return render_template('index.html', graphs=[graph_html1, graph_html2, graph_html3, graph_html4])
            else:
                return "Координаты введены в неправильном формате. Что бы успешно добавить точку снова перейди на /add и введи координаты в формате числа с разделенной точкой дробной частью. Если твоя точка в южном или западном полушарии, то вводи соответсвующие координаты с минусом."

        else:
            return "Координаты введены в неправильном формате. Что бы успешно добавить точку снова перейди на /add и введи координаты в формате числа с разделенной точкой дробной частью. Если твоя точка в южном или западном полушарии, то вводи соответсвующие координаты с минусом."


@app.route('/data', methods=['PUT', 'GET', 'POST'])
def data():
    if request.method == 'GET':
        return jsonify(cords)
if __name__ == '__main__':
    app.run(debug=True)




