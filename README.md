<div align="center">
  <h1>🌾 Skyblock Farming Macro 🌾</h1>
  <p><strong>An advanced, automated background macro for Minecraft/Lunar Client with WhatsApp notifications.</strong></p>
</div>

---

## 🌟 Features

- **🎮 Background Execution:** Sends inputs directly to the Minecraft window using Win32 API. You don't need to keep the window in focus!
- **📱 WhatsApp Notifications:** Get real-time updates directly to your phone when the macro starts, stops, or completes a run using CallMeBot.
- **⚙️ Fully Customizable:** Easily adjust walking distances, lines, and loop times to fit your specific farm layout.
- **🖥️ Interactive CLI:** A clean and colorful command-line interface to easily start and stop the macro.

## 📋 Prerequisites

Make sure you have Python 3 installed. You will also need the following Python libraries:

```bash
pip install pywin32 requests python-dotenv colorama windows-toasts
```

## 🚀 Setup & Installation

1. **Download the project** to your local machine.
2. **Create a `.env` file** in the root directory of the project.
3. **Configure WhatsApp Notifications (Optional but recommended):**
   Get your API key from [CallMeBot WhatsApp API](https://www.callmebot.com/blog/free-api-whatsapp-messages/) and add the following to your `.env` file:
   ```env
   PHONE_NUMBER=+1234567890
   CALLMEBOT_API_KEY=your_api_key_here
   ```

## 🕹️ Usage

To start the macro, simply run the Python script:

```bash
python main.py
```

Once the menu appears, you can use the following commands:
- `play` - Starts the farming macro. Make sure Minecraft/Lunar is running!
- `stop` - Stops the macro safely and clears all held keys.
- `exit` - Closes the program.

## 🛠️ Configuration

You can tweak the macro settings directly inside `main.py` under the `MACRO SETTINGS` section:
- `IN_LINE_VALUE`: Time spent walking along the row.
- `WALKING_VALUE`: Time spent transitioning to the next row.
- `WALKING_BACK_VALUE`: Time spent walking back to the start.
- `LOOP_VALUE`: Total number of full farm loops to complete.
- `LINE_VALUE`: Number of rows in your farm.

## ⚠️ Disclaimer

This macro is created for educational purposes. Using macros on servers like Hypixel may violate their Terms of Service and could result in a ban. Use at your own risk!
