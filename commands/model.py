import os
import time
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Global stop flag
stop_sending = False  


def update_dataset(input_text, output_text):
    """
    Append a new record to dataset.json.
    Record format:
    {
      "input_text": "...",
      "output_text": "..."
    }
    """
    dataset_file = "dataset.json"
    try:
        if os.path.exists(dataset_file):
            with open(dataset_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
    except Exception as e:
        print("Error loading dataset.json:", e)
        data = []
    new_record = {"input_text": input_text, "output_text": output_text}
    data.append(new_record)
    try:
        with open(dataset_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Error updating dataset.json:", e)


def read_dataset_context(limit=3):
    """
    Read the last `limit` records from dataset.json and return
    them as a formatted string to be used as context.
    """
    dataset_file = "dataset.json"
    if not os.path.exists(dataset_file):
        return ""
    try:
        with open(dataset_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("Error reading dataset.json:", e)
        return ""
    # Use the most recent `limit` records
    recent = data[-limit:] if len(data) >= limit else data
    context_lines = []
    for record in recent:
        input_text = record.get("input_text", "")
        output_text = record.get("output_text", "")
        context_lines.append(f"User: {input_text}\nBot: {output_text}")
    return "\n".join(context_lines)


def groq_chat(prompt, name, driver):
    """
    Get AI answer using groq's chat completion.
    If recent dataset records exist, include them as context.
    """
    context = read_dataset_context()
    if context:
        # Prepend the recent conversation history as context.
        prompt = (
            f"Here is some recent conversation history:\n{context}\n\nUser: {prompt}"
        )
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Respond without markdown formatting. Your name is Luna Aria, Your creator is Arvelio a.k.a Ariq and your mother is Keyla sabrina (Abianca) you are a child. answer with a short and simple sentence.",
            },
            {"role": "user", "content": f"The guy name who talk to you: {name} \n The message: " + prompt},
        ],
        temperature=0.3,
        max_completion_tokens=1000,
        top_p=1,
        stream=True,
        # reasoning_format="hidden",
    )
    answer = ""
    for chunk in completion:
        answer += chunk.choices[0].delta.content or ""
    return answer


def chat_command(driver, command, argument, name):
    """
    Process AI chat commands.
    Commands:
      .chat or .c       -> trigger AI response (augmented with dataset context)
      .chatstop or .cstop -> stop sending mid-response
    """
    global stop_sending
    if command in ("chatstop", "cstop"):
        stop_sending = True
        return

    if command not in ("chat", "c") or not argument:
        return

    answer_ai = groq_chat(argument, name, driver)
    if answer_ai:
        # Update dataset with the new conversation record.
        update_dataset(argument, answer_ai)

        # Toggle chat UI initially
        try:
            toggle_btn = driver.find_element(
                "css selector", 'ui-button[title="Toggle chat"] button'
            )
            toggle_btn.click()
        except Exception as e:
            print("Toggle error:", e)
        time.sleep(0.5)

        def ensure_chat_open(driver):
            """Ensure the chat textarea is visible; if not, toggle it open."""
            try:
                textarea = driver.find_element(
                    "css selector", 'textarea[aria-label="Chat message"]'
                )
                if not textarea.is_displayed():
                    toggle_btn = driver.find_element(
                        "css selector", 'ui-button[title="Toggle chat"] button'
                    )
                    toggle_btn.click()
                    time.sleep(0.5)
            except Exception as e:
                print("Ensure chat open error:", e)

        def send_message_part(text):
            ensure_chat_open(driver)
            try:
                ta = driver.find_element(
                    "css selector", 'textarea[aria-label="Chat message"]'
                )
                driver.execute_script("arguments[0].value = arguments[1];", ta, text)
                driver.execute_script(
                    "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                    ta,
                )
            except Exception as e:
                print("Type error:", e)
            try:
                send_btn = driver.find_element(
                    "css selector",
                    'ui-button[title="Send message (hold Shift to send without closing input)"] button',
                )
                send_btn.click()
            except Exception as e:
                print("Send error:", e)
            time.sleep(0.5)

        def split_message_by_chars(message, max_length=120):
            """
            Split the message into chunks of up to max_length characters,
            without breaking words.
            """
            words = message.split()
            chunks = []
            current_chunk = ""
            for word in words:
                spacer = " " if current_chunk else ""
                if len(current_chunk) + len(spacer) + len(word) > max_length:
                    chunks.append(current_chunk.strip())
                    current_chunk = word
                else:
                    current_chunk += spacer + word
            if current_chunk:
                chunks.append(current_chunk.strip())
            return chunks

        # Split the AI answer into parts of up to 120 characters each.
        message_parts = split_message_by_chars(answer_ai, 120)
        for part in message_parts:
            if stop_sending:
                # Reset flag for future calls
                stop_sending = False  
                break
            send_message_part(part)
            time.sleep(4)
