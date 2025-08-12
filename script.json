import requests
from bs4 import BeautifulSoup

dominios = [
    "https://www.propiedades.com/ciudad",
    "https://www.inmueblesya.com/listado"
]


def buscar_propiedades(url):
    propiedades = []
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # 🔹 Esta parte se adapta a cada sitio
        anuncios = soup.select(".anuncio")  # Cambiar según estructura HTML
        for anuncio in anuncios:
            ciudad = anuncio.select_one(".ciudad").get_text(strip=True) if anuncio.select_one(".ciudad") else ""
            direccion = anuncio.select_one(".direccion").get_text(strip=True) if anuncio.select_one(".direccion") else ""
            estado = anuncio.select_one(".estado").get_text(strip=True) if anuncio.select_one(".estado") else ""
            precio = anuncio.select_one(".precio").get_text(strip=True) if anuncio.select_one(".precio") else ""
            fuente = url

            propiedades.append({
                "ciudad": ciudad,
                "direccion": direccion,
                "estado": estado,
                "precio": precio,
                "fuente": fuente
            })
    except Exception as e:
        print(f"⚠️ Error con {url}: {e}")
    return propiedades
