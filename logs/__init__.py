import logging

log_handlers = [logging.FileHandler("./logs/debug.log"), logging.StreamHandler()]
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=log_handlers,
)
logger = logging.getLogger(__name__)