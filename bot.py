import logging
import os

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder,Updater, CommandHandler, MessageHandler, filters, InlineQueryHandler


def start(update, context):
    update.effective_message.reply_text(
        """Open a Whatsapp chat without saving the contact.

Send a mesage to the bot with the phone number in international format.

Examples:
+39 1234567890
+1 (555) 555-1234

Note: phone numbers are never saved 😇

Credits: @rignaneseleo ✌🏻"""
    )

# Handle all other messages


def reply(update, context):
    message = update.effective_message
    if message.text.startswith("+"):
        number = message.text
        number = number.replace("+", "")
        number = number.replace(" ", "")
        number = number.replace("-", "")
        number = number.replace("(", "")
        number = number.replace(")", "")
        number = number.replace(".", "")
        number = number.replace(",", "")
        update.effective_message.reply_text(
            f"This is the link to open the chat directly:\r\n\r\n📲 https://wa.me/{number}", disable_web_page_preview=True, reply_to_message_id=update.effective_message.message_id,
        )
    else:
        update.effective_message.reply_text("""⚠️ The phone number should start with +
    
Examples:
+39 1234567890
+1 (555) 555-1234
+441234567890""")


if __name__ == "__main__":
    # heroku app name
    NAME = "fast-wa-chat"
    # get TOKEN from Heroku Config Vars
    TOKEN = os.environ['TOKEN']

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    application = ApplicationBuilder().token(TOKEN).build()
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # Start the webhook
    application.run_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=f"https://{NAME}.herokuapp.com/{TOKEN}")
    application.idle()
