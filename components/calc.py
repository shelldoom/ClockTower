from components.helper_func import replace_all
from telegram import Update
from telegram.ext import CallbackContext, Filters, CommandHandler
from typing import Optional
import subprocess
from logs import logger
import platform


calc_msg = """
Input: Arithmetic Expression

Example:
<code>/calc 9 + 2.4 - 3*4 + 2^2 + 14/2 + 6 % 2 + pi </code>
"""

operands = ["^", "*", "/", "%", "+", "-"]
digits = ["(", ")", ".", " ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def evaluate(userQuery: str) -> Optional[str]:
    operand_count = 0
    digit_count = 0
    if "**" in userQuery:
        return
    userQuery = replace_all(userQuery, {"x": "*", "^": "**", "pi": "3.1415926535"})
    for char in userQuery:
        if char in operands:
            operand_count += 1
        if char in digits and char != " ":
            digit_count += 1
        if char not in operands and char not in digits:
            return
    if operand_count == 0 or digit_count == 0:
        return
    if digit_count > 30:
        return
    try:
        # Change python3 to python for windows
        python_command = (
            "python3" if not platform.system().lower() == "windows" else "python"
        )
        # Times out if the computation is expensive
        r = subprocess.run(
            [python_command, "./components/eval_calc.py", f"{userQuery}"],
            timeout=2,
            capture_output=True,
            text=True,
        )
        result = r.stdout
    except subprocess.TimeoutExpired:
        logger.info(f"User tried a expression {userQuery}, but failed due to timeout.")
        return
    if len(result) == 0 or len(result) > 4000:
        return
    return f"<code>{result}</code>"


def calc_callback(update: Update, context: CallbackContext):
    userQuery = " ".join(context.args)
    if userQuery in {"", " "}:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.message_id,
            text=calc_msg,
            parse_mode="HTML",
        )
        return

    result = evaluate(userQuery)
    if not result:
        return
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        text=result,
        parse_mode="HTML",
    )


calc_handler = CommandHandler(
    ["calc", "eval", "calculator"],
    calc_callback,
    filters=~Filters.update.edited_message,
    run_async=True,
)
