import time
import os
path='/home/suifeng/图片/mm/'
while True :
    l=len(os.listdir(path))
    print(l)
    time.sleep(5)
