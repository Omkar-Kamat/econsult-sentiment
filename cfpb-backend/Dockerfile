FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first (helps with wheels on 3.12)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model and NLTK data at build time
RUN python -m spacy download en_core_web_sm
RUN python -c "import nltk; \
    nltk.download('stopwords'); \
    nltk.download('wordnet'); \
    nltk.download('punkt'); \
    nltk.download('punkt_tab')"

# Copy app source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]