import time


def say_self(driver, cmd, arg):
    if cmd == "say" and arg:
        try:
            driver.click(
                'ui-button[title="Toggle chat"] button', timeout=5
            )  # Toggle chat
        except Exception as e:
            print("Toggle err:", e)
        time.sleep(0.5)  # Wait
        try:
            driver.type('textarea[aria-label="Chat message"]', arg)  # Type msg
        except Exception as e:
            print("Type err:", e)
        try:
            driver.click(
                'ui-button[title="Send message (hold Shift to send without closing input)"] button',
                timeout=5,
            )  # Send msg
        except Exception as e:
            print("Send err:", e)
    else:
        print(f"Say: {cmd} {arg}")
