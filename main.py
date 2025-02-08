from seleniumbase import Driver
import time
from dotenv import load_dotenv
import os
import threading
import logging
from selenium.webdriver.common.by import By
from utils.friends import accept_friend_request
from utils.handler import check_message_and_click_button, auto_canvas_click
from utils.select_chat import select_personal_chat

# Load env
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Cookies
COOKIES = [
    {"name": "cf_clearance", "value": os.getenv("CF_CLEARANCE"), "domain": "pony.town"},
    {"name": "session", "value": os.getenv("SESSION_ID"), "domain": "pony.town"},
]

BOT_VERSION = "1.2.0"
BOT_NAME = "LunaAI"
url = "https://pony.town"


def get_startup_banner(latency, driver):
    ascii_bunny = r"""
(\(\        LunaAI - Pony Town AI Assistant
( -.-)      Version: {}
o__(")(")   URL DIRECT: {}
""".format(
        BOT_VERSION, url
    )

    banner = f"\033[95m{ascii_bunny}\033[0m"
    banner += f"\033[94m✅ {BOT_NAME} is now online! Connected as: \n{driver.get_user_agent()}\033[0m\n"
    banner += f"\033[92m📡 Latency: {latency}ms\033[0m\n"
    banner += "-" * 50
    return banner


def main():
    # Init driver
    driver = Driver(uc=True, headless=True, chromium_arg="--mute-audio")
    try:
        # Open page with reconnect
        start_time = time.time()
        driver.uc_open_with_reconnect(url, 10)
        latency = (time.time() - start_time) * 1000

        # Print latency and banner
        print(get_startup_banner(latency, driver))

        # Bypass CloudFlare
        # Only use this if you use headless=True
        logger.warning("Start Bypassing CloudFlare...")
        try:
            logger.warning("Click CAPTCHA...")
            driver.uc_gui_click_captcha()
            time.sleep(3)
            logger.info("CAPTCHA OK.")
        except Exception as e:
            print("CAPTCHA err:", e)
        finally:
            logger.info("Bypass successful!")

        # Tab fix
        handles = driver.window_handles
        target = None  # Target tab
        for handle in handles:
            driver.switch_to.window(handle)
            if "pony.town" in driver.current_url:
                target = handle
                break
        if target:
            for handle in handles:
                if handle != target:
                    driver.switch_to.window(handle)
                    print("Closing:", driver.current_url)
                    driver.close()
            driver.switch_to.window(target)
        else:
            driver.get(url)
            time.sleep(5)
        print("Fixed URL:", driver.current_url)
        time.sleep(5)

        # Add cookies
        for cookie in COOKIES:
            try:
                driver.add_cookie(cookie)
            except Exception:
                script = (
                    f"document.cookie = '{cookie['name']}={cookie['value']}; "
                    f"domain={cookie['domain']}; path=/';"
                )
                driver.execute_script(script)
        driver.refresh()
        time.sleep(5)

        # Click play
        try:
            driver.click('//button[contains(@class, "btn-lg btn-success")]', timeout=10)
            logger.info("Play clicked.")
        except Exception as e:
            logger.error("Click err:", e)
            return

        time.sleep(10)

        # auto set to personal log chat
        select_personal_chat(driver, By)
        # Start threads for chat and canvas auto-click
        chat_thread = threading.Thread(
            target=check_message_and_click_button, args=(driver, logger), daemon=True
        )
        chat_thread.start()
        canvas_thread = threading.Thread(
            target=auto_canvas_click, args=(driver,), daemon=True
        )
        canvas_thread.start()

        logger.warning("Bot idle. Press Ctrl+C to exit.")

        # auto add friend request & loop idle
        while True:
            accept_friend_request(driver)
            time.sleep(5)

        # while True:
        #     # Idle loop
        #     time.sleep(60)

    finally:
        logger.info("Quitting driver...")
        driver.quit()


if __name__ == "__main__":
    main()
