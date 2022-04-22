from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from time import asctime, localtime
from os.path import exists
from os import getcwd, system
import pickle
from time import sleep

#les fonction pour sauvegarder les jeux pour en faire une liste plus tard
#egalement pour voir si le jeux a changer depuis la derniere fois
def recup_data(nom_fichier_score):
    """fonction recuperant les score du fichier 'score' ou si il n' existe pas cree la variable score={}"""
    if exists(nom_fichier_score):
        fichier_score = open(nom_fichier_score,'rb')
        mon_unpickler = pickle.Unpickler(fichier_score)
        data = mon_unpickler.load()
        fichier_score.close()

    else:
        data = {}
    return data

def enregistrer_data(dicti, nom_fichier_score):
    """cette fonction enregistre le dictionnaire des score dans un fichier"""
    with open(nom_fichier_score,'wb') as fichier:
        mon_unpickler=pickle.Pickler(fichier)
        mon_unpickler.dump(dicti)

def is_internet_connected(trys = 0):

    system("cls")
    if trys>= 500:
        raise ValueError ("Not internet connecton found")

    url = "http://www.google.com"
    timeout = 1
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        return True

    except (requests.ConnectionError, requests.Timeout) as exception:
        print(f"No internet connection. {trys + 1}")
        sleep(5)
        is_internet_connected(trys + 1)

def updated_chromium(options):

    # selenium 4
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.utils import ChromeType

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options = options)

    return driver

def change_wallpaper(img_path, folder_path = None, second_img = None):
    from PIL import Image
    import ctypes

    if not folder_path:
        folder_path = getcwd()

    #creating a white image that the size of 2 monitors
    new_img = Image.new('RGB', (3840, 1080), color = (0, 0, 0))

    img_1 = Image.open(img_path)

    images = [img_1]
    if second_img:
        images.append(Image.open(second_img))

    #resizing the images
    maxwidth, maxheight = (1920, 1080)
    for i, img in enumerate(images):
        width, height = img.size

        resize_ratio = min(maxwidth/width, maxheight/height)
        img = img.resize((int(resize_ratio * img.size[0]), int(resize_ratio * img.size[1])))

        

    
        #pasting the base image twice
        new_img.paste(img, (1920 * i + (1920 - img.size[0])//2, 0))

    save_path = folder_path + "/" + f"temp{i + 1}.jpg"
    new_img.save(save_path)

    #setting the walppaper
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, save_path, 0)


#global variables
path = "data"
img_path = getcwd()+"\\"+"img_0.jpg"
data = recup_data(path)

#options chrome pour qu'il souvre en arriere plan
options = webdriver.ChromeOptions()
options.add_argument('headless')

# si il n'y a pas internet on attends
is_internet_connected()

#setup et recuperation du html du browser
driver = updated_chromium(options)


driver.get("https://www.epicgames.com/store/fr/free-games")
# sleep(10)
content = driver.page_source


#on ferme toutes les instances de selenium (webdriver)
#sinon le programme ne se termine pas
driver.close()


#setup de la soup (arrangement du code html)
soup = BeautifulSoup(content, features="html.parser")

name = []

#apres des fouilles du code html on cherche ces ligne en particulier
liste_parsing = soup.findAll(class_ = "css-nq799m")
for a in liste_parsing:
    name.append(a.find('a', role = "link"))

free_game = []

#parmis toutes les lignes qui sont trouver par le bloc precedent
#on cherche celle qui parle du jeu gratuit
for n in name:
    print(n.text)
    if n:
        if n.text[:7] == "Gratuit":

            free_game.append((n.text.split("Gratuit")[1]))

system("cls")
print(f'le jeu gratuit du moment est "{free_game}"')

#si le jeu n'est pas deja connu
for game in free_game:
    if not game in data:
        #on recupere le nouveau jeu et la date auquel il a ete detecte la premiere fois
        data[game] = asctime(localtime())
        enregistrer_data(data, path)

        #on met l'image du jeu en fond d'ecran
        from download_img_game import get_img_url, download_img

        if game:
            print("new game !!")
            
            download_img(get_img_url(soup))
            sleep(1)
            cwd = getcwd()
            second_img = None

            if len(free_game) > 1:
                second_img = cwd +"\\"+"img_1.jpg"
                change_wallpaper(folder_path = cwd, img_path = cwd +"\\"+"img_0.jpg", second_img = second_img)

#on check que toutes les instances sont fermees
driver.quit()