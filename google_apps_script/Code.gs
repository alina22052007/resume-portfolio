/**
 * ==============================================================================
 * Google Apps Script for AI-Powered Portfolio Database & Resume Generator
 * Author: Computer Science Portfolio Management System
 * ==============================================================================
 * Instructions:
 * 1. Open Google Sheets (sheets.new)
 * 2. Click Extensions > Apps Script
 * 3. Replace all code in Code.gs with this script
 * 4. Click 'Save' and then click 'Deploy > New deployment'
 * 5. Select type: 'Web App', Execute as: 'Me', Who has access: 'Anyone'
 * 6. Copy the Web App URL and paste it into the Portfolio Web UI under 'Google Sheets Sync'
 * ==============================================================================
 */

// Global configuration
var BACKEND_URL = "http://localhost:5050/api/sheets/webhook"; // Update with your deployed backend tunnel if needed

/**
 * Creates custom menu when Google Sheet is opened
 */
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('⚡ Portfolio System')
    .addItem('📥 Fetch & Populate All Tabs from App', 'fetchAndPopulateFromApp')
    .addItem('📤 Push Current Sheet Changes to App', 'pushSheetChangesToApp')
    .addSeparator()
    .addItem('🛠️ Format & Color All Tabs', 'formatAllTabs')
    .addToUi();
}

/**
 * Handles incoming HTTP POST requests from the Portfolio Application
 */
function doPost(e) {
  try {
    var rawData = e.postData.contents;
    var data = JSON.parse(rawData);
    
    if (data.sheets) {
      populateSheets(data.sheets);
      return ContentService.createTextOutput(JSON.stringify({
        status: "success",
        message: "Google Sheets successfully populated with portfolio records",
        updated_at: new Date().toISOString()
      })).setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: "Invalid payload format: missing 'sheets' key"
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      error: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Handles incoming HTTP GET requests for testing endpoint connectivity
 */
function doGet(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var result = {
    status: "active",
    sheet_name: ss.getName(),
    tabs_count: ss.getSheets().length,
    timestamp: new Date().toISOString()
  };
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Iterates through portfolio categories, creates separate tabs, and populates data
 */
function populateSheets(sheetsData) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var colorPalette = {
    "Personal_Info": "#1E3A8A", // Indigo
    "Education": "#047857",     // Emerald
    "Skills": "#B45309",        // Amber
    "Certifications": "#6D28D9",// Purple
    "Projects": "#0369A1",      // Sky
    "Experience": "#0F766E",    // Teal
    "Achievements": "#C2410C",  // Orange
    "Publications": "#4338CA",  // Blue
    "Languages": "#4B5563"      // Gray
  };

  for (var sheetName in sheetsData) {
    if (!sheetsData.hasOwnProperty(sheetName)) continue;
    
    var categoryData = sheetsData[sheetName];
    var sheet = ss.getSheetByName(sheetName);
    
    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
    }
    
    sheet.clear();
    
    var headers = categoryData.headers;
    var rows = categoryData.rows;
    var allData = [headers];
    
    if (rows && rows.length > 0) {
      for (var i = 0; i < rows.length; i++) {
        allData.push(rows[i]);
      }
    }
    
    // Write data to sheet
    var range = sheet.getRange(1, 1, allData.length, headers.length);
    range.setValues(allData);
    
    // Style Header Row
    var headerRange = sheet.getRange(1, 1, 1, headers.length);
    var headerColor = colorPalette[sheetName] || "#2563EB";
    headerRange.setBackground(headerColor);
    headerRange.setFontColor("#FFFFFF");
    headerRange.setFontWeight("bold");
    headerRange.setFontFamily("Arial");
    headerRange.setHorizontalAlignment("center");
    
    // Style Data Rows
    if (rows.length > 0) {
      var dataRange = sheet.getRange(2, 1, rows.length, headers.length);
      dataRange.setFontFamily("Arial");
      dataRange.setVerticalAlignment("middle");
      sheet.setRowHeights(2, rows.length, 28);
    }
    
    // Auto resize column widths
    for (var c = 1; c <= headers.length; c++) {
      sheet.autoResizeColumn(c);
    }
    
    sheet.setFrozenRows(1);
  }
}

/**
 * Manual fetch action triggered from Sheet menu
 */
function fetchAndPopulateFromApp() {
  var ui = SpreadsheetApp.getUi();
  var promptResult = ui.prompt(
    'Sync from Portfolio Application',
    'Enter your Portfolio Application URL (e.g., http://localhost:5050 or ngrok/hosted URL):',
    ui.ButtonSet.OK_CANCEL
  );

  if (promptResult.getSelectedButton() !== ui.Button.OK) return;
  var baseUrl = promptResult.getResponseText().trim().replace(/\/$/, "");
  
  try {
    var response = UrlFetchApp.fetch(baseUrl + "/api/export/sheets-json");
    var data = JSON.parse(response.getContentText());
    if (data.sheets) {
      populateSheets(data.sheets);
      ui.alert('Success', 'Successfully synced ' + data.total_records + ' portfolio records into Google Sheets!', ui.ButtonSet.OK);
    } else {
      ui.alert('Error', 'Invalid response received from Portfolio App.', ui.ButtonSet.OK);
    }
  } catch (err) {
    ui.alert('Sync Failed', 'Could not connect to app: ' + err.toString(), ui.ButtonSet.OK);
  }
}

/**
 * Format and apply styling to all existing tabs
 */
function formatAllTabs() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = ss.getSheets();
  for (var i = 0; i < sheets.length; i++) {
    var sheet = sheets[i];
    if (sheet.getLastRow() > 0 && sheet.getLastColumn() > 0) {
      var header = sheet.getRange(1, 1, 1, sheet.getLastColumn());
      header.setBackground("#1E40AF").setFontColor("#FFFFFF").setFontWeight("bold");
      sheet.setFrozenRows(1);
    }
  }
  SpreadsheetApp.getUi().alert("All tabs styled with professional layout!");
}

