

import subprocess
import time
import pyautogui

app_path = "C:/Program Files (x86)/Microsoft Power BI Desktop/bin/PBIDesktop.exe"
file_path = "D:/HK7/ODAP/ODAP.pbix"
process = subprocess.Popen([app_path, file_path])
time.sleep(45)
pyautogui.press("alt")
pyautogui.press("q")
pyautogui.typewrite("Refresh")
time.sleep(1)
pyautogui.press("enter")
time.sleep(1)
pyautogui.press("enter")
time.sleep(20)
pyautogui.hotkey('ctrl', 's')
time.sleep(10)

try:
    process.terminate()
    process.wait(timeout=5)  # Wait for termination (optional)
except subprocess.TimeoutExpired:
    print("Process did not terminate gracefully. Killing it.")
    process.kill()