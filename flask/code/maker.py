#TODO Адаптивный шрифт!
from PIL import ImageDraw, ImageFont, Image, ImageOps

class ImageGenerator:

    TTF_SOURCE = "./code/content/times.ttf"
    LOGO_SOURCE = "./code/content/logo.jpg"

    def __init__(self, input_img, first_text, second_text, country):

        #Результат преобоазования 
        self.result = None

        self.input_img = input_img
        self.first_text = first_text
        self.second_text = second_text
        self.country = country
        self.processing()

    def crop_img(self, img):
        """Обрезка изображения по квадрату"""
        crop_width, crop_height = img.size
        value = crop_width if crop_width < crop_height else crop_height
        area = (0, 0, value, value)
        img = img.crop(area)
        return img

    def resizer(self, img, basewidth):
        """Ресайз фото"""
        width, height = img.size
        wpercent = basewidth / float(width)
        hsize = int((float(height) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        return img

    def processing(self):
        
        # Открываем основное изображение
        photo = Image.open(self.input_img)
        width, height = photo.size
        # Открываем флаг
        national_flag = Image.open("./code/content/flags/" + self.country.lower() + ".png")
        # Открываем лого
        company_logo = Image.open(self.LOGO_SOURCE)

        # Предобработка основого фото
        if width != height:
            photo = self.crop_img(photo)
            width, height = photo.size
        # Если больше - уменьшаем
        if width > 1080:
            photo = self.resizer(photo, 1080)
        # Если меньше - увеличиваем
        else:
            photo = photo.resize((1080, 1080), resample=Image.BOX)
        width, height = photo.size

        # Предобработка флага
        national_flag = self.resizer(national_flag, 190)
        national_flag = ImageOps.expand(national_flag, border=3, fill="black")
        width_nationalflag, height_nationalflag = national_flag.size

        # Создаем пустое изображение
        background = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(background)
        # Вставляем основное фото
        background.paste(photo)

        # Добавляем прямоугольник вниз
        photo_height = 898
        draw.rectangle(((0, photo_height), (1080, 1080)), fill="white")
        rectangle_height = 1080 - photo_height

        # Добавляем основной текст
        fontsize = 50
        font = ImageFont.truetype(self.TTF_SOURCE, fontsize)
        w, h = draw.textsize(self.first_text, font)
        left = (width - w) / 2
        draw.text(
            (left, 925), self.first_text, font=font, fill=(6, 26, 113), align="center"
        )

        # Добавляем текст с ценой
        fontsize = 45
        font = ImageFont.truetype(self.TTF_SOURCE, fontsize)
        w, h = draw.textsize(self.second_text, font)
        left = (width - w) / 2
        draw.text(
            (left, 1000), self.second_text, font=font, fill=(6, 26, 113), align="center"
        )

        # Вычисляем место флага и добавляем его
        flag_insertposition = (
            photo_height + (rectangle_height - height_nationalflag) / 2
        )
        background.paste(national_flag, (25, int(flag_insertposition)))

        # Добавляем лого
        background.paste(company_logo, (850, 925))

        # Сохраняем изображение
        self.result = background
