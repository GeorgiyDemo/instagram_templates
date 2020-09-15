from maker import ImageGenerator
import os

if __name__ == "__main__":

    flags_list = os.listdir("flags")
    for fichier in flags_list[:]:
        if not (fichier.endswith(".png")):
            flags_list.remove(fichier)
    flags_list = [v.split(".")[0] for v in flags_list]
    for i in range(len(flags_list)):
        ImageGenerator(
            "./image.jpg",
            "./result" + str(i) + ".jpg",
            "ОТЕЛЬ НА БАЛИ",
            "USD 2.500.000",
            flags_list[i],
        )
