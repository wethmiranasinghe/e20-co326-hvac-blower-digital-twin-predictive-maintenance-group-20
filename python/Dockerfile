FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Generate training data and train the anomaly detection model
RUN python generate_data.py
RUN python train_model.py

CMD ["python", "mqtt_publisher.py"]