"""
this script will create an HTML page listing image files in chronological order
Then print HTML page to PDF, e.g. capture slides from a talk
"""
import os
from datetime import datetime

# Folder path 
folder = "yann_LeCun" # 'slides'

# List all files in the folder
files = os.listdir(folder) 

# Filter for only image files
images = [f for f in files if f.lower().endswith('.jpg') or f.lower().endswith('.png')] 
# print(images)
# Sort by creation date
images.sort(key=lambda x: os.path.getctime(os.path.join(folder, x)))
# img_data = []
# for x in images:
#     ts = os.path.getctime(os.path.join(folder, x))
#     creation_time = datetime.fromtimestamp(ts)
#     formatted_time = creation_time.strftime("%Y-%m-%d_%H-%M-%S")    
#     img_data.append([x, formatted_time])
# print(img_data)

# Create HTML content 
li_tags = '\n'.join([f'<li><img src="{folder}/{img}" width=800 height=600 /></li>' for img in images])

html = f'''
<html><body><h1>{folder}</h1>
<ul>{li_tags}  </ul>
</body></html>'''

with open(f'{folder}.html','w') as f:
    f.write(html)