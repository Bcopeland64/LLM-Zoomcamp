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

- Interactive command-line interface for asking questions about "The Hobbit"
- Utilizes advanced NLP techniques for accurate and context-aware answers
- Integration with Prometheus for metrics collection
- Grafana dashboard for visualizing system performance
- Docker support for easy deployment and scalability

## Prerequisites

- Python 3.8 or higher
- Groq API key
- Docker and Docker Compose (for Docker setup)
- "The Hobbit" text file (not provided due to copyright)

## Setup and Installation

### Local Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/hobbit-qa.git
   cd hobbit-qa
   ```
2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root and add your Groq API key:

   ```
   GROQ_API_KEY=your_api_key_here
   ```
5. Place "The Hobbit" text file in the project root directory and name it `Hobbit, The - J. R. R. Tolkien.txt`.
6. Run the application:

   ```
   python hobbit_qa.py
   ```

### Docker Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/hobbit-qa.git
   cd hobbit-qa
   ```
2. Create a `.env` file in the project root and add your Groq API key:

   ```
   GROQ_API_KEY=your_api_key_here
   ```
3. Place "The Hobbit" text file in the project root directory and name it `Hobbit, The - J. R. R. Tolkien.txt`.
4. Build and run the Docker containers:

   ```
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
  - Import the provided dashboard JSON file for a pre-configured Hobbit Q&A dashboard

Metrics collected:

- Total number of queries processed
- Query processing latency

## Screenshots
