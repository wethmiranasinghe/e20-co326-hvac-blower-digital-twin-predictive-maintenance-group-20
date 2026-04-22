FROM python:3.11-slim

WORKDIR /app
COPY . /app

ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Generate training data and train the anomaly detection model
RUN python generate_data.py
RUN python train_model.py

CMD ["python", "mqtt_publisher.py"]