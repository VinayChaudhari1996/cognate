from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import pandas as pd
from tqdm import tqdm
import datetime


from typing import Optional
from pyngrok import ngrok
import nest_asyncio
import uvicorn
import json

# 1st import the package and check its version
import MTM
print("MTM version: ", MTM.__version__)

from MTM import matchTemplates, drawBoxesOnRGB

import cv2
from skimage.data import coins

import numpy as np
from skimage import io

from PIL import Image
from tqdm import tqdm
import glob
import os 



print("[status] : packages load successfully !")

#Functions 

try:
  os.mkdir("/app/datasets/")
except:
  print("/app/dataset/ : Is alredy exists.")



def getImgPaths(path,ext="jpg"):
  path = f"{path}*.{ext}"
  print("path is :",path)
  img_list = glob.glob(path)
  return img_list



def makeImgArray(img):
  image = io.imread(img)
  return image


# Classes 
"""
Download images using given url or path
  MainFolder :
  -- Folder 1
  -- Folder 2
  NOTE : Images name should be str only or number 
"""


class downloadImagesZip(BaseModel):
    zipFileUrl:str


# CRUD : For Modeling 

class createModel(BaseModel):
    banners_folder_path:str
    model_file_name_path: str

class readModel(BaseModel):
    model_file_name_path: str

class updateModel(BaseModel):
    model_path:str
    banner_img_path:str

class deleteModel(BaseModel):
    model_path:str


# VERIFY
class verifyResults(BaseModel):
    project_name:str
    model_path:str
    print_screen_folder_path:str




app = FastAPI(title="Banners verification AI",debug=True)


@app.get("/")
async def root():
    return {"message": "Hello World packages loaded successfully"}

@app.post("/downloadImages")
async def downloadImages(payload:downloadImagesZip):
    payload_ = payload.dict()

    ct = datetime.datetime.now()

    zipFileUrl = payload_["zipFileUrl"]
    
  
    response = requests.get(zipFileUrl, stream=True)

    with open(f"/app/datasets/data_{ct}.csv", "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

    return {"status":f"{zipFileUrl} : dowloaded at /app/dataset/"}



@app.post("/create_model/")
async def createModelFunction(payload:createModel):
  payload_ = payload.dict()

  model_file_name = payload_['model_file_name_path']
  banners_path = payload_['banners_folder_path']
 

  try:

    # For Banners
    banners_img_list = getImgPaths(banners_path,"jpg")

    all_banner_embeddings = []

    for img in banners_img_list:

      result = (img,makeImgArray(img))

      all_banner_embeddings.append(result)


    np.save(model_file_name,all_banner_embeddings)
    result = {"model_status":"success",
              "model_path":model_file_name}
  except:
    cause = """
    [Dataset has some issues]
    make sure all image are jpg format,
    dataset path should be valid and contain images,
    dataset should have atleast 5 images
    """
    result = {"model_status":cause}

  return result


@app.post("/read_model/")
async def readModelFunction(payload:readModel):
    payload_ = payload.dict()

    model_file_name = payload_['model_file_name_path']

    if os.path.isfile(model_file_name):


      listTemplate = np.load(model_file_name,allow_pickle=True)

      listTemplate_list = listTemplate.tolist()

      listTemplate = json.dumps(listTemplate_list)

      res = {"model_read_status":"success",
              "model_path":listTemplate}

    else:
      res = {"model_upate_status":"fail"}
    
    return res

  
@app.post("/update_model/")
async def updateModelFunction(payload:updateModel):
    payload_ = payload.dict()

    model_file_name = payload_['model_path']
    banner_img_path = payload_['banner_img_path']

    if os.path.isfile(model_file_name):


      listTemplate = np.load(model_file_name,allow_pickle=True)

      listTemplate = listTemplate.tolist()

      result = (banner_img_path,makeImgArray(banner_img_path))

      np.save(model_file_name,result)

      res = {"model_upate_status":"success",
              "model_path":model_file_name,
              "img_name_added":banner_img_path}
    else:
      res = {"model_upate_status":"fail",
              "model_path":model_file_name,
              "img_name_added":banner_img_path}
    
    return res


@app.post("/delete_model/")
async def deleteModelFunction(payload:updateModel):
    payload_ = payload.dict()

    model_file_name = payload_['model_path']

    try:
      os.remove(model_file_name)

      res = {"model_delete_status":"success", "model_path":model_file_name}
    
    except:
      res = {"model_delete_status":"failed", "model_path":model_file_name ,"remark":"model path is wrong or model not exisiting in dirs"}


    
    return res



@app.post("/verify_results/")
async def verifyModelFunction(payload:verifyResults):

    payload_ = payload.dict()

    project_name = payload_['project_name']
    model_path = payload_['model_path']
    print_screen_folder_path = payload_['print_screen_folder_path']

    # data.csv contains all process report and responses in json format.
    
    try:

      DATA = "data.csv"
      check_project_status = pd.read_csv(DATA)


      project = check_project_status.loc[check_project_status["project_name"]==project_name]


      project_response =  project.to_json(orient="records")
      
      if len(project)==0:

        CMD = f"""
        python verify_model.py --model {model_path} --folder {print_screen_folder_path}  --project_name {project_name} &
        """

        os.system(CMD) 
        
        return {"status":f"No such project was created , so creating new project as : {project_name}"}


      else:
        return {"status":"Existing project found !","response":project_response}

    except:

      return {"status":f"Something is wrong"}



# if __name__ == 'main':
#     uvicorn.run(app,host="127.0.0.1",port=8000)