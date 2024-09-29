from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta

# Your bot token
TOKEN = '7522198105:AAHv3Epb3A3raW1oOD0e67QVXKZxXBf8bq4'

# Dictionary to store when a user last received a key
user_last_access = {}

# Predefined keys
keys = {
    0: "X1b2N3k4L5m6V7j8",
    1: "T9g8J7h6B5n4M3r2",
    2: "A3f4S5d6G7h8J9k0",
    3: "U7y6T5r4E3w2Q1a0",
    4: "Q2w3E4r5T6y7U8i9",
    5: "Z1x2C3v4B5n6M7p8",
    6: "L3k4J5h6G7f8D9s0",
    7: "H7j8K9l0Z1x2C3v4",
    8: "P5o4I3u2Y1t0R9e8",
    9: "N0m9B8v7C6x5Z4l3",
    10: "V3b2N1m0L9k8J7h6",
    11: "F9d8S7a6W5q4R3t2",
    12: "D2f3G4h5J6k7L8m9",
    13: "C7v8B9n0M1o2P3i4",
    14: "E6r5T4y3U2i1O0p9",
    15: "G5h6J7k8L9m0N1o2",
    16: "M9n8B7v6C5x4Z3a2",
    17: "I3u2Y1t0R9e8W7q6",
    18: "K1l2J3h4G5f6D7s8",
    19: "O9p8I7u6Y5t4R3e2",
    20: "S0a1D2f3G4h5J6k7"
}

# Start command with warning message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Warning message in both English and Hindi
    warning_message = """
    ⚠️ *Important Notice* ⚠️
    
    Note: Create a new GoaGame account by clicking on the 'Register' button. If you use this mod in your old account, then the mod will not work.
    
    *'Register'* बटन पर क्लिक करके एक नया account बनाएं, यदि आप इस मॉड का उपयोग अपने पुराने account में करते हैं, तो मॉड काम नहीं करेगा।
    """

    keyboard = [
        [InlineKeyboardButton("Register", url='https://tinyurl.com/48vr69at')],
        [InlineKeyboardButton("Join Channel", url='https://t.me/Goa_Gamee_Link')],
        [InlineKeyboardButton("Confirm Channel Join", callback_data='confirm_join')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        warning_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Function to confirm channel join
async def confirm_channel_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Thanking the user for joining the channel
    await query.message.reply_text(
        "Thank you for confirming your channel join! You can now proceed to get your access key."
    )

    # Adding the option to get the key
    keyboard = [
        [InlineKeyboardButton("Get Key", callback_data='get_key')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Replying with the new options
    await query.message.reply_text(
        "Click the button below to get your access key.",
        reply_markup=reply_markup
    )

# Function to handle key request
async def get_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Check if the user is allowed to get another key (24-hour rule)
    user_id = query.from_user.id
    now = datetime.now()

    if user_id in user_last_access:
        last_access_time = user_last_access[user_id]
        if now - last_access_time < timedelta(hours=24):
            remaining_time = timedelta(hours=24) - (now - last_access_time)
            hours, minutes = divmod(remaining_time.seconds, 3600)
            minutes //= 60
            await query.message.reply_text(
                f"You can only get a new key every 24 hours. Please wait for {hours} hours and {minutes} minutes before trying again."
            )
            return
    
    # Ask the user for the access number (0-20)
    await query.message.reply_text(
        "Please enter your access number :"
    )
    context.user_data['awaiting_access_number'] = True  # Set flag to await number input

# Function to handle the access number entered by the user
async def handle_access_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    if context.user_data.get('awaiting_access_number', False):
        try:
            access_number = int(update.message.text)
            if 0 <= access_number <= 20:
                key = keys[access_number]
                await update.message.reply_text(f"Your access key: {key}")
                
                # Store the time when the user received the key
                user_last_access[user_id] = datetime.now()

                # Clear the awaiting flag
                context.user_data['awaiting_access_number'] = False
            else:
                await update.message.reply_text("Please enter a valid number between 0 and 20.")
        except ValueError:
            await update.message.reply_text("Please enter a valid number between 0 and 20.")
    else:
        await update.message.reply_text("You have already received your key. You can request a new key after 24 hours.")

# Main function
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(confirm_channel_join, pattern='confirm_join'))
    application.add_handler(CallbackQueryHandler(get_key, pattern='get_key'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_access_number))

    application.run_polling()

if __name__ == '__main__':
    main()
