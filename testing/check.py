import requests
import base64

text1 = "MEOW"
text2 = "2000 $"
flag = "hti"

r = None
with open ("./image.jpg", "rb") as file:
    r = requests.post("http://127.0.0.1:5000/create_image",data={"title" : text1, "subtitle" : text2, "flag" : flag}, files={"image" : file}).json()

if not r["exception"]:
    imgdata = base64.b64decode(r["result"])
    with open('./result.jpg', 'wb') as f:
        f.write(imgdata)

# from io import BytesIO
# bio = BytesIO()
# bio.name = 'image.jpeg'
# image.save(bio, 'JPEG')
# bio.seek(0)
# bot.send_photo(chat_id, photo=bio)
# 