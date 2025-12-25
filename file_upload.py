from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "8563591187:AAGvwM4blmAW0PaGIFzo0pM2QtEsrFQOTQY"

files = []  # simple storage

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📂 Show Files", callback_data="show_files")]
    ]

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "📎 Send a file to save it.\n"
        "📂 Tap *Show Files* to view saved files.\n\n"
        "❌ Text messages are not allowed.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Handle file upload
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    files.append({
        "name": file.file_name,
        "id": file.file_id
    })

    await update.message.reply_text("✅ File saved successfully")

# Reject text
async def reject_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Please send a file only.")

# Buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_files":
        if not files:
            await query.edit_message_text("📭 No files available.")
            return

        keyboard = [
            [InlineKeyboardButton(f["name"], callback_data=f"file_{i}")]
            for i, f in enumerate(files)
        ]

        await query.edit_message_text(
            "📁 Saved files:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("file_"):
        index = int(query.data.split("_")[1])
        await query.message.reply_document(files[index]["id"])

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reject_text))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
