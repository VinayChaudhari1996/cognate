from random import sample
import glob
import os

"""
dataset : !gdown https://drive.google.com/uc?id=1nCWTwIix0QhgE6f8kpr5bu9o3VjT5Ofb

"""


no = 30
p = "/app/banner_print/folder 2/"
files = os.listdir('/app/banner_print/folder 2/')

# for count,file in enumerate(files[:]):
#     os.rename(p+file,f"{p}{count}.jpg")
#     print("file:",file,f"{p}{count}.jpg")

# print("[Renname] : Done")

for file in files[:no]:
    print("file:",p+file)

    os.remove(p+file)

print(f"{no} : files deleted")