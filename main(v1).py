import os

import sqlite3

import json

import asyncio

from datetime import datetime

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F

from aiogram.types import Message

from aiogram.filters import Command



# Import the modern Google GenAI library

from google import genai

from google.genai import types



load_dotenv()



# 1. INITIALIZE APIS & CORE DATABASE

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))

dp = Dispatcher()



# Modern client initialization pattern

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



conn = sqlite3.connect("diet_bot.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, daily_target INTEGER DEFAULT 1500)")

cursor.execute("CREATE TABLE IF NOT EXISTS logs (user_id INTEGER, log_date TEXT, food_item TEXT, calories INTEGER)")

conn.commit()



SYSTEM_PROMPT = """

You are an expert nutritionist bot. Analyze the user's food input (which could be text, an image, or a voice transcription). 

Estimate the meal content and return a strict, valid JSON object containing exactly two keys: "food" and "calories".

Do not include markdown formatting, backticks, or extra commentary. 

Example Output: {"food": "2 scrambled eggs with whole wheat toast", "calories": 320}

"""



# 2. HELPER TO CORE PROCESSOR (THE CALORIE ENGINE)

async def process_user_intake(user_id: int, content_payload) -> str:

    # Query current user metrics

    cursor.execute("SELECT daily_target FROM users WHERE user_id = ?", (user_id,))

    row = cursor.fetchone()

    target = row[0] if row else 1500

    

    try:

        # Modern stateless generation call with system instructions pass

        response = client.models.generate_content(

            model='gemini-2.5-flash',

            contents=content_payload,

            config=types.GenerateContentConfig(

                system_instruction=SYSTEM_PROMPT

            )

        )

        

        # Strip potential formatting wrappers if the model hallucinations include backticks

        clean_json = response.text.replace("```json", "").replace("```", "").strip()

        data = json.loads(clean_json)

        food, calories = data["food"], int(data["calories"])

    except Exception as e:

        print(f"Parsing error details: {e}")

        return "❌ Couldn't clearly parse that meal. Please try describing it clearly."



    # Commit to DB

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (user_id, today, food, calories))

    conn.commit()



    # Calculate Remaining Target

    cursor.execute("SELECT SUM(calories) FROM logs WHERE user_id = ? AND log_date = ?", (user_id, today))

    total_consumed = cursor.fetchone()[0] or 0

    remaining = max(0, target - total_consumed)



    return f"🍽️ **Logged:** {food}\n🔥 **Calories:** {calories} kcal\n\n📊 **Today's Status:**\nTarget: {target} kcal\nConsumed: {total_consumed} kcal\nRemaining: {remaining} kcal"



# 3. TELEGRAM CHAT HANDLERS

@dp.message(Command("start"))

async def start_cmd(message: Message):

    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (message.from_user.id,))

    conn.commit()

    await message.answer("👋 Welcome to your Personal Dietitian Bot!\nYour default target is set to **1500 calories**.\n\nYou can log food anytime by:\n• Sending text (e.g., 'I ate an apple')\n• Snapping a photo of your plate\n• Sending a voice note!")



@dp.message(F.text)

async def handle_text(message: Message):

    status_msg = await message.answer("🔄 Analyzing text log...")

    result = await process_user_intake(message.from_user.id, message.text)

    await status_msg.edit_text(result, parse_mode="Markdown")



@dp.message(F.photo)

async def handle_photo(message: Message):

    status_msg = await message.answer("🔄 Processing plate image...")

    await bot.download(message.photo[-1], destination="temp.jpg")

    

    # Correct structure for passing inline image data bytes in the new SDK

    image_payload = types.Part.from_bytes(

        data=open("temp.jpg", "rb").read(),

        mime_type="image/jpeg"

    )

    result = await process_user_intake(message.from_user.id, image_payload)

    await status_msg.edit_text(result, parse_mode="Markdown")

    os.remove("temp.jpg")



@dp.message(F.voice)

async def handle_voice(message: Message):

    status_msg = await message.answer("🔄 Listening to voice log...")

    await bot.download(message.voice, destination="temp.ogg")

    

    # Correct structure for passing inline audio data bytes in the new SDK

    voice_payload = types.Part.from_bytes(

        data=open("temp.ogg", "rb").read(),

        mime_type="audio/ogg"

    )

    result = await process_user_intake(message.from_user.id, voice_payload)

    await status_msg.edit_text(result, parse_mode="Markdown")

    os.remove("temp.ogg")



if __name__ == "__main__":

    print("🤖 Bot is starting up safely with the modern GenAI SDK...")

    asyncio.run(dp.start_polling(bot)) 

