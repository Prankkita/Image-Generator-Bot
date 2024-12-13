import base64
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Set up the folder to save images
output_folder = "data/images"
os.makedirs(output_folder, exist_ok=True)

# Stability AI API parameters
engine_id = "stable-diffusion-v1-6"  # Example engine ID, update it if necessary
api_host = os.getenv('API_HOST', 'https://api.stability.ai')  # The API host
api_key = os.getenv("STABILITY_API_KEY")  # The API key from environment variables

# Ensure the API key is present
if api_key is None:
    raise Exception("Missing Stability API key.")

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
        else:
            print("No image data found.")
    except Exception as e:
        print(f"Error while saving the image: {e}")

# Main function
if __name__ == "__main__":
    prompt = input("Enter the prompt for image generation: ")  # User input for the image prompt

    print("Generating image...")
    image_data = generate_image(prompt, api_key)

    if image_data:
        save_image(image_data, output_folder, prompt)
    else:
        print("Image generation failed.")
