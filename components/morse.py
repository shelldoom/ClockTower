from telegram import Update
from telegram.ext import CallbackContext, Filters, CommandHandler
from logs import logger

MORSE_CODE_LOOKUP = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ", ": "--..--",
    ",": "--..--",
    ".": ".-.-.-",
    "?": "..--..",
    "/": "-..-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",
    "'": ".----.",
    "!": "-.-.--",
    ":": "---...",
    "_": "..--.-",
    "$": "...-..-",
    "@": ".--.-.",
    "=": "-...-",
    " ": "  ",
    "": "",
    "\n": "\n\n",
    "&": ".-...",
}
REVERSE_CODE_LOOKUP = {v: k for k, v in MORSE_CODE_LOOKUP.items()}


def encode(query: str, spacing: int = 4) -> str:
    query = query.capitalize().split(" ")
    word_separator = " " * spacing
    for i in range(len(query)):
        query[i] = [MORSE_CODE_LOOKUP[char] for char in query[i]]
    result = word_separator.join([" ".join(word) for word in query])
    return result


def decode(query: str, spacing: int = 4) -> str:
    validate_morse(query)
    word_separator = " " * spacing
    result = ""
    for word in query.split(word_separator):
        for char in word.split(" "):
            result += REVERSE_CODE_LOOKUP[char]
        result += " "
    return result


def validate_morse(query: str) -> str:
    check = {" ", "", "-", ".", "\n"}
    for char in query:
        if char not in check:
            raise ValueError("Invalid morse code!")
    return


MORSE_ENCODE_HELP = """
Input: Reply /mce to the message containing text
Output: Converts and returns its morse code version

Example:
<code>message 1: SOS </code>
<code>message 2: /morsecode </code>
Here <code>message 2</code> is a reply to <code>message 1</code>.

You can also use /mce instead of /morsecode. For decoding a morse code, you can use the /decodemorse or /mcd command.
"""

MORSE_DECODE_HELP = """
Input: Reply /mcd to the message containing the morse code
Output: Converts and returns in its text form

Example:
<code>Message 1:  ... --- ... </code>
<code>Message 2: /decodemorse </code>
Here <code>message 2</code> is a reply to <code>message 1</code>.

You can also use /mcd instead of /decodemorse. To convert a word to a morse code, you can use the /mce command.
"""

# /mce
def mce_callback(update: Update, context: CallbackContext):
    parentMsg = update.effective_message.reply_to_message

    if not parentMsg:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.message_id,
            text=MORSE_ENCODE_HELP,
            parse_mode="HTML",
        )
        return
    userQuery = parentMsg.text
    result = f"<code> {encode(userQuery)} </code>"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=parentMsg.message_id,
        text=result,
        parse_mode="HTML",
    )


mc_handler = CommandHandler(
    ["morse", "mce", "morsecode", "mc"],
    mce_callback,
    filters=~Filters.update.edited_message,
)


# /mcd
def mcd_callback(update: Update, context: CallbackContext):
    parentMsg = update.effective_message.reply_to_message
    if parentMsg:
        userQuery = parentMsg.text

        try:
            result = f"<code> {decode(userQuery)} </code>"
        except ValueError:
            logger.info("User tried invalid morse code expression")
            return
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=parentMsg.message_id,
            text=result,
            parse_mode="HTML",
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.message_id,
            text=MORSE_DECODE_HELP,
            parse_mode="HTML",
        )


mcd_handler = CommandHandler(
    ["decodemorse", "mcd"], mcd_callback, filters=~Filters.update.edited_message
)