import os
import base64  
import requests
from dotenv import load_dotenv
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from utils.deletefiles import delete_images_in_folder
# Load environment variables from .env file
load_dotenv()

# Stability AI API parameters
engine_id = "stable-diffusion-v1-6"  # Example engine ID, update if necessary
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")

# Telegram Bot API Token
telegram_api_key = os.getenv("TELEGRAM_API_KEY")

# Ensure the API key is present
if api_key is None:
    raise Exception("Missing Stability API key.")

if telegram_api_key is None:
    raise Exception("Missing Telegram API key.")

# Set up the folder to save images
output_folder = "data/images"
os.makedirs(output_folder, exist_ok=True)

# Function to generate an image using Stability AI API
def generate_image(prompt, api_key):
    url = f"{api_host}/v1/generation/{engine_id}/text-to-image"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,  # Creativity vs adherence to prompt
        "samples": 1,  # Number of images to generate
        "steps": 30,  # Number of diffusion steps
        "height": 1024,  # Image height
        "width": 1024,  # Image width
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"Response Data: {data}")  # Print the response for debugging
        if "artifacts" in data and len(data["artifacts"]) > 0:
            image_data = data["artifacts"][0]  # Assuming the first artifact
            return image_data
        else:
            print("No 'artifacts' found in the response.")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Function to save the image locally
def save_image(image_data, folder, prompt):
    try:
        image_base64 = image_data.get("base64")
        if image_base64:
            # Create a filename based on the prompt and current timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            sanitized_prompt = prompt.replace(" ", "_").replace("/", "_")
            filename = f"{sanitized_prompt}_{timestamp}.png"
            filepath = os.path.join(folder, filename)

            # Decode and save the image
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(image_base64))

            print(f"Image saved at: {filepath}")
            return filepath
        else:
            print("No image data found.")
            return None
    except Exception as e:
        print(f"Error while saving the image: {e}")
        return None

# Define the start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a prompt, and I'll generate an image for you.")

# Define the handler for receiving text messages (prompts)
async def handle_prompt(update: Update, context: CallbackContext):
    prompt = update.message.text  # Get the user's prompt from the message
    await update.message.reply_text(f"Generating image for: {prompt}...")

    # Generate the image
    image_data = generate_image(prompt, api_key)

    if image_data:
        # Save the image locally
        image_path = save_image(image_data, output_folder, prompt)

        if image_path:
            # Send the image back to the user
            with open(image_path, 'rb') as img_file:
                await update.message.reply_photo(photo=img_file)
            os.remove(image_path)  # Clean up the image file after sending it
            # Delete all images in the 'data/images' folder
            delete_images_in_folder(output_folder) 
    else:
        await update.message.reply_text("Sorry, I couldn't generate an image for that prompt.")

# Function to set up the bot
def main():
    # Create the Application instance and pass in the bot's API key
    application = Application.builder().token(telegram_api_key).build()

    # Register the command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt))

    print("Bot is running.....")
    # Start the bot
    application.run_polling()

# Run the bot
if __name__ == "__main__":
    main()
