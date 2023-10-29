import asyncio

from aiogram import Bot, Dispatcher, executor, types
from dotenv.main import load_dotenv
import os
from PIL import Image
import pytesseract
import shutil

load_dotenv()
TOKEN = os.environ['TOKEN']
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Send photo you want to extract text from")

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    try:
        if not os.path.exists('downloads'):
            os.mkdir('downloads')
        photo = message.photo[-1]
        path = f"downloads/{photo.file_id}.jpg"
        await photo.download(path)
        image = Image.open(path)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(image)
        await message.answer(text)
        if os.path.exists(path):
            os.remove(path)
    except:
        shutil.rmtree('downloads')
        os.mkdir('downloads')

@dp.message_handler(content_types=['document'])
async def handle_photo(message: types.Message):
    await message.reply("document")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
