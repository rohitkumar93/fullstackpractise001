# Coding Exercise: Document Management and RAG-based Q&A Application


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
