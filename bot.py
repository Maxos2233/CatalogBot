from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from config import TOKEN
import catalog

NAME, ARTICLE, QUANTITY = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["/add"],
        ["/search", "/show"],
        ["/edit", "/delete"],
        ["/help"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Я бот склада\n"
        "Для вызова всех доступных команд нажмите на кнопку ниже, либо введите /help",
        reply_markup=reply_markup
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/add - Добавить новую позицию\n"
        "/delete - Удалить позицию полностью\n"
        "/show - Показать весь каталог\n"
        "/search - поиск товара по артиклю"
        "/edit - редактировать остатки товара\n"
        "/cancel - отменить действие"
    )

async def add_start(update, context):
    await update.message.reply_text("Введите название товара:")
    return NAME

async def get_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Введите артикул")
    return ARTICLE

async def get_article(update, context):
    context.user_data["article"] = update.message.text
    product = catalog.product_exists(context.user_data["article"])
    if product:
        await update.message.reply_text("Товар с таким артиклем уже существует")
        return ConversationHandler.END
    await update.message.reply_text("Введите количество")
    return QUANTITY

async def end_add(update, context):
    context.user_data["quantity"] = update.message.text
    await update.message.reply_text(catalog.add_product(context.user_data["name"], context.user_data["article"], context.user_data["quantity"]))
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Отмена")
    return ConversationHandler.END

async def show_all(update, context):
    await update.message.reply_text(catalog.show_product())

async def delete_start(update, context):
    await update.message.reply_text("Введите артикул для удаления")
    return ARTICLE

async def delete_end(update, context):
    context.user_data["article"] = update.message.text
    product = catalog.product_exists(context.user_data["article"])
    if product is None:
        await update.message.reply_text("Такого товара не существует")
        return ConversationHandler.END
    await update.message.reply_text(catalog.delete_product(context.user_data["article"]))
    return ConversationHandler.END

async def edit_start(update, context):
    await update.message.reply_text("Введите артикул для изменения количества товара")
    return ARTICLE

async def edit_article(update, context):
    context.user_data["article"] = update.message.text
    product = catalog.product_exists(context.user_data["article"])
    if product is None:
        await update.message.reply_text("Такого товара не существует")
        return ConversationHandler.END
    await update.message.reply_text("Введите новое количество товара")
    return QUANTITY

async def edit_end(update, context):
    context.user_data["quantity"] = update.message.text
    await update.message.reply_text(catalog.edit_product(context.user_data["article"], context.user_data["quantity"]))
    return ConversationHandler.END

async def search_start(update, context):
    await update.message.reply_text("Введите артикул товара")
    await update.message.reply_text("Пизда")
    return ARTICLE

async def search_end(update, context):
    context.user_data["article"] = update.message.text
    await update.message.reply_text(f"Найденые товары: {catalog.search_product(context.user_data["article"])}")
    return ConversationHandler.END

add_position = ConversationHandler(
    entry_points=[CommandHandler("add", add_start)],
    states={
        NAME:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        ARTICLE:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_article)],
        QUANTITY:    [MessageHandler(filters.TEXT & ~filters.COMMAND, end_add)],
    },
    fallbacks = [CommandHandler("cancel", cancel)]
)

delete_position = ConversationHandler(
    entry_points=[CommandHandler("delete", delete_start)],
    states={
        ARTICLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_end)],
    },
    fallbacks = [CommandHandler("cancel", cancel)]
)

edit_position = ConversationHandler(
    entry_points=[CommandHandler("edit", edit_start)],
    states={
        ARTICLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_article)],
        QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_end)],
    },
    fallbacks = [CommandHandler("cancel", cancel)]
)

search_position = ConversationHandler(
    entry_points=[CommandHandler("search", search_start)],
    states={
        ARTICLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_end)],
    },
    fallbacks = [CommandHandler("cancel", cancel)]
)

app = Application.builder().token(TOKEN).build()
app.add_handler(add_position)
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", info))
app.add_handler(CommandHandler("show", show_all))
app.add_handler(delete_position)
app.add_handler(edit_position)
app.add_handler(search_position)

app.run_polling()