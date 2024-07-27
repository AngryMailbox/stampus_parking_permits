# Parking Permit Generator

This project is a graphical user interface (GUI) application to generate parking permits. The application is built using `customtkinter`, `tkcalendar`, and `Pillow` for image processing, and it uses an SQLite database for storing the permits.

## Features

- Generate parking permits with user-provided details.
- View and manage existing permits.
- Automatically generate permit numbers.
- Select valid dates using a date picker.
- Includes a built-in SQLite database to store permit information.

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- The required Python packages (see below for installation instructions)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/parking-permit-generator.git
    cd parking-permit-generator
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Make sure you have `logo.png` and `permits.db` in the same directory as the `GUI.py` script.

## Usage

To run the application, execute the following command:

```sh
python GUI.py
