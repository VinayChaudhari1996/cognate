import MTM
print("MTM version: ", MTM.__version__)
import sys 

from MTM import matchTemplates, drawBoxesOnRGB

import cv2
from skimage.data import coins
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io

from PIL import Image
from tqdm import tqdm
import glob
import os 
import argparse

import json 
import time
import pandas as pd

import csv
import os.path
from csv import DictWriter

# using datetime module
import datetime;

# ct stores current time
ct = datetime.datetime.now()
print("current time:-", ct)
print("-"*50)



def makeImgArray(img):
  image = io.imread(img)
  return image

start_time = time.time()


def bannerNPY(npy_path,websiteImgFolderPath):
    
  listTemplate = np.load(npy_path,allow_pickle=True)
  listTemplate = tuple(map(tuple, listTemplate))

  websiteImgFolderPath = f"{websiteImgFolderPath}*.jpg"
  websitesImgList = glob.glob(websiteImgFolderPath)

  print(websitesImgList)


  allHits = []
  for website in tqdm(websitesImgList):

    print("-"*70)

    print(f"✔️ {website} : processing...")
    websiteEmbedding = makeImgArray(website)

    try:

      # Then call the function matchTemplates (here a single template)
      Hits = matchTemplates(listTemplate,websiteEmbedding , 
                            N_object=13,score_threshold=0.8, 
                            method=cv2.TM_CCOEFF_NORMED, maxOverlap=0.1)
      
      Hits = Hits.to_json(orient="records")

      result = {"print_screen":website,"banners_found":Hits}

      allHits.append(result)

    except:

      print(f"❌ {website} : have some issues...")

  return json.dumps(allHits)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    This script is going to verify banners in printscreen
    """)
    parser.add_argument("--model", help="path of model eg: /app/data.npy")
    parser.add_argument("--folder", help="path of folder where you want to find folder1 images")
    parser.add_argument("--project_name", help="campaign name unique id")

    args = parser.parse_args()
    
    #print(args)

    MODEL_PATH = args.model
    FOLDER_PATH = args.folder
    PROJECT_NAME = args.project_name


    result = bannerNPY("/app/data.npy","/app/banner_print/folder 2/")
    end_time = time.time() - start_time
    
    response = json.loads(result)


    result_report = {"project_name":PROJECT_NAME,
                    "print_screen_folder_path":FOLDER_PATH,
                    "model_path":MODEL_PATH,
                    "processing_time_in_sec":end_time,
                    "timestamp":ct,
                    "response":response}



    file_name = 'data.csv'

    with open(file_name, 'a') as f:

      df = pd.DataFrame(result_report)
      df.to_csv(f, mode='a', header=f.tell()==0,index=False)


    """
    CMD : 
    python verify_model.py --model "data.npy" --folder "folder 2" --project_name "sample"

    """
    print("response_logs saved successfully")

sys.exit() 




