# 📊 Google Sheets Two-Way Integration Guide

## 1. Architectural Overview
The **PortfoliAI System** integrates bidirectionally with Google Sheets. Google Sheets acts as an accessible, collaborative spreadsheet view where users and evaluators can view, audit, and modify portfolio records across **9 dedicated colored tabs**:

1. `Personal_Info` (Indigo `#1E3A8A`)
2. `Education` (Emerald `#047857`)
3. `Skills` (Amber `#B45309`)
4. `Certifications` (Purple `#6D28D9`)
5. `Projects` (Sky `#0369A1`)
6. `Experience` (Teal `#0F766E`)
7. `Achievements` (Orange `#C2410C`)
8. `Publications` (Blue `#4338CA`)
9. `Languages` (Gray `#4B5563`)

---

## 2. Option A: Automated Google Apps Script Webhook (Recommended)

### Step 1: Create a New Google Sheet
1. Open your browser and navigate to [https://sheets.new](https://sheets.new).
2. Title the sheet: `Aarav Sharma - Portfolio Database`.

### Step 2: Open Google Apps Script
1. In Google Sheets, click on **Extensions** in the top menu.
2. Select **Apps Script**.

### Step 3: Paste the Integration Script
1. Delete any boilerplate code inside the editor.
2. Copy the entire content of [`google_apps_script/Code.gs`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/google_apps_script/Code.gs).
3. Paste it into the Apps Script editor.
4. Click the **💾 Save** icon.

### Step 4: Deploy as Web App
1. In the top right corner of the Apps Script editor, click **Deploy** > **New deployment**.
2. Click the gear icon (**Select type**) and choose **Web app**.
3. Configure the deployment settings:
   - **Description**: `Portfolio Sync Engine`
   - **Execute as**: `Me (your email)`
   - **Who has access**: `Anyone` *(crucial for local webhook communication)*
4. Click **Deploy**.
5. Copy the generated **Web App URL** (e.g., `https://script.google.com/macros/s/AKfycbx.../exec`).

### Step 5: Trigger Sync from Portfolio App
1. Open the PortfoliAI web application in your browser (`http://localhost:5050`).
2. Navigate to the **📊 Google Sheets Sync** tab.
3. Paste your Web App URL into the input field.
4. Click **🔄 Push to Google Sheets**.
5. Return to your Google Sheet — all 9 tabs will instantly populate with headers, professional color coding, auto-sized columns, and frozen header rows!

---

## 3. Option B: Spreadsheet Custom Menu Trigger
Once the Apps Script is saved:
1. Refresh your Google Sheet.
2. Notice a new custom menu in the top bar: **⚡ Portfolio System**.
3. Click **⚡ Portfolio System** > **📥 Fetch & Populate All Tabs from App**.
4. Enter your Portfolio Application URL (`http://localhost:5050`).
5. The spreadsheet will fetch `/api/export/sheets-json` and populate all tabs automatically.

---

## 4. Option C: Direct CSV Category Downloads (Zero Setup)
If offline or without Google account access during demonstration:
1. Go to the **📊 Google Sheets Sync** tab in the PortfoliAI UI.
2. Click any of the one-click category download buttons:
   - `⬇️ Personal Info`
   - `⬇️ Education`
   - `⬇️ Skills`
   - `⬇️ Projects`
   - `⬇️ Experience`
   - `⬇️ Certifications`
   - `⬇️ Achievements`
   - `⬇️ Publications`
   - `⬇️ Languages`
3. In Google Sheets, choose **File** > **Import** > **Upload** to import any CSV directly.
4. Or import the pre-generated JSON export at [`samples/exported_portfolio_sheets.json`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/samples/exported_portfolio_sheets.json).

