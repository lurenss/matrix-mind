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
from langchain.agents.agent_types import AgentType

#initialization
app = FastAPI()
credentials = False
path_df = None
csv_agent = None
llm = None 


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

class Item_msg(BaseModel):
    msg: str

@app.post("/api-key")
def process_api_key(item: Item_api):
    """
    Processes the API key and model with LangChain.

    Args:
        item (Item_api): The API key and model to process.

    Returns:
        dict: A message indicating that the API key and model have been processed.
    """
    # try to process the api key and model with langchain
    try:
        os.environ["OPENAI_API_KEY"] = item.apiKey
        #global csv_agent
        global llm 
        #csv_agent = create_csv_agent(ChatOpenAI(temperature=0, model_name = "gpt-4"), path_df, verbose= True)
        llm = ChatOpenAI(temperature=0, model_name = "gpt-4-0613")
        global credentials
        credentials = True

        return {"message": "API Key and model processed"}
    
    except ValueError as e:
        print("An error occurred: ", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("An error occurred: ", e)
        raise HTTPException(status_code=500, detail="Internal server error.")
    
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a CSV file and saves it to the server.

    Args:
        file (UploadFile, optional): The CSV file to upload. Defaults to File(...).

    Returns:
        dict: A message indicating that the file has been uploaded.
    """
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
    """
    Generates a response to a user message based on the uploaded CSV file.

    Returns:
        dict: A message containing the AI-generated response.
    """
    try:
        global path_df
        global csv_agent
        global llm
        if path_df is None:
            raise ValueError("CSV file not uploaded. Please upload a CSV file first.")
        user_msg = "What are the columns of this dataset? Answer with a sentence please."
        csv_agent = create_csv_agent(llm, path_df, verbose= True, agent_type= AgentType.OPENAI_FUNCTIONS)
        msg = csv_agent.run(user_msg)
        print("USER: " + user_msg)
        print("AI: " + msg)
        return {"message": msg}
    
    except ValueError as e:
        print("An error occurred: ", e)
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    except Exception as e:
        print("An error occurred: ", e)
        return JSONResponse(status_code=500, content={"message": "Internal server error."})
    
@app.post("/generate")
def generate(item_msg: Item_msg):
    """
    Generates a response to a user message based on the uploaded CSV file.

    Args:
        item_msg (Item_msg): The user message to generate a response to.

    Returns:
        dict: A message containing the AI-generated response.
    """
    try:
        global csv_agent
        if csv_agent is None:
            raise ValueError("CSV agent not initialized. Please run /first_generate first.")
        msg = csv_agent.run(item_msg.msg)
        print("USER: " + item_msg.msg)
        print("AI: " + msg)
        return {"message": msg}
    
    except ValueError as e:
        print("An error occurred: ", e)
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    except Exception as e:
        print("An error occurred: ", e)
        return JSONResponse(status_code=500, content={"message": "Internal server error."})
