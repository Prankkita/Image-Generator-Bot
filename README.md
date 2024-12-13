# Telegram Image Generation Bot

This bot uses Stability AI's image generation API to generate images from text prompts sent by users on Telegram. After the image is generated, it is sent back to the user, and all the images in the `data/images` folder are deleted.

## Features
- Accepts text prompts from users on Telegram.
- Generates an image based on the prompt using Stability AI's API.
- Sends the generated image back to the user.
- Deletes all images in the `data/images` folder after sending the image.

## Prerequisites
- Python 3.8+
- A Telegram bot API key.
- A Stability AI API key for image generation.
- Railway account for deployment.

## Requirements

- `requests`
- `python-dotenv`
- `python-telegram-bot==20`
- `base64`
- `os`

You can install these dependencies by running:
```bash
pip install requests python-dotenv python-telegram-bot==20
```

## Setting Up the Project

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/telegram-image-generation-bot.git
   cd telegram-image-generation-bot
   ```

2. Create a `.env` file in the root directory with the following variables:

   ```
   STABILITY_API_KEY=your_stability_api_key
   TELEGRAM_API_KEY=your_telegram_bot_api_key
   ```

   - Replace `your_stability_api_key` with your Stability AI API key.
   - Replace `your_telegram_bot_api_key` with the Telegram bot API key you got when you created the bot using [@BotFather](https://core.telegram.org/bots#botfather).

## Project Structure
```
telegram-image-generation-bot/
│
├── bot.py                 # Main bot script
├── utils/
│   └── deletefiles.py     # Utility to delete images in 'data/images' folder
├── data/
│   └── images/            # Folder to save generated images temporarily
├── .env                   # Environment variables file
└── README.md              # Project documentation
```

## Running the Bot Locally

1. **Set up the environment variables**: Create a `.env` file as explained above.

2. **Run the bot**:
   ```bash
   python bot.py
   ```

3. **Interact with the bot**: Go to Telegram and search for your bot by its username. Start the bot and send a text prompt to generate the image.

The bot will send the generated image and automatically delete all images in the `data/images` folder after sending the image.

## Deployment on Railway

You can deploy this bot on Railway, a platform that provides easy deployment for Python applications.

### Steps to Deploy

1. **Create a Railway Account**: If you don’t already have one, sign up at [Railway](https://railway.app).

2. **Create a New Project**: After logging in, click on "New Project" and choose the "Deploy from GitHub" option.

3. **Connect GitHub Repository**: 
   - Authorize Railway to access your GitHub repository.
   - Select the repository where you have the code for the Telegram bot.

4. **Set up the Environment Variables**:
   - On Railway, navigate to the "Variables" section of your project.
   - Add the following environment variables:
     - `STABILITY_API_KEY`: Your Stability API key.
     - `TELEGRAM_API_KEY`: Your Telegram bot API key.

5. **Add a `Procfile`**: Create a `Procfile` in the root directory to specify how to run your app.

   Create the file `Procfile` with the following content:

   ```
   web: python bot.py
   ```

6. **Deploy the Bot**:
   - After setting the environment variables and adding the `Procfile`, Railway will automatically detect the app and start the deployment process.
   - Once the deployment is finished, the bot will be running and accessible via a URL provided by Railway.

7. **Start the Bot**: Railway will automatically start the bot for you. You can check the logs to verify that the bot is running correctly.

   To view logs, click on "Logs" in the Railway dashboard.

### Notes:
- Ensure that the Railway project is set to run indefinitely so your bot stays online.
- You can use Railway’s "Always On" feature to keep the bot running 24/7.

## Contributing

Feel free to fork the repository, contribute to the code, or report any issues. Pull requests are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Summary of Steps to Deploy on Railway:
1. **Sign up** on [Railway](https://railway.app).
2. **Create a new project** and **link it to GitHub**.
3. **Add environment variables** for the Stability API and Telegram bot API keys.
4. **Create a `Procfile`** with the content `web: python bot.py`.
5. **Deploy** the app and keep the bot running.