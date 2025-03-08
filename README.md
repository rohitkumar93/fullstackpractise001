Features# Coding Exercise: Document Management and RAG-based Q&A Application


## Overview

The Document Management System is a Flask-based web application that allows users to manage a collection of Documents. Users can add, update, delete, and retrieve Documents, along with their summaries and reviews. This application utilizes PostgreSQL for data storage and provides a simple RESTful API for interaction.

## Features

- **Add a New Document**: Add Documents with details such as title, author, genre, year published, and summary.
- **Retrieve All Documents**: Fetch a list of all Documents in the database.
- **Retrieve a Document by ID**: Get detailed information about a specific Document.
- **Update a Document**: Modify the details of an existing Document.
- **Delete a Document**: Remove a Document from the database.
- **Get Document Summary**: Fetch a Document's summary and average rating.
- **Add Reviews**: Add reviews and ratings for each Document.
- **Get Reviews**: Get all reviews of a Document

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Asynchronous Support**: SQLAlchemy with AsyncIO
- **API Documentation**: Swagger UI via Flasgger

## Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL
- pip (Python package manager)

### Steps to Set Up the Application

1. **Clone the repository:**

   ```bash
   git clone https://github.com/rohitkumar93/fullstackpractise001.git
   cd fullstackpractise001

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows use: venv\Scripts\activate

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Set up the PostgreSQL database**
    ```sql
    CREATE DATABASE Document_management_system;


## CI/CD Workflow for Deploying the Document Management System on AWS

### Steps to Set Up CI/CD Workflow

1. Create a Dockerfile
2. Create a GitHub Actions Workflow: In your GitHub repository, create a new directory .github/workflows and add a YAML file (e.g., bms.yml). This file will define the CI/CD workflow.
3. Deploying the Application: When we push changes to the main branch of your GitHub repository, GitHub Actions will automatically run the CI/CD workflow defined in .github/workflows/bms.yml.README.md







Used Ruff for lint
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

yet TODO:
Next Step: Optimize with asyncio.gather for each operation


Added two ingesters for easy sample data creation

I have used OpenAI client(free tier) for constructing final answers from retrieval

Tests for Ability to handle large dataset (Tested with large requests, tested with mutliple requests at the same time, not yet tested Large Multiple requests)

Tests for Demonstrating strategies for large-scaledocument ingestion,storage,and
efficientretrieval

Create comprehensive design documentation

Additional coverage for edge cases like handling timeouts or rate limiting

Optimize Dockerization

Add Cloud deployment instructions

Much more work can be done!


Curl command to test multiple (add ending brace at 144):
# Start background jobs
$jobs = 1..10 | ForEach-Object {
    Start-Job -ScriptBlock {
        param($i, $startTime)

        # Generate timestamp and random variation
        $timestamp = (Get-Date -Format "HHmmssfff")  # Unique per request
        $variation = "random_text_" + (Get-Random -Minimum 1 -Maximum 1000)  # Randomized input

        # Record start time
        $start = Get-Date

        try {
            # Send request with slight variations
            $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/ingestion/" `
                                          -Method Post `
                                          -Headers @{"Content-Type" = "application/json"} `
                                          -Body (@{
                                              filename="test_document_$i_$timestamp.txt"
                                              content="This is test document number $i with $variation at $timestamp."
                                          } | ConvertTo-Json -Depth 10)

            # Record end time
            $end = Get-Date
            $duration = ($end - $start).TotalMilliseconds

            # Output result with timing
            Write-Output "Request $i started at: $($start - $startTime) | Completed in: $duration ms | Response: $($response | ConvertTo-Json -Compress)"
        }
        catch {
            Write-Output "Request $i failed: $_"
        }

    } -ArgumentList $_, (Get-Date)
 

# Wait for jobs to complete
$jobs | ForEach-Object { Wait-Job -Id $_.Id }

# Collect and display job output
$jobs | ForEach-Object { Receive-Job -Id $_.Id }

# Cleanup finished jobs
$jobs | ForEach-Object { Remove-Job -Id $_.Id }
