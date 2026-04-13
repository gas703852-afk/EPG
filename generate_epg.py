from datetime import datetime, timedelta

def generar_epg():
    now = datetime.utcnow()

    # Ajuste Perú (-5)
    now = now - timedelta(hours=5)

    programas = [
        ("Noticias ATV", 8, 9),
        ("Película del Día", 9, 11),
        ("Serie Nacional", 11, 13),
    ]

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<tv>\n'

    canal_id = "atv.pe"

    xml += f'  <channel id="{canal_id}">\n'
    xml += f'    <display-name>ATV</display-name>\n'
    xml += f'  </channel>\n'

    for titulo, start_h, end_h in programas:
        start = now.replace(hour=start_h, minute=0, second=0)
        end = now.replace(hour=end_h, minute=0, second=0)

        start_str = start.strftime("%Y%m%d%H%M%S -0500")
        end_str = end.strftime("%Y%m%d%H%M%S -0500")

        xml += f'  <programme start="{start_str}" stop="{end_str}" channel="{canal_id}">\n'
        xml += f'    <title>{titulo}</title>\n'
        xml += f'  </programme>\n'

    xml += '</tv>'

    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(xml)

if __name__ == "__main__":
    generar_epg()
