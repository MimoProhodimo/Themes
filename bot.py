import asyncio
import logging
import json
import os
import random
import string
from pathlib import Path
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, FSInputFile
from aiogram.enums import ParseMode
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен из переменных окружения
TOKEN = "8324427955:AAHXfZoCYB7M9MUABvSah-PQrpXsOJMk9CQ"
WEB_APP_URL = "https://mimoprohodimo.github.io/Themes/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Папки
UPLOAD_FOLDER = "uploads"
THEMES_FOLDER = "themes"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(THEMES_FOLDER).mkdir(exist_ok=True)

def create_attheme_file(colors: dict) -> bytes:
    """Создает .attheme файл"""
    theme_colors = {
        "bg_color": colors.get("bg", "#1a1a1a"),
        "section_bg_color": colors.get("bg", "#1a1a1a"),
        "text_color": colors.get("text", "#ffffff"),
        "hint_color": colors.get("text", "#8e8e93"),
        "link_color": colors.get("accent", "#0088cc"),
        "accent_color": colors.get("accent", "#0088cc"),
        "button_color": colors.get("accent", "#0088cc"),
        "button_text_color": colors.get("text", "#ffffff"),
        "header_bg_color": colors.get("bg", "#1a1a1a"),
        "header_title_text_color": colors.get("text", "#ffffff"),
        "header_subtitle_text_color": colors.get("text", "#8e8e93"),
        "header_accent_text_color": colors.get("accent", "#0088cc"),
        "destructive_text_color": "#ff3b30",
        "section_header_text_color": colors.get("accent", "#0088cc"),
        "section_text_color": colors.get("text", "#ffffff"),
        "section_icon_color": colors.get("accent", "#0088cc"),
        "check_color": colors.get("accent", "#0088cc"),
        "separator_color": "#3a3a3c",
    }
    
    file_data = bytearray()
    for key, value in theme_colors.items():
        hex_value = value.lstrip('#')
        file_data.extend(key.encode('utf-8'))
        file_data.append(0)
        file_data.extend(hex_value.encode('utf-8'))
        file_data.append(0)
    
    return bytes(file_data)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Старт бота"""
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎨 Создать тему", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    
    await message.answer(
        "✨ *Конструктор тем для Telegram*\n\n"
        "🎯 Нажми кнопку ниже, чтобы создать тему:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )

@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    """Получаем данные из Mini App"""
    try:
        data = json.loads(message.web_app_data.data)
        logger.info(f"📦 Данные: {data}")
        
        if data.get('action') == 'apply_theme':
            theme = data.get('theme', {})
            
            colors = {
                "bg": theme.get('dominant', '#1a1a1a'),
                "text": theme.get('text', '#ffffff'),
                "accent": theme.get('accent', '#0088cc'),
                "is_dark": theme.get('is_dark', True)
            }
            
            # Создаём файл
            timestamp = int(datetime.now().timestamp())
            theme_path = os.path.join(THEMES_FOLDER, f"theme_{message.from_user.id}_{timestamp}.attheme")
            
            theme_data = create_attheme_file(colors)
            
            with open(theme_path, 'wb') as f:
                f.write(theme_data)
            
            # Случайное имя файла
            random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            filename = f"{random_name}_@Aboba_Bubovich_Bot.attheme"
            
            theme_file = FSInputFile(theme_path, filename=filename)
            
            await message.answer_document(
                document=theme_file,
                caption=f"🎨 *Тема готова!*\n\n"
                        f"🌄 Фон: `{colors['bg']}`\n"
                        f"✨ Акцент: `{colors['accent']}`\n"
                        f"📝 Текст: `{colors['text']}`\n"
                        f"{'🌙 Темная' if colors['is_dark'] else '☀️ Светлая'}\n\n"
                        f"📥 Скачай и открой в Telegram",
                parse_mode=ParseMode.MARKDOWN
            )
            
            os.remove(theme_path)
            
    except Exception as e:
        logger.error(f"WebApp error: {e}")
        await message.answer("❌ Ошибка при создании темы")

# Webhook handlers
async def on_startup(app): 
    webhook_url = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
    if webhook_url:
        webhook_url = f"https://{webhook_url}/webhook"
        await bot.set_webhook(webhook_url)
        print(f"✅ Webhook: {webhook_url}")

async def on_shutdown(app):
    await bot.delete_webhook()
    logger.info("Webhook deleted")

def main():
    app = web.Application()
    
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    ).register(app, path="/webhook")
    
    setup_application(app, dp, bot=bot)
    
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting server on port {port}")
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()