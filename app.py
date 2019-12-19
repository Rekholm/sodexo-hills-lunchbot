from flask import Flask, request, Response, jsonify
import requests
from datetime import date, timedelta


def link(day, month, year):


    r = requests.get(
        f"https://www.sodexo.fi/ruokalistat/output/daily_json/60/{year}-{month}-{day}")
    
    coursesData = r.json()["courses"]
    z = 1
    food = []
    category = []
    flist = []

    while z != len(coursesData):
        category.append(coursesData[str(z)]["category"])
        food.append(coursesData[str(z)]["title_fi"])
        lunchToday = list(zip(category, food))
        z += 1

    for c, f in lunchToday:
        flist.append(f"{c}:\n{f}\n\n")
        teksti = "".join(flist)

    return teksti


def today():
    
    today = date.today()

    d = today.strftime("%d")  # Day
    m = today.strftime("%m")  # Month
    y = today.strftime("%Y")  # Year
    courseData = link(d.rstrip(""),m.rstrip(""),y.rstrip(""))

    return courseData


def tomorrow():

    tomorrow = date.today() + timedelta(days=1)
    tomorrow = str(tomorrow)
    tomorrow = tomorrow.split("-")
    
    d = tomorrow[2]  # Day
    m = tomorrow[1]  # Month
    y = tomorrow[0]  # Year

    courseData = link(d.rstrip(""),m.rstrip(""),y.rstrip(""))
    return courseData


def yesterday():

    yesterday = date.today() - timedelta(days=1)
    yesterday = str(yesterday)
    yesterday = yesterday.split("-")
    
    d = yesterday[2]  # Day
    m = yesterday[1]  # Month
    y = yesterday[0]  # Year

    courseData = link(d.rstrip(""),m.rstrip(""),y.rstrip(""))
    return courseData


app = Flask(__name__)

@app.route('/lunch', methods=['POST'])
def lunch():
    text = request.form.get('text', '')
    if 'today' in text.lower() and today() not in text: # Return today()
        return {"text": f"{today()}"}  # DYI JSON
    if 'tomorrow' in text.lower() and tomorrow() not in text:
        return {"text": f"{tomorrow()}"}  # DYI JSON
    if 'yesterday' in text.lower() and yesterday() not in text:
        return {"text": f"{yesterday()}"}  # DYI JSON
    return Response(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
