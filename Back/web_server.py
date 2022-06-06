import json
import urllib

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from pydantic import BaseModel

from dashapp import create_dash_app

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_main():
    return {
        "routes": [
            {"method": "GET", "path": "/", "summary": "Landing"},
            {"method": "GET", "path": "/status", "summary": "App status"},
            {"method": "GET", "path": "/dash", "summary": "Sub-mounted Dash application"},
            {"method": "GET", "path": "/graph-pure-plotly", "summary": "Plotly Graph"},
        ]
    }

@app.get("/status")
def get_status():
    return {"status": "ok"}

@app.get("/graph-student-bar")
def get_graph():
    details = {
        'Student': [ "S1 ",
                     "S2  ",
                     "S3  ",
                     "S4  ",
                     "S5  "],
        'Grade': [80, 90, 35, 55, 56],
        'Expected': [100, 100, 100, 100, 100]
        }
    df = pd.DataFrame(details)            
    gas_figure = go.Figure(go.Bar(
        x=df["Expected"], y=df["Student"],
        hovertemplate = 'Student: %{y}'+'<br>Expected: %{x}<br>'+'Grade: %{text}',
        text = [' {}%'.format(i) for i in df['Grade']],
        orientation='h'
    ))
    return json.loads(gas_figure.to_json())

@app.get("/graph-pure-plotly/{item_id}")
def get_graph(item_id: int):
    item = {0: 'BHU', 1: 'JNU', 2: 'DU'}
    details = {
        'Date': ['2017-12-25', '2017-12-26', '2017-12-27', '2017-12-28', '2017-12-25', '2017-12-26', '2017-12-27', '2017-12-28', '2017-12-25', '2017-12-26', '2017-12-27', '2017-12-28'],
        'Students': ['BHU', 'BHU', 'BHU', 'BHU', 'JNU', 'JNU', 'JNU', 'JNU', 'DU', 'DU', 'DU', 'DU'],
        'Grade': [80, 90, 35, 55, 56, 77, 66, 45, 80, 90, 35, 55]
    }
    df = pd.DataFrame(details)
    dff = df[df['Students'] == item[item_id]]

    gas_figure = px.line(
        dff, x="Date", y="Grade", color="Students"
    )

    return json.loads(gas_figure.to_json())


dash_app = create_dash_app(requests_pathname_prefix="/dash/")
app.mount("/dash", WSGIMiddleware(dash_app.server))

class Info(BaseModel):
    id: int
    name: str


@app.post("/recipe")
def getInformation(info: Info):
    return {
        "status": "SUCCESS",
        "data": info
    }

    # Streaming response  async
    # Devolver un binario
