import subprocess, re

ARCHIVOS = ["lista_por_categorias (1).m3u"]  # los que existan en tu repo

# ID del live de Dailymotion -> nombre (solo informativo)
CANALES = {
    "xa63dow": "Willax TV",
    "xa50i1c": "Panamericana TV",
}

def link_fresco(video_id):
    r = subprocess.run(
        ["yt-dlp", "-g", f"https://www.dailymotion.com/video/{video_id}"],
        capture_output=True, text=True,
    )
    if r.returncode != 0 or not r.stdout.strip():
        print(f"FALLÓ {video_id}: {r.stderr[:200]}")
        return None
    return r.stdout.strip().splitlines()[0]

nuevos = {vid: link_fresco(vid) for vid in CANALES}

for archivo in ARCHIVOS:
    try:
        with open(archivo, encoding="utf-8", newline="") as f:
            texto = f.read()
    except FileNotFoundError:
        continue
    for vid, link in nuevos.items():
        if link:
            # reemplaza solo la línea del link, respeta los saltos de línea \r\n
            texto = re.sub(
                rf"https://cdndirector\.dailymotion\.com/cdn/live/video/{vid}\.m3u8[^\r\n]*",
                link, texto,
            )
    with open(archivo, "w", encoding="utf-8", newline="") as f:
        f.write(texto)
