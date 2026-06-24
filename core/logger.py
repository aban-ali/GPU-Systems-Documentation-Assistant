import logging
from os import path

def setup_logger(name:str):
    filepath = path.join("logs", name+".log")
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )

    ## no need to create logger for console since uvicorn already handles it.
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filepath)
    file_handler.setFormatter(formatter)

    # logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger