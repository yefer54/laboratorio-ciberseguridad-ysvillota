#!/bin/sh
apk add --no-cache curl bind tools
echo "--- PRUEBA HTTP ---"
curl -I https://servidor-web-dez.onrender.com
echo "--- INICIANDO SERVIDOR ---"
python -m http.server 8000
