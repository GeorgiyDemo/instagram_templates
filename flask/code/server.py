from maker import ImageGenerator
import json
from flask import Flask, request


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
        return {"exception" : False, "result" : img_obj.result}
    return {"exception" : True}
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)