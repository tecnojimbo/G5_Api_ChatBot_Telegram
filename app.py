from flask import Flask, jsonify, request
import json

app = Flask(__name__)
DB_FILE = 'datos.json'

def gestionar_bd(accion, datos_nuevos=None):
    if accion == 'leer':
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif accion == 'escribir':
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(datos_nuevos, f, indent=4, ensure_ascii=False)

@app.route('/api/productos/<cat>', methods=['GET'])
def obtener_productos(cat):
    db = gestionar_bd('leer')
    filtrados = [p for p in db['productos'] if p['categoria'].lower() == cat.lower()]
    return jsonify(filtrados)

@app.route('/api/comprar/<int:id_p>', methods=['POST'])
def procesar_compra(id_p):
    db = gestionar_bd('leer')
    for p in db['productos']:
        if p['id'] == id_p and p['stock'] > 0:
            p['stock'] -= 1
            gestionar_bd('escribir', db)
            return jsonify({"res": "ok"})
    return jsonify({"res": "error"}), 400

if __name__ == '__main__':
    print("🚀 Servidor TecJims listo en http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
    