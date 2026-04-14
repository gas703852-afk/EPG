import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

HEADERS = {"User-Agent": "Mozilla/5.0"}

CANALES = [
    {"id": "ATV", "url": "https://www.gatotv.com/canal/atv"},
    # canal ATV +
    # canal ATV Sur
    # canal RPP
    # canal Canal N
    {"id": "Panamericana", "url": "https://mi.tv/pe/canales/panamericana-tv"},
    # canal PBO
    {"id": "WILLAX", "url": "https://www.gatotv.com/canal/willax_tv"},
    # canal Exitosa
    # canal PLUS TV LIFE
    {"id": "Tv Peru", "url": "https://mi.tv/pe/canales/tv-peru"},
    {"id": "LATINA", "url": "https://www.gatotv.com/canal/frecuencia_latina"},
    # canal Latina Noticias
    {"id": "LATINA", "url": "https://www.gatotv.com/canal/frecuencia_latina"},
    # canal Global
    {"id": "LATINA", "url": "https://www.gatotv.com/canal/america_television_peru"},
    # canal Liga 1 Max
    # canal Liga 1
    # canal DirecTV
    # canal Movistar Deportes
    {"id": "ESPN HD", "url": "https://www.gatotv.com/canal/espn_internacional"},
    {"id": "ESPN 2 HD", "url": "https://www.gatotv.com/canal/espn_internacional"},
    {"id": "ESPN 3 HD", "url": "https://www.gatotv.com/canal/espn_internacional"},
    {"id": "ESPN 4 HD", "url": "https://www.gatotv.com/canal/espn_internacional"},
    {"id": "ESPN 5 HD", "url": "https://www.gatotv.com/canal/espn_internacional"},
    {"id": "ESPN 6 HD", "url": "https://www.gatotv.com/canal/espn_internacional"},
    {"id": "ESPN 7 HD", "url": "https://www.gatotv.com/canal/espn_internacional"},
    {"id": "ESPN Premium HD", "url": "https://www.gatotv.com/canal/espn_internacional"},
]

def obtener_programacion(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        programas = []
        items = soup.select(".item")  # puede variar

        for item in items:
            hora = item.select_one(".time")
            titulo = item.select_one(".title")

            if hora and titulo:
                programas.append({
                    "hora": hora.text.strip(),
                    "titulo": titulo.text.strip()
                })

        return programas

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []


def generar_programas_xml(canal_id, programas_scraping):
    now = datetime.now()
    xml = ""

    # 🔴 SI FALLA SCRAPING → fallback automático
    if not programas_scraping:
        for i in range(12):
            start = now + timedelta(hours=i)
            stop = start + timedelta(hours=1)

            xml += f'''
  <programme start="{start.strftime("%Y%m%d%H%M%S")} -0500" stop="{stop.strftime("%Y%m%d%H%M%S")} -0500" channel="{canal_id}">
    <title>{canal_id} Programa {i+1}</title>
    <desc>Programación automática</desc>
  </programme>
'''
        return xml

    # 🟢 SI HAY DATOS REALES
    for prog in programas_scraping[:12]:
        try:
            h, m = map(int, prog["hora"].split(":"))
            start = now.replace(hour=h, minute=m, second=0)
            stop = start + timedelta(hours=1)

            xml += f'''
  <programme start="{start.strftime("%Y%m%d%H%M%S")} -0500" stop="{stop.strftime("%Y%m%d%H%M%S")} -0500" channel="{canal_id}">
    <title>{prog["titulo"]}</title>
    <desc>Programación real</desc>
  </programme>
'''
        except:
            continue

    return xml


def generar_epg():
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<tv>
'''

    for canal in CANALES:
        canal_id = canal["id"]

        xml += f'''
  <channel id="{canal_id}">
    <display-name>{canal_id}</display-name>
  </channel>
'''

        programas_scraping = obtener_programacion(canal["url"])
        xml += generar_programas_xml(canal_id, programas_scraping)

    xml += "\n</tv>"

    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(xml)

    print("EPG generado correctamente")


if __name__ == "__main__":
    generar_epg()
