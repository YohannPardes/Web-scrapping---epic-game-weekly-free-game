from requests import get


def download_img(image_urls):

    for i, url in enumerate(image_urls):
        img_data = get(url).content
        with open('img_{}.jpg'.format(i), 'wb') as handler:
            handler.write(img_data)

def get_img_url(soup):

    matches = []

    liste_parsing = soup.findAll(class_ = "css-1lozana")
    for a in liste_parsing:
        matches.append(a.find('img', class_ = "css-13vabc5"))


    print(matches)

    
    right_match = [match for match in matches if match][:2] #visiblement c'est cette image la bonne

    urls = []
    for match in right_match:

        url = match["data-image"]

        url = url.split(".jpg")[0]+".jpg"

        urls.append(url)

    return urls

if __name__ == "__main__":

    pass