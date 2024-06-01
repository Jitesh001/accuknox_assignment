Here's the formatted content for your README file on GitHub:

---

# Project Setup Guide

## Common Steps

1. **Clone the repository**:
   ```sh
   git clone https://github.com/Jitesh001/accuknox_assignment.git
   ```

2. **Navigate to the repository folder**:
   ```sh
   cd accuknox_assignment
   ```

3. **Navigate to the Django project folder**:
   ```sh
   cd social_network
   ```

## Method 1: Running the Project on a Local Machine with Python Virtual Environment

Ensure you have Python3 installed on your local machine.

1. **Create a virtual environment**:
   ```sh
   python -m venv <env_name>
   ```

2. **Activate the virtual environment**:
   ```sh
   <env_name>/Scripts/activate
   ```

3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the project on a local server and test API endpoints using Postman with the shared collections**:
   ```sh
   python manage.py runserver
   ```

## Method 2: Running the Project with Docker

### Method 2.1: Using Dockerfile

Ensure your Docker engine is running.

1. **Create a Docker image**:
   ```sh
   docker build --tag <your_image_tag> .
   ```

2. **Run the development server using the created Docker image, and test API endpoints using Postman with the shared collections**:
   ```sh
   docker run --publish 8000:8000 <your_image_tag>
   ```

### Method 2.2: Using docker-compose.yml

Ensure your Docker engine is running.

1. **Create a Docker image**:
   ```sh
   docker build --tag <your_app_name> .
   ```

2. **Run the development server using the created Docker image, and test API endpoints using Postman with the shared collections**:
   ```sh
   docker-compose up --build
   ```

---

This README provides clear and concise instructions for setting up and running your project using either a local Python virtual environment or Docker.
