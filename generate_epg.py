import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

channels = [
    {"id": "ATV", "url": "https://www.gatotv.com/canal/atv"},
    {"id": "Latina HD", "url": "https://www.gatotv.com/canal/frecuencia_latina"},
    {"id": "WILLAX", "url": "https://www.gatotv.com/canal/willax_tv"},
]

def format_time(dt):
    return dt.strftime("%Y%m%d%H%M%S -0500")

def get_schedule(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        programas = []

        # 🔥 SELECTOR MÁS FLEXIBLE
        bloques = soup.find_all("div", class_="item")

        print(f"DEBUG: encontrados {len(bloques)} bloques en {url}")

        for b in bloques:
            try:
                hora_tag = b.find("div", class_="time")
                titulo_tag = b.find("div", class_="title")

                if not hora_tag or not titulo_tag:
                    continue

                hora = hora_tag.text.strip()
                titulo = titulo_tag.text.strip()

                # validar formato HH:MM
                if ":" not in hora:
                    continue

                programas.append((hora, titulo))

            except Exception as e:
                print("Error parseando bloque:", e)
                continue

        return programas

    except Exception as e:
        print("Error scraping:", e)
        return []

def generate_epg():
    now = datetime.now()

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'

    for ch in channels:
        xml += f'  <channel id="{ch["id"]}">\n'
        xml += f'    <display-name>{ch["id"]}</display-name>\n'
        xml += f'  </channel>\n'

        programas = get_schedule(ch["url"])

        if not programas:
            # fallback
            for i in range(10):
                start = now + timedelta(hours=i)
                stop = start + timedelta(hours=1)

                xml += f'''
  <programme start="{format_time(start)}" stop="{format_time(stop)}" channel="{ch["id"]}">
    <title>{ch["id"]} Programa {i+1}</title>
    <desc>Programación automática</desc>
  </programme>
'''
        else:
            for i, (hora, titulo) in enumerate(programas):
                try:
                    h, m = map(int, hora.split(":"))
                    start = now.replace(hour=h, minute=m, second=0)
                    stop = start + timedelta(hours=1)

                    xml += f'''
  <programme start="{format_time(start)}" stop="{format_time(stop)}" channel="{ch["id"]}">
    <title>{titulo}</title>
    <desc>Programación real</desc>
  </programme>
'''
                except:
                    continue

    xml += "</tv>"

    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(xml)


generate_epg()
