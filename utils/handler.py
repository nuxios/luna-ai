import time
from selenium.webdriver.common.by import By
from commands.say import say_self
from commands.model import chat_command

# Timer
last_command_time = time.time()


def check_message_and_click_button(driver, logger):
    global last_command_time
    # Last msg
    last_msg = None
    while True:
        try:
            msgs = driver.find_elements(
                By.CSS_SELECTOR, ".chat-line-message"
            )  # Get msgs
            names = driver.find_elements(
                By.CSS_SELECTOR, ".chat-line-name-content"
            )  # Get names
            if msgs and names:
                # Last msg
                msg = msgs[-1].text.strip()
                # Last nick
                nick = names[-1].text.strip()
                # New msg
                if msg and msg != last_msg:
                    logger.info(f"Msg from {nick}: {msg}")
                    if msg.startswith("."):
                        # Reset timer
                        last_command_time = time.time()
                        # Parse msg
                        parts = msg[1:].split(" ")
                        cmd = parts[0]
                        arg = " ".join(parts[1:]) if len(parts) > 1 else ""
                        emote = msg[3:] if msg.startswith(".e") else None
                        # Say cmd
                        say_self(driver, cmd, arg)
                        # Emote
                        chat_command(driver, cmd, arg, nick)
                        emote_play(driver, emote)
                        # AI
                        ai_handler(driver, cmd, arg, nick)
                    # Save msg
                    last_msg = msg
            # Delay
            time.sleep(1)
        except KeyboardInterrupt:
            # Stop
            print("Bot stop")
            break
        except Exception as e:
            print("Chat err:", e)
            time.sleep(2)


# Anti afk feature
def auto_canvas_click(driver):
    global last_command_time
    while True:
        try:
            if time.time() - last_command_time >= 240:
                try:
                    # Find canvas
                    canvas = driver.find_element(By.TAG_NAME, "canvas")
                    # Click canvas
                    canvas.click()
                    print("Canvas clicked.")
                except Exception as ce:
                    print("Canvas err:", ce)
                # Reset timer
                last_command_time = time.time()
            # Loop delay
            time.sleep(10)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Auto err:", e)
            time.sleep(2)


def emote_play(driver, emote):
    if emote:
        print("Emote:", emote)


def ai_handler(driver, cmd, arg, nick):
    print("AI:", cmd, arg, "from", nick)
