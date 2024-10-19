from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Define a class to store the previous responses
class Reference:
    '''
    A class to store previous responses from the OpenAI API
    '''
    def __init__(self) -> None:  # Fixed constructor
        self.response = ""

reference = Reference()
model_name = "gpt-3.5-turbo"

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)

def clear_past():
    """A function to clear the previous conversation and context."""
    reference.response = ""

# Command handler to clear previous conversations
@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

# Command handler for the start command
@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Hi\nI am Tele Bot!\nCreated by Siddhanth Tiwari. How can I assist you?")

# Command handler for the help command
@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    help_command = """
    Hi there, I'm a Telegram bot created by Siddhanth Tiwari! Please follow these commands:
    /start - to start the conversation
    /clear - to clear the past conversation and context
    /help - to get this help menu
    I hope this helps. :)
    """
    await message.reply(help_command)

# Main chat handler for interacting with OpenAI's ChatGPT API
@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    print(f">>> USER: \n\t{message.text}")

    # Call the OpenAI ChatCompletion API
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "system", "content": reference.response},  # Previous conversation context
            {"role": "user", "content": message.text}  # Current user input
        ]
    )

    # Store the response and send it to the user
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=reference.response)

# Start the bot
if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)
