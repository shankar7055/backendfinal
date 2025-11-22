# How to Open index2.html in Your Browser

## Method 1: Using Terminal (Easiest) ✅

I just opened it for you! The file should now be open in your default browser.

If you need to open it again:
```bash
open /Users/shankar/PROJECT/Ai_Powered_E_COM_Hub/index2.html
```

## Method 2: Using Finder (macOS)

1. Open **Finder**
2. Press `Cmd + Shift + G` (Go to Folder)
3. Paste this path:
   ```
   /Users/shankar/PROJECT/Ai_Powered_E_COM_Hub
   ```
4. Press Enter
5. Find `index2.html` in the folder
6. Double-click it (it will open in your default browser)

## Method 3: Drag and Drop

1. Open **Finder**
2. Navigate to: `/Users/shankar/PROJECT/Ai_Powered_E_COM_Hub`
3. Find `index2.html`
4. Drag it to your browser window (Safari, Chrome, Firefox, etc.)

## Method 4: Right-Click Menu

1. In Finder, navigate to the project folder
2. Right-click on `index2.html`
3. Select **"Open With"** → Choose your browser (Safari, Chrome, etc.)

## Method 5: From Browser Directly

1. Open your browser (Safari, Chrome, Firefox, etc.)
2. Press `Cmd + O` (Open File)
3. Navigate to: `/Users/shankar/PROJECT/Ai_Powered_E_COM_Hub`
4. Select `index2.html`
5. Click "Open"

## Quick Command

If you're in the project directory:
```bash
cd /Users/shankar/PROJECT/Ai_Powered_E_COM_Hub
open index2.html
```

## What You Should See

Once opened, you'll see:
- **Dashboard** tab - Overview with statistics
- **Customers** tab - List of customers
- **Inventory** tab - Product inventory
- **Financials** tab - Financial analytics
- **AI Assistant** tab - Interactive AI chat

## Important Notes

- ✅ The backend server must be running on **http://localhost:5002**
- ✅ Make sure the server is running before using the frontend
- ✅ The frontend will connect to the backend automatically

## If It Doesn't Work

1. **Check if server is running:**
   ```bash
   curl http://localhost:5002/customers
   ```

2. **Restart the server if needed:**
   ```bash
   cd /Users/shankar/PROJECT/Ai_Powered_E_COM_Hub
   export OPENAI_API_KEY="your_key"
   python3 Backend_api1.py
   ```

3. **Check browser console for errors:**
   - Press `F12` or `Cmd+Option+I` to open DevTools
   - Check the Console tab for any errors

