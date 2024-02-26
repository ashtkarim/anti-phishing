# from urllib.parse import urlparse
from flask import Flask, request, render_template
from flask_cors import CORS
"""
from ML.Detection import FeaturesExtraction
import requests
import numpy as np
import pickle
import sqlite3
import pandas as pd
import xgboost
"""
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
'''
model = pickle.load(open('ML/hybrid1.pickle.dat', 'rb'))

def MLwork(url):
    try:
        response = requests.get(url, timeout=5)
        print("done")
        
        features = FeaturesExtraction(url, response)
        print("Features extracted:", features)
        
        features = np.array(features).reshape(1, -1)

        if int(model.predict(features)) == 0:
            output = "legitimate"
        else:
            output = "phishing"
    except Exception as e:
        print(e)
        output = "Error in Scraping"
    return output

def VerifyRank(url):
    dat = pd.read_csv("rank.csv").values.tolist()
    if urlparse(url).netloc in dat:
        return "legitimate"
    else:
        return None

def VerifyDB(url):
    conn = sqlite3.connect("lien.db")
    cursorobj = conn.cursor()
    cursorobj.execute(f"SELECT label FROM liens WHERE urls = '{url}'")
    row = cursorobj.fetchall()
    conn.close()
    
    if len(row) == 0:
        return None
    else:
        return row[0]

def AddToDatabase(lien, out):
    conn = sqlite3.connect("lien.db")
    cursorobj = conn.cursor()
    cursorobj.execute(f"INSERT INTO liens(urls, label) VALUES ('{lien}', '{out}')")
    conn.close()
def get_all_db():
conn = sqlite3.connect("lien.db")
    cursorobj = conn.cursor()
    cursorobj.execute(f"SELECT * FROM liens WHERE label = 'phishing'")
    row = cursorobj.fetchall()
    conn.close()


'''
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=="POST":
        try:
            data = request.get_json()
            # Access JSON data using keys, for example:
            url = data.get('url')
        
            '''
            if not url:
                return render_template('index.html', output="")

            if VerifyDB(url) is None:
                if VerifyRank(url) is None:
                    out = MLwork(url)
                    AddToDatabase(url, out)
                else:
                    out = "legitimate"
            else:
                out = VerifyDB(url)
            '''
            out='false'
            return {'url':url,'out':out}
        except :
            return {'error':'error'}

    else:
        return {}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
