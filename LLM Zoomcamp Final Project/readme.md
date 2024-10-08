# Hobbit Q&A Project

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Setup and Installation](#setup-and-installation)
   - [Local Setup](#local-setup)
   - [Docker Setup](#docker-setup)
5. [Usage](#usage)
6. [Monitoring](#monitoring)
7. [Screenshots](#screenshots)

## Project Overview

The Hobbit Q&A Project is an interactive question-answering system based on J.R.R. Tolkien's "The Hobbit". It uses natural language processing and machine learning techniques to provide answers to user queries about the book. The system is built with Python, leveraging the LangChain framework and the Groq API for language model inference.

## Features

This QA Chatbot is designed to answer all Hobbit-related questions for anyone interested in this part of Tolkien's legendarium. I have also added additional texts in the event that the user wants to explore other parts of the Tolkien lore including the Silmarillion and the Lord of the Rings.

## Prerequisites

- Python 3.8 or higher
- Groq API key
- Docker and Docker Compose (for Docker setup)
- "The Hobbit" text file (not provided due to copyright)

## Setup and Installation

### Local Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/hobbit-qa.git
    cd hobbit-qa
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root and add your Groq API key:

    ```bash
    GROQ_API_KEY=your_api_key_here
    ```

5. Place "The Hobbit" text file in the project root directory and name it `Hobbit, The - J. R. R. Tolkien.txt`.

6. Run the application:

    ```bash
    python hobbit_qa.py
    ```

### Docker Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/hobbit-qa.git
    cd hobbit-qa
    ```

2. Create a `.env` file in the project root and add your Groq API key:

    ```bash
    GROQ_API_KEY=your_api_key_here
    ```

3. Place "The Hobbit" text file in the project root directory and name it `Hobbit, The - J. R. R. Tolkien.txt`.

4. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

## Usage

1. Once the application is running, you'll see a welcome message and a prompt for your question.
2. Type your question about "The Hobbit" and press Enter.
3. The system will process your question and provide an answer along with relevant sources from the book.
4. To exit the application, type 'quit' and press Enter.

## Monitoring

The project includes Prometheus for metrics collection and Grafana for visualization.

- Prometheus: Access at `http://localhost:9090`
- Grafana: Access at `http://localhost:3000`
- Default login: admin/admin
- Import the provided dashboard JSON file for a pre-configured Hobbit Q&A dashboard.

I have included two files for evaluation including Grafana or the monitor.py file. This gives users two options for monitoring the chatbot metrics. **It should be noted that this application runs best with a GPU. It can run locally, but compute times can be heavy, especially in the case of the evaluation.py file (run at your own risk).**

Metrics collected:

- Total number of queries processed
- Query processing latency

## Screenshots

| Screenshot 1 | Screenshot 2 | Screenshot 3 |
|--------------|--------------|--------------|
| ![Screenshot from 2024-10-08 11-57-34](https://github.com/user-attachments/assets/d3abe094-5646-4c9c-a32f-5ff9edde2946) | ![Screenshot from 2024-10-08 11-53-51](https://github.com/user-attachments/assets/17e315dc-d590-4a31-8bec-1be20027d8d0) | ![Screenshot from 2024-10-08 11-53-23](https://github.com/user-attachments/assets/e13e7f4f-6b48-48b2-b300-326a78a42633) |
| ![Screenshot from 2024-10-07 20-11-30](https://github.com/user-attachments/assets/f3781289-6a77-4659-8ef0-5e70deea9f11) | ![Screenshot from 2024-10-07 20-08-31](https://github.com/user-attachments/assets/24063645-f5b0-43c8-8df6-9b12bb4cf159) |              |
