# Simple Survey API

## Project Description

This is a simple survey application where the backend is built with Django and Django REST Framework. The frontend of this application is built with React (the frontend code can be found in the `simple-survey-client` repository).

## Installation Instructions

Before you start, make sure you have Python and pip installed on your machine.

1. **Clone the Repository**: Clone this repository to your local machine using `git clone https://github.com/username/simple-survey-api.git`. Replace `username` with your GitHub username.

2. **Create a Virtual Environment**: Navigate to the project directory and create a virtual environment using `python -m venv env`.

3. **Activate the Virtual Environment**: Activate the virtual environment. On Windows, use `env\Scripts\activate`. On Unix or MacOS, use `source env/bin/activate`.

4. **Install Dependencies**: Install the project dependencies using `pip install -r requirements.txt`.

## Usage Instructions

To run the Django server, use the command `python manage.py runserver`. The API will be available at `http://localhost:8000`.

## Deployment Instructions

1. **Push Your Changes**: Make sure all your changes are committed and pushed to your GitHub repository.

2. **Create a Vercel Account**: If you haven't already, create a Vercel account and install the Vercel CLI[^1^][4].

3. **Import Your Project**: Import your project into Vercel using the `vercel` command in your terminal[^1^][4]. Vercel will automatically detect that you're using Django[^2^][1].

4. **Deploy**: Vercel will build and deploy your Django application, providing you with a deployment URL upon completion[^1^][4].

5. **Check Your Application**: Visit the deployment URL to ensure your Django application runs correctly on Vercel[^1^][4].


## Contribution Guidelines

Contributions are open! If you have any ideas or suggestions, feel free to make a pull request or open an issue.

