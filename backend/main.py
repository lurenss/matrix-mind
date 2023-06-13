from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import io
import pandas as pd
from pydantic import BaseModel
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_csv_agent

#initialization
app = FastAPI()
credentials = False
path_df = None
csv_agent = None


## add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item_api(BaseModel):
    apiKey: str
    model: str

class Item_msg(BaseModel):
    msg: str

@app.post("/api-key")
def process_api_key(item: Item_api):
    # try to process the api key and model with langchain
    try:
        os.environ["OPENAI_API_KEY"] = item.apiKey
        llm = OpenAI(temperature = 0.1)
        text = "What would be a good company name for a company that makes colorful socks?"
        print(llm(text))
        global credentials
        credentials = True
    except: 
        raise HTTPException(status_code=400, detail="Invalid API Key or model. Please try again.")
    return {"message": "API Key and model processed"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if  credentials == False:
        raise HTTPException(status_code=400, detail="Please process your API Key and model first.")

    if file.filename.endswith('.csv'):
        data = await file.read()
        data_stream = io.StringIO(data.decode("utf-8"))
        df_uploaded = pd.read_csv(data_stream)
        print(df_uploaded.head()) # prints the first 5 rows of the dataframe
        # write the df to a file
        global path_df
        path_df = os.path.join(os.getcwd(), file.filename)
        df_uploaded.to_csv(path_df, index=False)
        
        return {"filename": file.filename}
    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV files are accepted.")
    
@app.get("/first_generate")
def first_generate():
    while True:
        try:
            global path_df
            global csv_agent
            csv_agent = create_csv_agent(
                ChatOpenAI(temperature=0),
                path_df
            )
            user_msg = "Try to describe what is this CSV file about starting from the name of the columns."
            msg = csv_agent.run(user_msg)
            print("USER: " + user_msg)
            print("AI: " + msg)
            return {"message": msg}
        except Exception as e:
            print("An exception occurred: ", e)

@app.post("/generate")
def generate(item_msg: Item_msg):
    while True:
        try:
            global csv_agent
            msg = csv_agent.run(item_msg.msg)
            print("USER: " + item_msg.msg)
            print("AI: " + msg)
            return {"message": msg}
                
        except Exception as e:
            print("An exception occurred: ", e)