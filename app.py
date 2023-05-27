from asyncio.windows_events import NULL
from urllib.parse import urlparse
from flask import Flask, request, render_template
from ML.Detection import FeaturesExtraction
import requests
import numpy as np
import pickle
import sqlite3
import pandas as pd
from urllib.parse import urlparse
import xgboost
# from sklearn.preprocessing import *

app = Flask(__name__,static_folder="./templates")
model = pickle.load(open('ML\hybrid1.pickle.dat','rb'))

def MLwork(url):
    try:
        output="---"
        response = requests.get(url,timeout=5)
        print("donne")
        features = FeaturesExtraction(url,response)
        print("wi",features)
        features = np.array(features).reshape(1,-1)
        print("Features extracted:", features)
        

        if int(model.predict(features)) == 0:
            output = "legitimate"
        else:
            output = "phishing"
    except Exception as e:
        print(e)
        output="Erreur dans Scraping "
    return output

def VerifyRank(url):
    dat=pd.read_csv("rank.csv").values.tolist()
    if urlparse(url).netloc in dat:
        return "legitimate"
    else:
        return NULL

def VerifyDB(url):
    conn=sqlite3.connect("lien.db")
    cursorobj=conn.cursor()
    cursorobj.execute(f"select label from liens where urls='{url}'")
    row=cursorobj.fetchall()
    conn.close()
    if len(row)==0:
        return NULL
    else:
        return row[0]

def AddToDatabase(lien,out):
    conn=sqlite3.connect("lien.db")
    cursorobj=conn.cursor()
    cursorobj.execute(f"insert into liens(urls,label) values('{lien}','{out}')")
    conn.close()

@app.route('/',methods=['GET','POST'])
def home():
    url = request.form.get("url")
    if not url:
        return render_template('index.html', output="")

    if(VerifyDB(url)==NULL):
        if(VerifyRank(url)==NULL):
            out=MLwork(url)
            AddToDatabase(url,out)
        else:
            out="legitimate"
    else:
        out=VerifyDB(url)
    
        

    return render_template('index.html', output=out )

if __name__ == "__main__":
    app.run(debug=True, port=3000)