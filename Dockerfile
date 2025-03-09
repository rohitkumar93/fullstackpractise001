FROM python:3.11

# Set working directory inside the container to match your project structure
WORKDIR /src

# Copy requirements first for caching
COPY requirements.txt requirements.txt

# Install dependencies (only when requirements.txt changes)
RUN pip install --upgrade -r requirements.txt

# Copy everything into the container
COPY . .

# Copy and set permissions for entrypoint script (Update: Not needed atm)
# COPY entrypoint.sh /src/
# RUN chmod +x /src/entrypoint.sh

# Expose FastAPI's default port
EXPOSE 8000

# Start the FastAPI app (ensure the path to main.py is correct)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
