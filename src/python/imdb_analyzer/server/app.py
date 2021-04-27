import sys,os
from fastapi import FastAPI,HTTPException
from analyzer import *
import pandas as pd
from fastapi.responses import HTMLResponse

data_path = f"{os.environ.get('DATA_DIR')}/{os.environ.get('DATA_FILE')}"

data_file = FileHandler(data_path)
data = data_file.get_data()
del(data_file)
all_actors = union_actor_columns(data)
app = FastAPI()

@app.get("/actors/{name}",response_class=HTMLResponse)
async def find_actor(name:str):
    try:
        # actor = all_actors[all_actors['actor_name']==name]
        actor = data[(data['actor_1_name']==name) | (data['actor_2_name']==name) | (data['actor_3_name']==name)]
    except Exception as e:
        raise HTTPException(status_code=404, detail={"error":"Actor Not Found"})
    return actor.to_html()

@app.get("/actors/financial/{name}",response_class=HTMLResponse)
async def find_actor(name:str):
    try:
        # actor = all_actors[all_actors['actor_name']==name]
        actor_films = all_actors[all_actors['actor_name']==name]
        actor = calculate_top_gross_profit(data_frame=actor_films,colnames=['actor_name'],top_n=1)
    except Exception as e:
        
        raise HTTPException(status_code=404, detail={"error":"Actor Not Found"})
    return actor.to_html()

@app.get("/actors/top/{n}",response_class=HTMLResponse)
async def find_actor(n:int):
    if not n: n=10
    try: 
        return calculate_top_gross_profit(data_frame=all_actors,colnames=['actor_name'],top_n=n).to_html() 
    except Exception as e:
        raise HTTPException(status_code=500, detail="zzzzzz")

@app.get("/genres/top/{n}",response_class=HTMLResponse)
async def find_actor(n:int):
    if not n: n=10
    try:
        return calculate_top_gross_profit(data_frame=data,colnames=['genres'],top_n=n).to_html()
    except Exception as e:
        raise HTTPException(status_code=500, detail="zzzzzz")