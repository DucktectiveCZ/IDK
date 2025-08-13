from game import Game
from dotenv import load_dotenv
import logging
import os
import tkinter as tk
from tkinter import messagebox
from scenes import MenuScene
import traceback


def show_error_dialog(title: str, msg: str) -> None:
    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(title, msg)


if __name__ == '__main__':
    app_title = 'duk game'
    app_version = '0.1.0'

    load_dotenv()
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info(f"Log level: {log_level} aka {numeric_level}")
    logging.info("quak<3")
    logging.info(f"Starting {app_title} v{app_version}...")

    try:
        Game(app_title, MenuScene()).start()
    except RuntimeError as err:
        logging.critical(f"Critical exception: {err}")
        show_error_dialog(
            app_title,
            f"A critical error has occured: {err}"
        )
        exit(1)
    except Exception as err:
        logging.critical(f"Critical unexpected exception: {err}")
        logging.critical("Stack trace:")
        traceback.print_exc()
        show_error_dialog(
            app_title,
            f"An unexpected error has occured: {err}",
        )
        exit(1)
