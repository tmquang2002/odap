import subprocess
import time
import os

while True:
    if os.path.exists("processed_data.csv"):
        subprocess.run('hadoop fs -copyFromLocal -f processed_data.csv /processed_data.csv',shell=True)
        print("New update!")
        time.sleep(10)
    
