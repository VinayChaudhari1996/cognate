import glob
import os

f1 = glob.glob("/app/banner_print/folder 1/*.jpg")
f2 = glob.glob("/app/banner_print/folder 2/*.jpg")


f1 = f1[:3]
print(f1)
f2 = f2[:3]
print(f2)

for f_1 in f1:
    os.unlink(f_1)

print("f1 done")

for f_2 in f2:
    os.unlink(f_2)

print("f2 done")



