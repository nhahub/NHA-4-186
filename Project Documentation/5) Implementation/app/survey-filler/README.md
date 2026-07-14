# Menofia Survey Auto-Filler Extension

This Chrome extension automates the tedious process of filling out surveys on the Menofia Education Portal. It injects a floating control panel directly onto the survey page, allowing you to instantly auto-fill all survey questions across all tabs for a subject, with built-in randomization and automatic popup handling.

## Features
- **Auto-Fill All Tabs**: Automatically iterates through every tab of the selected subject, fills the radio buttons, saves, and handles confirmation popups.
- **Smart Skip**: Instantly detects if a tab has already been filled and skips it to save time.
- **Aggressive Speed**: Scans for the "Saved" popups and dismisses them within milliseconds of appearing, cutting down wait times.
- **Realistic Randomization**: Mixes answers between 60%, 80%, and 100% agreement to simulate realistic human responses.
- **Zero Login Friction**: Runs directly in your browser as a content script, meaning it uses your existing session and you don't need to pass passwords to an external script.

## Installation Instructions

1. **Download or Clone the Repository**
   If you haven't already, clone this repository to your local machine:
   ```bash
   git clone https://github.com/FreyGold/survey-filler.git
   ```

2. **Open Chrome Extensions Page**
   Open Google Chrome and navigate to the Extensions page by typing this URL in your address bar:
   `chrome://extensions/`

3. **Enable Developer Mode**
   In the top right corner of the Extensions page, turn on the **Developer mode** toggle switch.

4. **Load the Extension**
   Click the **Load unpacked** button that appears in the top left corner.
   Select the folder containing this extension (`survey-filler`).

5. **Use the Extension**
   - Navigate to the Menofia Education Portal survey page.
   - Select your subject from the dropdown menu ("اختر الماده").
   - Click the purple **Auto-Fill All Tabs (Mix 60-100%)** button from the floating widget in the bottom right corner.
   - Wait for it to blast through the tabs.
   - Select your next subject and repeat!

## Notice
Use this script responsibly. It is designed to save time on repetitive forms.
