from telegram.ext import Dispatcher
from components.helper_func import mapper
from components.urban_dict import urbanHandler
from components.qr_code import qr_handler
from components.calc import calc_handler
from components.basic_cmds import (
    start_handler,
    help_handler,
    donate_handler,
    ob_handler,
    echo_handler,
)
from components.clg_cmds import ar_handler, hub_handler, bulletin_handler, cal_handler
from components.upload_img import imgup_handler
from components.morse import mc_handler, mcd_handler
from components.quote import quote_handler
from components.feedback import feedback_handler


def setup(dispatcher: Dispatcher) -> None:
    dispatcher.add_handler(urbanHandler)
    dispatcher.add_handler(qr_handler)
    dispatcher.add_handler(calc_handler)
    mapper(
        dispatcher.add_handler,
        [start_handler, help_handler, donate_handler, ob_handler, echo_handler],
    )
    dispatcher.add_handler(mc_handler)
    dispatcher.add_handler(mcd_handler)
    dispatcher.add_handler(quote_handler)
    mapper(
        dispatcher.add_handler, [ar_handler, hub_handler, bulletin_handler, cal_handler]
    )
    dispatcher.add_handler(feedback_handler)
    dispatcher.add_handler(imgup_handler)