import time
from selenium.webdriver.common.by import By


def accept_friend_request(driver):
    """
    Automatically accepts friend requests if the 'Accept' button appears.
    """
    try:
        # Locate friend request notification
        friend_request = driver.find_elements(
            By.XPATH, "//b[contains(text(), 'Friend request')]"
        )

        if friend_request:
            print("Friend request detected!")

            # Locate and click the 'Accept' button
            accept_button = driver.find_element(
                By.XPATH,
                "//button[contains(@class, 'btn-success') and text()='Accept']",
            )
            accept_button.click()
            print("Friend request accepted!")
            time.sleep(1)  # Small delay to ensure action completes

    except Exception as e:
        print("No friend request detected or error occurred:", e)
