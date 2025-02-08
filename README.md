# LunaAria Bot - Character AI for Pony Town

Luna Aria Bot for Pony Town is an interactive, AI-powered chatbot designed to enhance your Pony Town experience. Leveraging advanced natural language processing via Groq’s chat completions, Luna Aria Bot offers friendly, engaging, and context-aware conversations with players.

## ✨Features

- **Contextual Understanding**: Maintains context across conversations, making interactions feel more natural and engaging.

- **Engaging Dialogue**: Provides a wide range of responses, from humorous to informative, to keep conversations interesting.

- **Customizable**: Easily adaptable to different scenarios and user preferences.

- **Efficient**: Designed to handle multiple users simultaneously, ensuring a smooth experience for all players.

- **Anti AFK**: Prevents the bot from being AFK, ensuring it remains active and responsive.

- **Auto Accept Friend request**: Automatically accepts friend requests from players.

- **Auto Delete Friend**: Automatically delete friend requests from players.

- **Auto change local to Personal chat log**: Automatically change local to Personal chat log.

## 💻 Command Available
- **.chat `<prompt>`**: _Start a conversation with Luna Aria Bot._

- **.say `<prompt>`**: _Make the bot say anything in the prompt._

## Authority Commands
- **.delete `<days>`**: _delete lots of player from the friend list._

## 🛠 How It Works

- **User Interaction**: _Players interact with Luna Aria Bot through text commands in the Pony Town chat._

- **API Request**: _The bot sends the user's message to Groq's chat completions API._

- **Response Generation**: _Groq processes the input and generates a relevant response._

- **Response Delivery**: _The bot sends the generated response back to the user in the Pony Town chat._

## 🚀 Getting Started

Installation
To set up LunaBot on your device, follow the steps below:

1️⃣ Create a Virtual Environment
For Windows

```Bash
py -m venv .venv
source .venv\Scripts\activate
```

For macOS/Linux

```Bash
python3 -m venv .venv
source .venv/bin/activate
```

2️⃣ Install Dependencies

```Bash
pip install -r requirements.txt
```

3️⃣ Set Up Environment Variables
Create a .env file in the project directory and add:

```Ini
CF_CLEARANCE=your_cloudflare_clearance_token_here
SESSION_ID=you_session_token_in_cookies_browser
GROQ_API_KEY=your_api_key_here
```

4️⃣ **Run the Bot**

Option 1: Using Python3

```Bash
python3 main.py
```

Option 2: Using Py Command (Windows)

```Bash
py main.py
```

or

```Bash
py app.py
```

## 🛠️ How to get API KEY

To obtain an API key for SwertaBot, follow these steps:

GroqCLoud:

1. Visit the [Groq API Cloud website](https://console.groq.com/playground).
2. Sign up or log in to your account.
3. Navigate to the API section and create a new API key.