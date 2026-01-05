# Inventory Management System

A command-line based **Inventory Management System** developed in Python.  
The system allows users to manage stock items using a simple, menu layout, with storage handled via a JSON file.

---

## Features:

- Add new inventory items with full input validation  
- View all stored items in a clear format  
- Update existing items safely  
- Search items by ID or name  
- Delete individual items  
- Generate low stock reports  
- Clear all inventory items with confirmation  
- Persistent data storage using JSON  

---

## How It Works:

The program runs using a menu based loop, allowing users to select actions by entering a number (1,2,3..)  

Input validation is applied throughout to prevent invalid data and ensure can run with no issues.
---

## Data Storage:

- Inventory data is stored in `inventory.json`
- File is created automatically if it does not exist
- Empty or invalid JSON files are handled safely
- Items are sorted by numeric ID before saving

---

## User Interface

- Text-based, terminal interface:
- Screen clears between actions to prevent clutter
- Clear prompts and confirmations for user actions
- Destructive actions require confirmation

---

## Error Handling & Validation:

- Numeric validation for item IDs
- Price and quantity validation
- Prevention of duplicate item IDs
- Graceful handling of invalid input
- Protection against corrupted JSON files

---

