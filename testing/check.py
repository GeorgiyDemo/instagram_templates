import requests
import base64

text1 = "MEOW"
text2 = "2000 $"
flag = "hti"

with open ("./image.jpg", "rb") as file:
    r = requests.post("http://127.0.0.1:5000/create_image",data={"title" : text1, "subtitle" : text2, "flag" : flag}, files={"image" : file}).json()

if not r["exception"]:
    img_data = base64.b64decode(r["result"])
    with open('./result.jpg', 'wb') as f:
        f.write(img_data)