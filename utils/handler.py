import time
from selenium.webdriver.common.by import By
from commands.say import say_self
from commands.model import chat_command
from commands.friendlist import process_delete_command

# Timer for Anti-AFK
last_command_time = time.time()


def check_message_and_click_button(driver, logger):
    """
    Listens for chat messages and processes commands starting with '.'
    """
    global last_command_time
    last_msg = None  # Track last message

    while True:
        try:
            # Get all messages and names
            msgs = driver.find_elements(By.CSS_SELECTOR, ".chat-line-message")
            names = driver.find_elements(By.CSS_SELECTOR, ".chat-line-name-content")

            if msgs and names:
                msg = msgs[-1].text.strip()  # Last message
                nick = names[-1].text.strip()  # Sender name

                # Process new messages
                if msg and msg != last_msg:
                    logger.info(f"💬 Msg from {nick}: {msg}")

                    if msg.startswith("."):  # Check if message is a command
                        last_command_time = time.time()  # Reset AFK Timer

                        # Parse command
                        parts = msg[1:].split(" ")
                        cmd = parts[0]  # Extract command keyword
                        arg = " ".join(parts[1:]) if len(parts) > 1 else ""
                        emote = msg[3:] if msg.startswith(".e") else None

                        # Execute other commands
                        process_delete_command(driver, cmd, arg)
                        say_self(driver, cmd, arg)
                        chat_command(driver, cmd, arg, nick)
                        emote_play(driver, emote)
                        ai_handler(driver, cmd, arg, nick)

                    last_msg = msg  # Save last processed message

            time.sleep(1)  # Prevent excessive looping

        except KeyboardInterrupt:
            print("🛑 Bot stopped.")
            break
        except Exception as e:
            print("❌ Chat error:", e)
            time.sleep(2)


# 🔹 Anti-AFK Feature
def auto_canvas_click(driver):
    """
    Clicks on the game canvas every 4 minutes if no commands are used.
    """
    global last_command_time
    while True:
        try:
            if time.time() - last_command_time >= 240:  # 4 min inactivity
                try:
                    canvas = driver.find_element(By.TAG_NAME, "canvas")
                    canvas.click()
                    print("🎮 Anti-AFK: Canvas clicked.")
                except Exception as ce:
                    print("⚠️ Canvas click error:", ce)

                last_command_time = time.time()  # Reset timer
            time.sleep(10)  # Check every 10 sec
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("❌ Auto-AFK error:", e)
            time.sleep(2)


def emote_play(driver, emote):
    if emote:
        print("🎭 Emote:", emote)


def ai_handler(driver, cmd, arg, nick):
    print("🤖 AI:", cmd, arg, "from", nick)
