FROM python:3.11-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory to /backend
COPY ./backend /backend
# Set PYTHONPATH to include the backend directory
ENV PYTHONPATH=/backend

EXPOSE 8080
# Change working directory to backend and run from there
WORKDIR /backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]