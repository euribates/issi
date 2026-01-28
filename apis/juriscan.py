from urllib.request import urlopen
from bs4 import BeautifulSoup
HOST = 'www3.gobiernodecanarias.org'

URL_BASE = f'https://{HOST}/juriscan/ficha.jsp?id={{id_juriscan}}'

def get_juriscan(id_juriscan):
    url = URL_BASE.format(id_juriscan=id_juriscan)
    print(url)
    with urlopen(url) as response:
        print(response.url)
        print(response.headers)
        print(response.status)
        soup = BeautifulSoup(response.read())
        name = soup.find(id="titleFicha")
        print(name)
        print(f'  ---"{name.text}"---  ')


def main():
    get_juriscan(62312)


if __name__ == "__main__":
    main()

