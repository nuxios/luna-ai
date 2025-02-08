import time


def select_personal_chat(driver, By):
            """
            Automatically selects the 'Personal' chat tab in Pony Town.
            """
            try:
            # Find all chat tab elements
                chat_tabs = driver.find_elements(By.CSS_SELECTOR, ".chat-log-tabs a")

                for tab in chat_tabs:
                    if tab.text.strip().lower() == "personal":
                        print("Switching to Personal chat...")
                        tab.click()
                        time.sleep(1)
                        break
            except Exception as e:
                print("Error selecting Personal chat:", e)