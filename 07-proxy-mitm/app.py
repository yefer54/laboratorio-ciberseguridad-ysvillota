from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# URL del servidor objetivo en la DMZ
TARGET_DMZ = "https://servidor-web-dmz-ebl.onrender.com"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mitm_proxy(path):
    # 1. Registrar la petición interceptada (Salida inmediata con flush=True)
    print(f"\n[MITM INTERCEPTADO] Petición entrante hacia la ruta: /{path}", flush=True)
    print(f"[CABECERAS INTERCEPTADAS] {dict(request.headers)}", flush=True)

    # 2. Construir la URL de destino evitando la doble barra '//'
    url = f"{TARGET_DMZ}/{path}" if path else f"{TARGET_DMZ}/"

    try:
        # Reenviar la petición HTTP al servidor DMZ
        if request.method == 'GET':
            resp = requests.get(url, timeout=5)
        elif request.method == 'POST':
            resp = requests.post(url, data=request.form, timeout=5)
        else:
            resp = requests.request(request.method, url, timeout=5)

        contenido_original = resp.text
        status_code = resp.status_code
    except Exception as e:
        print(f"[ERROR MITM] No se pudo conectar con la DMZ: {str(e)}", flush=True)
        contenido_original = f"<h1>Error al conectar con la DMZ</h1><p>{str(e)}</p>"
        status_code = 502

    # 3. Inyección / Alteración de la respuesta (Ataque Man-in-the-Middle)
    payload_mitm = "\n\n<!-- [ALERTA MITM] Este contenido fue alterado en tránsito por el Proxy Interceptor -->"
    contenido_alterado = contenido_original + payload_mitm

    print("[MITM ALERTA] Respuesta modificada e inyectada con éxito.", flush=True)

    # 4. Devolver la respuesta alterada al cliente final
    return Response(contenido_alterado, status=status_code, mimetype='text/html')

if __name__ == '__main__':
    # Usar el puerto de Render si existe o 8080 por defecto
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
