#Необходимо выдавать изображение 1080*1080

from PIL import ImageDraw, ImageFont, Image

def crop_img(img):
    """Обрезка изображения по квадрату"""
    crop_width, crop_height = img.size
    value = crop_width if crop_width < crop_height else crop_height
    area = (0, 0, value, value)
    img = img.crop(area)
    return img

basewidth = 1080
photo = Image.open('./image.jpg')
width, height = photo.size

#Предобработка фото
if width != height:
    photo = crop_img(photo)
    width, height = photo.size

if width > basewidth:
    wpercent = basewidth / float(width)
    hsize = int((float(height) * float(wpercent)))
    photo = photo.resize((basewidth, hsize), Image.ANTIALIAS)

width, height = photo.size
print(width, height)


background = Image.new('RGB', (width, height), (255,255,255))
draw = ImageDraw.Draw(background)

fontsize = 100  # starting font size
font = ImageFont.truetype("./arial.ttf", fontsize)
background.paste(photo)
draw.rectangle(((0, 898), (1080, 1080)), fill="white")
draw.text((450, 950), "ОТЕЛЬ НА БАЛИ", font=font, fill=(0,0,0)) # put the text on the image
background.save('./result.png')


