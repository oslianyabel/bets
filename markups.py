from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def menu_markup():
    apuestas = InlineKeyboardButton("🎲Apuestas", callback_data="apuestas")
    combinadas = InlineKeyboardButton("🔀Combinadas", callback_data="combinadas")
    movimientos = InlineKeyboardButton("💹Movimientos", callback_data="movimientos")
    bonos = InlineKeyboardButton("🎁Bonos por referencia", callback_data="bonos")
    grupo = InlineKeyboardButton("💬Grupo chat", url="https://t.me/Osliany")
    terminos = InlineKeyboardButton("📜Terminos", callback_data="terminos")
    reglas = InlineKeyboardButton("⚖️Reglas", callback_data="reglas")
    soporte = InlineKeyboardButton("📞Soporte", url="https://t.me/Osliany")

    markup = InlineKeyboardMarkup()
    markup.row(apuestas, combinadas)
    markup.row(movimientos, bonos)
    markup.row(grupo)
    markup.row(terminos, reglas)
    markup.row(soporte)

    return markup


def apuestas_markup():
    beisbol = InlineKeyboardButton("⚾Béisbol", callback_data="beisbol")
    futbol = InlineKeyboardButton("⚽Fútbol", callback_data="futbol")
    baloncesto = InlineKeyboardButton("🏀Baloncesto", callback_data="baloncesto")
    tenis = InlineKeyboardButton("🎾Tenis", callback_data="tenis")
    ufc = InlineKeyboardButton("🥋UFC", callback_data="ufc")
    boxeo = InlineKeyboardButton("🥊Boxeo", callback_data="boxeo")
    futbol_americano = InlineKeyboardButton(
        "🏈Fútbol Americano", callback_data="futbol_americano"
    )
    balonmano = InlineKeyboardButton("🤾Balonmano", callback_data="balonmano")
    regresar = InlineKeyboardButton("↩️Regresar", callback_data="menu")

    markup = InlineKeyboardMarkup()
    markup.row(futbol, beisbol)
    markup.row(baloncesto, tenis)
    markup.row(ufc, boxeo)
    markup.row(futbol_americano)
    markup.row(balonmano)
    markup.row(regresar)

    return markup


def movimientos_markup():
    mi_saldo = InlineKeyboardButton("💰Mi Saldo", callback_data="mi_saldo")
    recarga = InlineKeyboardButton("💳Recarga", callback_data="recarga")
    retiros = InlineKeyboardButton("📤Retiros", callback_data="retiros")
    transferencia_interna = InlineKeyboardButton(
        "📨Transferencia Interna", callback_data="transferencia"
    )
    regresar = InlineKeyboardButton("↩️Regresar", callback_data="menu")

    markup = InlineKeyboardMarkup()
    markup.row(mi_saldo)
    markup.row(recarga, retiros)
    markup.row(transferencia_interna)
    markup.row(regresar)

    return markup


def futbol_markup():
    arabia = InlineKeyboardButton("Arabia Saudí", callback_data="arabia")
    alemania = InlineKeyboardButton("Alemania", callback_data="alemania")
    italia = InlineKeyboardButton("Italia", callback_data="italia")
    francia = InlineKeyboardButton("Francia", callback_data="francia")
    españa = InlineKeyboardButton("España", callback_data="españa")
    championship = InlineKeyboardButton("Championship", callback_data="championship")
    rusia = InlineKeyboardButton("Rusia", callback_data="rusia")
    paises_bajos = InlineKeyboardButton("Países bajos", callback_data="paises_bajos")
    turquia = InlineKeyboardButton("Turquía", callback_data="turquia")
    portugal = InlineKeyboardButton("Portugal", callback_data="portugal")
    australia = InlineKeyboardButton("Australia", callback_data="australia")
    belgica = InlineKeyboardButton("Bélgica", callback_data="belgica")
    rumania = InlineKeyboardButton("Rumanía", callback_data="rumania")
    mexico = InlineKeyboardButton("México", callback_data="mexico")
    argentina = InlineKeyboardButton("Argentina", callback_data="argentina")
    colombia = InlineKeyboardButton("Colombia", callback_data="colombia")

    markup = InlineKeyboardMarkup()
    markup.row(arabia, alemania)
    markup.row(italia, francia)
    markup.row(españa)
    markup.row(championship, rusia)
    markup.row(paises_bajos, turquia)
    markup.row(portugal, australia)
    markup.row(belgica, rumania)
    markup.row(mexico, argentina)
    markup.row(colombia)

    return markup


def reglas_markup():
    beisbol = InlineKeyboardButton("⚾Beisbol", callback_data="reglas_beisbol")
    futbol = InlineKeyboardButton("⚽Fútbol", callback_data="reglas_futbol")
    baloncesto = InlineKeyboardButton("🏀Baloncesto", callback_data="reglas_baloncesto")
    tenis = InlineKeyboardButton("🎾Tenis", callback_data="reglas_tenis")
    ufc = InlineKeyboardButton("🥋UFC", callback_data="reglas_ufc")
    boxeo = InlineKeyboardButton("🥊Boxeo", callback_data="reglas_boxeo")
    futbol_americano = InlineKeyboardButton(
        "🏈Fútbol Americano", callback_data="reglas_futbol_americano"
    )
    balonmano = InlineKeyboardButton("🤾Balonmano", callback_data="reglas_balonmano")
    regresar = InlineKeyboardButton("↩️Regresar", callback_data="menu")

    markup = InlineKeyboardMarkup()
    markup.row(futbol, beisbol)
    markup.row(baloncesto, tenis)
    markup.row(ufc, boxeo)
    markup.row(futbol_americano)
    markup.row(balonmano)
    markup.row(regresar)

    return markup
