import openai
import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Set up the OpenAI API key
openai.api_key = "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"

# Set up the Telegram bot
bot = telegram.Bot(token="6221139469:AAEV4B0QbYJO8go5bxtCzwocTJp2u4bI35o")
updater = Updater(bot=bot, use_context=True)

# Define a global variable to store the current state of the conversation
# This includes the context and any previously generated response
conversation_state = {}


# Define the /start command handler
def start_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot. Send me a message and I'll "
                                                                    "generate a response.")


# Define the message handler
def message_handler(update, context):
    global conversation_state

    # Get the user's message
    message = update.message.text

    # Add the user's message to the conversation context
    if "context" not in conversation_state:
        conversation_state["context"] = message
    else:
        conversation_state["context"] += "\n" + message

    # Generate a response from OpenAI using the conversation context
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=conversation_state["context"],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Update the conversation context with the new response
    conversation_state["context"] += "\n" + response.choices[0].text

    # Send the response to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=response.choices[0].text)


# Add the command and message handlers to the updater
updater.dispatcher.add_handler(CommandHandler("start", start_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

# Start the bot
updater.start_polling()
updater.idle()
