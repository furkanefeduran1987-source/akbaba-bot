import requests
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Senin görsellerinden aldığım güncel bilgiler
TRLINK_API_KEY = "510ed1f00db22c48ddbf17cd2b7d3fa293f24d9c"
BOT_TOKEN = "8569206431:AAGSdcL1mDAHpkd-8ANSfTr-D6xVlhXKfBQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("🚀 Akbaba Bot Render üzerinde 7/24 Aktif! Link gönder kanka.")

@dp.message(F.text.startswith("http"))
async def link_handler(message: types.Message):
    uzun_link = message.text
    # Render'da proxy gerekmez, direkt bağlanıyoruz
    api_url = f"https://tr.link/api?api={TRLINK_API_KEY}&url={uzun_link}"
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        if data.get("status") == "success":
            await message.answer(f"✅ **Linkin Hazır:**\n{data['shortenedUrl']}")
        else:
            await message.answer("❌ TR.Link API Hatası verdi.")
    except:
        await message.answer("⚠️ Link kısaltılırken bir sorun oluştu.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
