
# Elim DB – Church Member Database Manager

A Python desktop application built with Tkinter and SQLite for managing church membership records.

The application provides a graphical interface to store, search, update, and manage congregation data.
Members are categorized by age group and stored in a structured SQLite database.

---

## Features

### Member Management
- Add new member records
- Update existing member information
- Delete records from the database
- Store profile photos

### Member Classification
Members are categorized by age group based on their date of birth:

- Anak – Children
- Remaja – Teenagers
- Dewasa – Adults

Each category stores slightly different information relevant to that group.

### Search System
Users can search members by:

- Name
- JDM (small group)
- Komisi
- SOM (Team)

Search results are displayed in a table view inside the application.

---

## Technologies Used

- Python
- Tkinter (GUI framework)
- SQLite3 (local database)
- PIL / Pillow (image handling)

---

## Database Structure

The system uses a local SQLite database containing several tables.

Jemaat
- Base table storing general member information
- Name
- Date of Birth
- Gender

Anak
- Children records

Remaja
- Teen member records

Dewasa
- Adult member records

Members are first inserted into the Jemaat table and then classified into the appropriate category table.

---

## Project Structure

- database.py
- README.md

database.py contains the full implementation of the application including:

- GUI interface
- database connection logic
- CRUD operations
- search functionality
- member classification logic

---

## Database Location

The application automatically creates a local SQLite database:

Elim_data/jemaatElim.db

This file will be generated automatically if it does not already exist.

---

## How to Run

### Requirements

Install Pillow for image handling:

pip install pillow

Tkinter and SQLite are included with most Python installations.

### Run the Application

python database.py

The main menu will open with options to:

- Insert Data
- Search Records
- Edit Records
- Delete Records

---

## Example Workflow

1. Launch the application
2. Select Insert Data
3. Enter member details
4. The system determines the member's age category
5. The record is saved in the database
6. Records can later be searched or edited

---

## Concepts Demonstrated

- Python GUI development with Tkinter
- SQLite database integration
- CRUD database operations
- Data categorization logic
- Desktop application design

---

## Project Notes

This project was developed earlier in my programming journey while learning Python GUI development and database integration.

The application is implemented in a single Python file (database.py) as originally written. While the code structure could be modularized further, the project is preserved in its original form to reflect the initial implementation.

---

## Author

Jonathan Harjono
