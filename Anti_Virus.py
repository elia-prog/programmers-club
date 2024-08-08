from pathlib import Path
import requests
import json
import time

def check_anti_virus(folder):
    if not folder.exists():
        return "Directory does not exist"
    files = [f for f in folder.iterdir() if f.is_file()]

    results = {}
    for file in files:
        if file.is_dir():
            check_anti_virus(file)            
        else:   
            results[file.name] = is_file_safe(file)
            time.sleep(20)  # השהייה של 20 שניות בין כל בדיקת קובץ

    return results

def is_file_safe(file_path):
    api_key = "57562bd1d53b2ebd14a3715fce8c7900a463ee1686d39e38cec2a7242f041913"
    url = "https://www.virustotal.com/api/v3/files"
    
    headers = {
        'x-apikey': api_key
    }
    
    with open(file_path, 'rb') as file:
        files = {
            'file': (file_path.name, file)
        }
        
        response = requests.post(url, headers=headers, files=files)
    
    if response.status_code != 200:
        print(f"Error uploading file {file_path.name}: {response.status_code} - {response.text}")
        return "Error in uploading the file"
    
    result = response.json()
    file_id = result['data']['id']
    
    # בדיקת התוצאות של הדוח
    while True:
        report_url = f"https://www.virustotal.com/api/v3/analyses/{file_id}"
        response = requests.get(report_url, headers={'x-apikey': api_key})
        
        if response.status_code != 200:
            print(f"Error getting report for file {file_path.name}: {response.status_code} - {response.text}")
            return "Error in getting the report"
        
        report = response.json()
        
        # בדיקה אם הדוח מוכן
        if report['data']['attributes']['status'] == 'completed':
            break
    
    # ניתוח התוצאות
    stats = report['data']['attributes']['stats']
    
    if stats['malicious'] > 0:
        return "No"
    return "Yes"

# folder1 = input("Enter your folder: ")
path = 'C:/Users/User/OneDrive/שולחן העבודה/python'
results = check_anti_virus(Path(path))
print(results)