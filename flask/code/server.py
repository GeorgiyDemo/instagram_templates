from maker import ImageGenerator
import json
from flask import Flask, request
import base64
from io import BytesIO


app = Flask(__name__)


@app.route("/create_image", methods=["POST"])
def create_place():
    """Создание нового изображения"""


    title_text = request.form.get('title')
    subtitle_text = request.form.get('subtitle')
    nationalflag_code = request.form.get('flag')

    image = request.files['image']
    img_obj = ImageGenerator(image,title_text,subtitle_text,nationalflag_code)
    if img_obj.result != None:

        buffered = BytesIO()
        img_obj.result.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return {"exception" : False, "result" : img_str.decode("utf-8")}
    return {"exception" : True}
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)