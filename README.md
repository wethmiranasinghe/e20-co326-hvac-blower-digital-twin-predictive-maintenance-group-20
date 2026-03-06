# HVAC Blower Digital Twin Predictive Maintenance

This project implements an **Industrial Internet of Things (IIoT) based Digital Twin system** designed to monitor and predict potential failures in an HVAC blower fan. HVAC (Heating, Ventilation, and Air Conditioning) systems rely heavily on blower fans to maintain proper airflow in buildings and industrial environments. Over time, factors such as airflow blockage, bearing wear, or mechanical stress can increase motor load and eventually lead to system failures. Early detection of such conditions is essential to reduce downtime, prevent equipment damage, and improve energy efficiency.

The objective of this project is to develop a **predictive maintenance framework** that continuously monitors the operational health of a blower fan using real-time sensor data. A **current sensor (ACS712)** is used to measure the motor current of a 12V brushless DC fan, which acts as a scaled representation of an HVAC blower. Variations in motor current are analyzed to detect abnormal operating conditions such as airflow obstruction or increased mechanical load.

An **ESP32-S3 microcontroller** serves as the edge device responsible for data acquisition and local processing. The system performs **edge-level anomaly detection using lightweight machine learning techniques (TinyML)** to identify unusual patterns in motor current. These anomaly scores and sensor readings are transmitted through an **MQTT-based communication pipeline using the Sparkplug B topic structure**, enabling structured industrial messaging and a Unified Namespace (UNS).

The project follows a **four-layer Industrial IoT architecture**:

1. **Perception Layer** – Sensor data acquisition and feature extraction using the ESP32-S3.
2. **Transport Layer** – Secure data transmission via MQTT following a structured topic hierarchy.
3. **Edge Logic Layer** – Data processing, rule-based logic, and orchestration using Node-RED.
4. **Application Layer** – Time-series data storage using InfluxDB and visualization through Grafana dashboards.

The collected data is stored in **InfluxDB**, a time-series database optimized for industrial telemetry. Visualization and monitoring are performed using **Grafana**, which provides a SCADA-style interface to represent the system’s **Digital Twin**. The Digital Twin maintains real-time synchronization with the physical system, allowing operators to observe system behavior, detect anomalies, and remotely control the blower fan through a relay module.

Additionally, the system performs **trend analysis and Remaining Useful Life (RUL) estimation** in the cloud layer using Node-RED function nodes. This allows the system to provide predictive insights into potential motor degradation over time.

To ensure industrial-grade reliability, the system incorporates several **cybersecurity and reliability features**, including MQTT authentication, controlled topic access, Last Will and Testament (LWT) messages for device status monitoring, automatic reconnection mechanisms, and timestamped data logging.

Overall, this project demonstrates a complete **cyber-physical monitoring system integrating embedded hardware, industrial communication protocols, edge intelligence, and cloud analytics**. It highlights how modern industrial environments can transition from traditional reactive maintenance strategies to **predictive maintenance using Digital Twin technologies and Industrial IoT architectures**.

---
