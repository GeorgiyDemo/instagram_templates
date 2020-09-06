from PIL import ImageDraw, ImageFont, Image, ImageOps

#############################
LOGO_SOURCE = "./logo.jpg"
INPUT_IMG = "./image.jpg"
OUTPUT_IMG = "./result.jpg"
TTF_SOURCE = "./times.ttf"
IMG_TEXT_FIRST = "ОТЕЛЬ НА БАЛИ"
IMG_TEXT_SECOND = "USD 2.500.000"
COUNTRY_FLAG = "ECU"
#############################


def crop_img(img):
    """Обрезка изображения по квадрату"""
    crop_width, crop_height = img.size
    value = crop_width if crop_width < crop_height else crop_height
    area = (0, 0, value, value)
    img = img.crop(area)
    return img


def resizer(img, basewidth):
    """Ресайз фото фото"""
    width, height = img.size
    wpercent = basewidth / float(width)
    hsize = int((float(height) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    return img


# Открываем основное изображение
photo = Image.open(INPUT_IMG)
width, height = photo.size
# Открываем флаг
national_flag = Image.open("./flags/" + COUNTRY_FLAG.lower() + ".png")
# Открываем лого
company_logo = Image.open(LOGO_SOURCE)


# Предобработка основого фото
if width != height:
    photo = crop_img(photo)
    width, height = photo.size
# Если больше - уменьшаем
if width > 1080:
    photo = resizer(photo, 1080)
# Если меньше - увеличиваем
else:
    photo = photo.resize((1080, 1080), resample=Image.BOX)
width, height = photo.size

# Предобработка флага
national_flag = resizer(national_flag, 190)
national_flag = ImageOps.expand(national_flag, border=3, fill="black")

# Создаем пустое изображение
background = Image.new("RGB", (width, height), (255, 255, 255))
draw = ImageDraw.Draw(background)
# Вставляем основное фото
background.paste(photo)

# Добавляем прямоугольник вниз
draw.rectangle(((0, 898), (1080, 1080)), fill="white")

# Добавляем основной текст
fontsize = 50
font = ImageFont.truetype(TTF_SOURCE, fontsize)
w, h = draw.textsize(IMG_TEXT_FIRST, font)
left = (width - w) / 2
draw.text((left, 925), IMG_TEXT_FIRST, font=font, fill=(6, 26, 113), align="center")

# Добавляем текст с ценой
fontsize = 45
font = ImageFont.truetype(TTF_SOURCE, fontsize)
w, h = draw.textsize(IMG_TEXT_SECOND, font)
left = (width - w) / 2
draw.text((left, 1000), IMG_TEXT_SECOND, font=font, fill=(6, 26, 113), align="center")

# Добавляем флаг
background.paste(national_flag, (25, 925))

# Добавляем лого
background.paste(company_logo, (850, 925))

# Сохраняем изображение
background.save(OUTPUT_IMG)
