import logging
import os
import time
import threading
import random
import string
import re
from selenium.webdriver.common.by import By

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def generate_authority_code():
    """Regenerates a new AUTHORITY_CODE every minute."""
    while True:
        new_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        os.environ["AUTHORITY_CODE"] = new_code
        logger.info(f"🔑 New Authority Code: {new_code}")
        time.sleep(60)


# Start the authority code generator in a separate thread
threading.Thread(target=generate_authority_code, daemon=True).start()


def open_friend_list(driver):
    """
    Opens the friend list in Pony Town by clicking the Friends button.
    Uses driver.click() with the appropriate CSS selector.
    """
    try:
        driver.click('ui-button[title="Friends"] button', timeout=10)
        time.sleep(1)  # Wait for the friend list to load
        logger.info("📂 Friend list opened.")
        return True
    except Exception as e:
        print("❌ Error opening friend list:", e)
        return False


def close_friend_list(driver, max_days):
    """
    Closes the friend list in Pony Town by clicking the Friends button.
    Uses driver.click() with the appropriate CSS selector.
    """
    try:
        driver.click('ui-button[title="Friends"] button', timeout=10)
        time.sleep(1)
        logger.info("📂 Friend list closed.")
        try:
            driver.click(
                'ui-button[title="Toggle chat"] button', timeout=5
            )  # Toggle chat
        except Exception as e:
            print("Toggle err:", e)
        time.sleep(0.5)  # Wait
        try:
            driver.type(
                'textarea[aria-label="Chat message"]',
                f"Success deleting friends offline more than {max_days} days!",
            )
        except Exception as e:
            print("Type err:", e)
        try:
            driver.click(
                'ui-button[title="Send message (hold Shift to send without closing input)"] button',
                timeout=5,
            )  # Send msg
        except Exception as e:
            print("Send err:", e)
        return True
    except Exception as e:
        print("❌ Error opening friend list:", e)
        return False


def delete_old_friends(driver, input_code, max_days):

    # Verify the authority code
    if input_code != os.getenv("AUTHORITY_CODE"):
        logger.warning("❌ Invalid Authority Code!")
        return

    logger.info(f"🔍 Checking for friends offline more than {max_days} days...")

    # Open the friend list
    if not open_friend_list(driver):
        logger.warning("❌ Failed to open Friend List. Aborting deletion.")
        return

    try:
        # Find all friend elements (adjust selector if needed)
        friends = driver.find_elements(By.CSS_SELECTOR, ".friends-item")
        for friend in friends:
            try:

                friend_text = friend.get_attribute("textContent")
                # Extract offline days from text like "Seen 158d ago"
                match = re.search(r"Seen\s+(\d+)d\s+ago", friend_text)
                if match:
                    days_offline = int(match.group(1))
                    if days_offline > max_days:
                        try:
                            # Click the friend element to open the options modal
                            friend.click()
                            time.sleep(5)

                            try:
                                remove_button = driver.find_element(
                                    By.CSS_SELECTOR,
                                    'button[title="Remove this player from the friend list"]',
                                )
                                remove_button.click()
                                time.sleep(2)
                                remove_button_confirm = driver.find_element(
                                    By.XPATH,
                                    '//button[contains(@class, "btn-outline-danger") and contains(text(), "Remove")]',
                                )
                                remove_button_confirm.click()
                            except Exception as e:
                                print("Error clicking remove button:", e)

                            logger.info(
                                f"🗑️ Deleted friend last seen {days_offline} days ago."
                            )
                            time.sleep(1)
                        except Exception as e:
                            print("❌ Error removing friend:", e)
            except Exception:
                pass
        logger.info("✅ Deletion process completed.")
        close_friend_list(driver, max_days)
        logger.info("close the friendlists")
    except Exception as e:
        print("❌ Error processing friend list:", e)


def process_delete_command(driver, cmd, arg):
    """
    Handles the .delete command to remove inactive friends.
    Command format: .delete <AUTHORITY_CODE> <DAYS_LIMIT>
    """
    if cmd == "delete" and arg:
        try:
            args = arg.split(" ")
            if len(args) == 2:
                input_code = args[0]
                days_limit = int(args[1])
                delete_old_friends(driver, input_code, days_limit)
            else:
                logger.info(
                    "❌ Invalid .delete command format. Use: .delete <AUTHORITY_CODE> <DAYS_LIMIT>"
                )
        except Exception as e:
            print("❌ Command error:", e)
    else:
        logger.info(f"📝 Command: {cmd} {arg}")
