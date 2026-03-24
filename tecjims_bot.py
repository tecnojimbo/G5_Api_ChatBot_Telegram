
import telebot
import requests
from telebot import types

TOKEN = '8612400251:AAFoCRt3YuzJOKZmIIbMnjRxtblIvxog-tk'
# API_URL = "http://127.0.0.1:5000/api"
API_URL = "http://api-tecjims:5000/api"
bot = telebot.TeleBot(TOKEN)

# Memoria temporal para el carrito de cada usuario
sesiones_compra = {}

@bot.message_handler(commands=['start', 'hola'])
def menu_inicio(message):
    uid = message.from_user.id
    sesiones_compra[uid] = [] # Resetear/Crear carrito
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💻 Laptops", callback_data='cat_Laptops'),
        types.InlineKeyboardButton("🖱️ Mouse", callback_data='cat_Mouse'),
        types.InlineKeyboardButton("🔊 Audio", callback_data='cat_Audio'),
        types.InlineKeyboardButton("💾 Discos/USB", callback_data='cat_Almacenamiento'),
        types.InlineKeyboardButton("🌐 Redes", callback_data='cat_Redes')
    )
    bot.send_message(message.chat.id, "👋 ¡Hola! Bienvenido a **TecJims**.\nSelecciona una categoría para empezar tu pedido:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def mostrar_catalogo(call):
    categoria = call.data.replace('cat_', '')
    items = requests.get(f"{API_URL}/productos/{categoria}").json()
    
    if not items:
        bot.send_message(call.message.chat.id, "No hay stock de este rubro.")
        return

    for i in items:
        markup = types.InlineKeyboardMarkup()
        # Callback: add_ID_NOMBRE_PRECIO
        btn = types.InlineKeyboardButton(f"🛒 Agregar ${i['precio']}", callback_data=f"add_{i['id']}_{i['nombre']}_{i['precio']}")
        markup.add(btn)
        bot.send_message(call.message.chat.id, f"📦 *{i['nombre']}*\n💰 Precio: ${i['precio']}\n🔢 Stock: {i['stock']}", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def procesar_seleccion(call):
    _, p_id, p_nom, p_pre = call.data.split('_')
    uid = call.from_user.id
    
    # Descontamos stock en la API
    requests.post(f"{API_URL}/comprar/{p_id}")

    # Guardamos en el carrito local
    if uid not in sesiones_compra: sesiones_compra[uid] = []
    sesiones_compra[uid].append({"nombre": p_nom, "precio": float(p_pre)})

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("➕ Seguir comprando", callback_data='volver_menu'))
    markup.add(types.InlineKeyboardButton("🧾 YA NO QUIERO MÁS (Ver Total)", callback_data='finalizar'))
    
    bot.send_message(call.message.chat.id, f"✅ Has agregado: **{p_nom}**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == 'finalizar')
def generar_factura(call):
    uid = call.from_user.id
    carrito = sesiones_compra.get(uid, [])
    
    if not carrito:
        bot.send_message(call.message.chat.id, "No has seleccionado productos aún.")
        return

    subtotal = sum(item['precio'] for item in carrito)
    iva = subtotal * 0.15 # IVA 15% (Ecuador)
    total = subtotal + iva

    resumen = "🧾 **RESUMEN DE TU PEDIDO - TECJIMS**\n\n"
    for item in carrito:
        resumen += f"• {item['nombre']}: ${item['precio']:.2f}\n"
    
    resumen += f"\n----------------------------"
    resumen += f"\n🔹 **Subtotal:** ${subtotal:.2f}"
    resumen += f"\n🔹 **IVA (15%):** ${iva:.2f}"
    resumen += f"\n✅ **TOTAL A PAGAR:** ${total:.2f}"
    resumen += f"\n----------------------------"
    resumen += f"\n\n💵 **Pago:** Efectivo al retirar\n📍 **Lugar:** Local TecJims (Guayaquil)\n📞 **Contacto:** 0983810181"
    resumen += f"\n\n¡Gracias por preferir TecJims!"

    bot.send_message(call.message.chat.id, resumen, parse_mode="Markdown")
    sesiones_compra[uid] = [] # Limpiar carrito tras finalizar

@bot.callback_query_handler(func=lambda call: call.data == 'volver_menu')
def regresar(call):
    menu_inicio(call.message)

print("🤖 Bot TecJims (Versión Carrito) Online...")
bot.polling()