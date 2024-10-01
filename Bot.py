import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta

# Initialize logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global dictionary to store user data
user_data = {}

# Access keys for numbers 0 to 20
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

# Function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    # Welcome message
    await update.message.reply_text(
        f"Hello {user.first_name}, welcome to the TonnyBot!"
    )

    # Create buttons for registration, channel join, and check
    keyboard = [
        [InlineKeyboardButton("Register", url="https://tinyurl.com/48vr69at")],
        [InlineKeyboardButton("Join Channel", url="https://t.me/Goa_Gamee_Link")],
        [InlineKeyboardButton("Check Join", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Professional warning message
    warning_message = (
        "⚠️ *Important Notice:*\n\n"
        "To create a successful account, please click the *'Register'* button. "
        "Using this mod on an existing account will render the mod non-functional. "
        "Please ensure to register a new account to enjoy all features seamlessly.\n\n"
        "⚠️ *महत्वपूर्ण सूचना:*\n\n"
        "एक सफल खाता बनाने के लिए कृपया *'Register'* बटन पर क्लिक करें। "
        "इस मॉड का उपयोग एक मौजूदा खाते पर करने से मॉड कार्यशील नहीं होगा। "
        "कृपया सभी सुविधाओं का लाभ उठाने के लिए एक नया खाता पंजीकृत करें।"
    )

    # Send the warning message after the welcome message
    await update.message.reply_text(warning_message, parse_mode='Markdown')

    # Send the keyboard after the warning message
    await update.message.reply_text("Join & Register ⬇️", reply_markup=reply_markup)

# Function to handle callback queries
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "check_join":
        # Logic to check if user has joined the channel
        if user_id in user_data and user_data[user_id].get("joined", False):
            await query.answer("You have already joined the channel!")
            await query.message.reply_text("Thanks To Joining Us 😉")
            await ask_get_key_button(query, context)
        else:
            user_data[user_id] = {"joined": True}
            await query.answer("Channel join verified!")
            await query.message.reply_text("You have joined the channel! You can now proceed to get your access key.")
            await ask_get_key_button(query, context)

# Ask for the Get Key button
async def ask_get_key_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Get Key 🔐", callback_data="get_key")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the button to get your access key 🗝️", reply_markup=reply_markup)

# Function to handle Get Key request
async def get_key_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Bilingual notice message
    notice_message = (
        "ℹ️ *Important Reminder:*\n\n"
        "Before using this mode, please ensure you register using our provided link. "
        "Recharge a minimum of ₹500 or ₹1000 to enhance your chances of winning significantly. "
        "Your success is our priority!\n\n"
        "ℹ️ *महत्वपूर्ण अनुस्मारक:*\n\n"
        "इस मोड का उपयोग करने से पहले, कृपया सुनिश्चित करें कि आप हमारे दिए गए लिंक का उपयोग करके *'Register'* करें। "
        "अपनी जीतने की संभावनाओं को बढ़ाने के लिए न्यूनतम ₹500 या ₹1000 का रिचार्ज करें। "
        "आपकी सफलता हमारी प्राथमिकता है!"
    )
    await query.message.reply_text(notice_message, parse_mode='Markdown')

    # Ask for access number
    await query.message.reply_text(" Enter your access number 👇 :")

# Handle the access number entered by the user
async def handle_access_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    message_text = update.message.text

    # Check if the user is eligible for the key (not requested in the last 24 hours)
    if user_id in user_data and "last_access_time" in user_data[user_id]:
        last_access_time = user_data[user_id]["last_access_time"]
        if datetime.now() - last_access_time < timedelta(hours=24):
            remaining_time = timedelta(hours=24) - (datetime.now() - last_access_time)
            await update.message.reply_text(f" 😔 Sorry, you can only request a key once every 24 hours. "
                                            f"Please try again in {remaining_time}.")
            return

    try:
        # Convert the user's message to an integer (access number)
        access_number = int(message_text)
        if access_number in keys:
            access_key = keys[access_number]
            # Sending the access key
            await update.message.reply_text(f"{user.first_name}, Your access key 🗝️ :  {access_key}")

            # Store the time the user received the key
            user_data[user_id]["last_access_time"] = datetime.now()
        else:
            await update.message.reply_text("Invalid access number. Please enter a number between 0 and 20.")
    except ValueError:
        await update.message.reply_text("Please enter a valid number between 0 and 20.")

# Main function to start the bot application
def main():
    # Create the application and pass the bot token
    application = Application.builder().token("7522198105:AAHv3Epb3A3raW1oOD0e67QVXKZxXBf8bq4").build()

    # Add command and callback query handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="check_join"))
    application.add_handler(CallbackQueryHandler(get_key_handler, pattern="get_key"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_access_number))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
