import pandas as pd
from fastapi import FastAPI
import requests
from io import StringIO

app = FastAPI()

# Ton URL Google Sheet publiée en CSV
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVmhuBTc1tIfFQE8S7oHaP_8O0ObqVy0URx54fuEto5sIFGkf43nIaD7LTumSL2Ks5RT7_FgvNAFMQ/pub?gid=1038856094&single=true&output=csv"

def get_live_data():
    # Cette fonction lit ton fichier réel sur le Web
    response = requests.get(CSV_URL)
    return pd.read_csv(StringIO(response.text))

@app.get("/data")
def read_data(page: int = 1, limit: int = 10):
    df = get_live_data()

    # On remplace tous les NaN par une chaîne vide ou 0 pour que le JSON soit valide
    df = df.fillna("")
    
    # On calcule où commence et s'arrête la "page" demandée
    start = (page - 1) * limit
    end = start + limit
    
    # On découpe le DataFrame (Pandas)
    chunk = df.iloc[start:end]
    
    return {
        "total_rows": len(df),
        "current_page": page,
        "data": chunk.to_dict(orient="records")
    }
