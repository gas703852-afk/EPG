from datetime import datetime, timedelta

# Hora actual
now = datetime.utcnow()

# Crear contenido XML básico
epg = '''<?xml version="1.0" encoding="UTF-8"?>
<tv>
  <channel id="ATV">
    <display-name>ATV</display-name>
  </channel>
'''

# Generar programación simple (24 horas)
for i in range(24):
    start = now + timedelta(hours=i)
    stop = start + timedelta(hours=1)

    start_str = start.strftime("%Y%m%d%H%M%S -0500")
    stop_str = stop.strftime("%Y%m%d%H%M%S -0500")

    epg += f'''
  <programme start="{start_str}" stop="{stop_str}" channel="atv.pe">
    <title>Programa {i+1}</title>
    <desc>Contenido de prueba</desc>
  </programme>
'''

epg += '</tv>'

# Guardar archivo
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(epg)

print("EPG generado correctamente")
