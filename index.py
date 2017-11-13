from flask import Flask,request
from flask import render_template,make_response
import json
import os
import tools
app = Flask(__name__)
json_location = "json/data.json"

def loadJsonFile():
    if os.path.exists(json_location):
        with open(json_location, 'rb') as f:
            rep = f.read()
            return rep
    else:
        open(json_location, 'w').close()
        return "[]"

@app.route("/")
def index():
    return render_template('portal.html')

@app.route("/left")
def left():
    return render_template('left.html')

@app.route("/right")
def right():
    date_time = tools.parseJsonFile_cutdowntime()
    date_obj = json.loads(date_time)
    return render_template('right.html',year=date_obj["year"],month=date_obj["month"],day=date_obj["day"])


@app.route("/addjson")
def addjson():
    data = request.args.get("data")
    result = json.loads(data)
    all_data = json.loads(loadJsonFile())
    if result["parentNode"].strip() and result["parentNode"].strip() in [child["name"].strip() for child in all_data] and (result["name"] != "" or result["url"] != ""):
        for item in all_data:
            if result["parentNode"].strip() == item["name"]:
                flag = True
                for sub in item["subContent"]:
                    if sub["name"] == result["name"] and result["url"] == "":
                        item["subContent"].remove(sub)
                        flag = False
                    elif sub["name"] == result["name"] and result["url"] != "":
                        sub["url"] = result["url"]
                        flag = False
                if flag:
                    del result["parentNode"]
                    item["subContent"].append(result)

    elif result["parentNode"].strip() and result["name"].strip() == "" and result["url"].strip() == "" :
        for item in all_data:
            if item["name"] == result["parentNode"]:
                all_data.remove(item)

    else:
        del result["parentNode"]
        result["subContent"] = []
        all_data.append(result)

    with open(json_location,"wb") as f:
        json.dump(all_data,f)

    return "success"

@app.route("/getjson")
def getjson():
    if os.path.exists(json_location):
        with open(json_location, 'rb') as f:
            rep = f.read()
            return rep
    else:
        return "[]"

@app.route("/login")
def login():
    date_time = tools.parseJsonFile_cutdowntime()
    date_obj = json.loads(date_time)
    info = request.args.get("info","null")
    user = "null"
    if info and info != "null":
        if info.split('/')[0] == "zerg" and info.split('/')[1] == "zerg":
            user = "zerg"
        else:
            user = "fail"
    return render_template('admin_login.html',user=user)



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
