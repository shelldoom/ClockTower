import html

SOURCE_MSG = """
https://github.com/shelldoom/ClockTower
"""

HELP_MSG = f"""
Hey there user!

Commands available:

■ /start - start the bot
■ /help - prints this message
■ /feedback - send feedback about the bot to creator

■ /dc - prints current working hubs
■ /ar - academic resources
■ /cal - academic calendar
■ /bulletin - bulletin
■ /ob - ob

■ /echo - echo provided message
■ /ud - get {html.escape('<query>')} definition from urban dictionary
■ /imgup - get image link
■ /eval - evaluate a arithmetic expression
■ /quote - get random quote
■ /qr - convert text to qr code image
■ /mce - convert text to morse code (encode)
■ /mcd - convert morse code to text (decode)
"""

GRP_START_MSG = """
Hello, I'm a bot. To get started, message <code>/help</code> here or in PM.
"""

START_STICKER = [
    "CAACAgUAAxkBAAOUYDJijcwk9X2zR17RDsY7Qr9oNvcAAgEAA-oMEiJCjYpRVlxi-x4E",
    "CAACAgUAAxkBAAOqYDJmQ14qo5et_dLPKoN4mO5DeRcAArwBAALsdahVjAABA0_ZyqQRHgQ",
]

DONATE_MSG = """
https://ko-fi.com/virtualize
"""

DC_MSG = """
No hubs running. Know any active hubs that are not listed here ? Use /feedback command to send the info about such.
"""

AR_MSG = """
No resources are available at the moment. Are you willing to contribute any resources or have a link ? Use /feedback to send any resources.
"""


HEY_STICKER = "CAACAgUAAxkBAAOUYDJijcwk9X2zR17RDsY7Qr9oNvcAAgEAA-oMEiJCjYpRVlxi-x4E"
LOADING_STICKER = (
    "CAACAgUAAxkBAAOqYDJmQ14qo5et_dLPKoN4mO5DeRcAArwBAALsdahVjAABA0_ZyqQRHgQ",
)
