
# D-blog: A blog created with flask

#### *By: James R. Brown*

## Description

> Simple blog created using flask.

## Dependencies

> python 3.12
> alother dependencies can be installed using `requirements.txt`

## Issues

> Only just begun...

## Fixes

> More to come...

## Versions

> 1.0

## Instructions

1. Ensure you have python 3.12 or later installed.
2. Recommend creating a virtual environment to run the app in.
    1. Command: `python3 -m venv .venv
    2. This will create a virtual environment to run the app in.
    3. Start your environment 
        - `. .venv/bin/activate` in Linux
        - `.venv\Scripts\activate.bat` in Windows CMD
        - `source .venv/bin/activate` in MacOS/Linux
3. Install required dependencies in environment.
    - `pip install -r requirements.txt`
4. Set environment variables.  You can do this through you OS terminal or Command line.  You can also set the variables to a `.env` file in project folder and not mess with your envornment.
    1. Create a file `.env` and save it to your project folder root.
    2. In this file is where you will place the environment variables.
    3. Set `FLASK_APP=flaskblog.py`
  
> [!NOTE]
> The `FLASK_APP` is the only variable that needs to be added to the `.env` file or to the OS environment for the app to work.

5. Start the app
    - `flask run`
6. After startin the first user you create will be the admin.

##### Enjoy!

> [!NOTE]
> You can also set environment variables for the...
> database: `DATABASE_URI`.
> database key: `SECRET_KEY`
