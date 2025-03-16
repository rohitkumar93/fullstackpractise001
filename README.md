Document Management and RAG-based Q&A Application


## Overview

The Document Management System is a FastAPI-based web application that allows users to upload Documents and search through them. 

## Features

- **Ingest a New Document**: Upload and ingest Documents, and at the same time, process it to store it in vector form so our QNA service can fetch them
- **Select a Document**: Add a Document to the selection to search from.
- **Retrieve Document**: Fetch a Document's Vector to see if the question that has been asked, has relevant vectors or not.
- **OpenAI QNA**: Once a question has been asked, the OpenAI client will search through the vectors given  in the selected documents, and formulate an answer using LLM to create a meaningful answer.



The OpenAI client being used, does have some general knowledge already. My intention was to use a good LLM so it can formulate and create meaningful sentences. Unfortunately, to test if the retrieval and ingestion services work, we have to ask questions that the OpenAI does not already know, so we can assert that it is indeed learning from the documentation we are providing.e.g.

 




First we ask a non general knowledge question, and it replies it does not know.


![Screenshot 2025-03-10 022801](https://github.com/user-attachments/assets/3688e865-2efb-4382-a2c0-8a6f31068872)

Then we feed/ingest that data in the database. We also need to add that document ID to selected_ids using the selection service, so the QNA will search through the selected ids only.

![image](https://github.com/user-attachments/assets/1100f86e-d04b-44c6-be69-896d09b3d09e)

Now the AI knows that new information!

![Screenshot 2025-03-10 023810](https://github.com/user-attachments/assets/ee74c4d2-02a0-42c4-9ae1-6e58b2f0cee6)






## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL-15 with pgvector
- **Asynchronous Support**: SQLAlchemy with AsyncIO
- **Lint**: Ruff [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Installation

Pull the docker image from:

> docker pull dadarklord/rag_qna:latest

(Could be under construction as I am actively working on this project still)

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15
- pip (Python package manager)

### Steps to Set Up the Application

1. **Clone the repository:**

   ```bash
   git clone https://github.com/rohitkumar93/fullstackpractise001.git
   cd fullstackpractise001

2. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate |  For Windows use: .venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Copy the .env.example file and load a working OpenAI client Key**
     This project uses OpenAI client which needs atleast a free tier of OpenAI; I have securely added the credentials in the docker image, but cannot add it on the gh repo. 
     Contact me if you need the key to run the application.


TODO:

CI/CD Workflow for Deploying the Document Management System on AWS

~~Optimize with asyncio.gather for each operation~~

~~Add two ingesters for easy Real sample data creation~~

~~Used OpenAI client(free tier) for constructing final answers from retrieval~~

Tests for Ability to handle large dataset (Tested with large requests, tested with mutliple requests at the same time, not yet tested Large Multiple requests)

Tests for Demonstrating strategies for large-scaledocument ingestion,storage,and
efficientretrieval

Create comprehensive design documentation

Additional coverage for edge cases like handling timeouts or rate limiting

Optimize Dockerization

Add Cloud deployment instructions

Much more work to be done!


# Miscellaneous:

Curl command to test multiple (add ending brace at 144):

```
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
```
