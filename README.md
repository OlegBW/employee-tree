# Employee Hierarchy Management System

This Django project implements a system for managing employees in a hierarchical structure, where each employee can have a manager and can be responsible for other subordinates. The project provides an API for managing employees and their hierarchical relationships, as well as a user interface for viewing and managing this data.

## Features

- **Employee Management:** Add, update, and delete employees in the system.
- **Hierarchical Structure:** Manage the hierarchy of employees, where each employee can have a manager and can manage other employees.
- **API:** RESTful API for interacting with the employee data and hierarchy.
- **Client-Side Rendering:** Hierarchical tree visualization on the client-side using existing solutions.
- **Validation:** Ensures data integrity, such as preventing cycles in the hierarchy.

## Technologies

- **Backend:** Django, Django REST Framework
- **Database:** SQLite
- **Frontend:** React, Bootstrap for styling
- **Tools:** Vite for React integration, Bootstrap for navigation and UI components

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/OlegBW/employee-tree.git
   cd employee-tree

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply the migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

## Seeding data

- **You can seed the database with initial data using the following command:**

    ```bash
    python manage.py seed
    ```

- **In employees/management/commands/seed there is a variable SUBORDINATES_PER_MANAGER, the current value of 3 is defined to generate and test quickly, to generate 50k+ records, change to 5 (5^7 records)**


# UI

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Node.js** (version 12.0 or higher)
- **npm** (version 6.0 or higher) or **yarn** (version 1.22 or higher)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/OlegBW/employee-tree-client.git
   cd employee-tree-client
   ```

2. **Install the dependencies:**

   ```bash
    npm install
   ```

3. **Running the Development Server:**

   ```bash
    npm run dev
   ```