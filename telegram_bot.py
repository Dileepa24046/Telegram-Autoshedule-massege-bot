from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# Replace with your bot token
BOT_TOKEN = "8189066007:AAHzQaRhMCB-FS_7p13gznpzgeVSVBnE_8g"

# Create a scheduler instance
scheduler = BackgroundScheduler()

# Function to send scheduled messages
async def send_scheduled_message(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    message = context.job.data
    await context.bot.send_message(chat_id=chat_id, text=message)

# Command handler to schedule a message
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Example: /schedule 2024-09-23 16:30 This is a scheduled message
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("Usage: /schedule YYYY-MM-DD HH:MM Your message here")
            return

        # Extract date, time, and message from the arguments
        date = args[0]
        time = args[1]
        message = ' '.join(args[2:])

        # Parse the date and time
        scheduled_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        # Schedule the message
        job = scheduler.add_job(send_scheduled_message, 'date', run_date=scheduled_time, args=[context], data=message, chat_id=update.effective_chat.id)

        await update.message.reply_text(f"Message scheduled for {scheduled_time}:\n{message}")

    except ValueError:
        await update.message.reply_text("Invalid date or time format. Please use YYYY-MM-DD HH:MM format.")

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! You can schedule messages using the /schedule command.")

# Main function to run the bot
def main():
    # Start the scheduler
    scheduler.start()

    # Create the bot application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schedule", schedule))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
