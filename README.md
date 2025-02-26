# Kafka-Based Cash Flow Simulation

## Contributors

- [Jess Todd](https://github.com/Jessicacktodd)
- [Oli Kelly](https://github.com/olikelly00)

## Overview
This project simulates a **bank account system** using **Kafka** for real-time transaction processing. It consists of:

This setup demonstrates event-driven data processing and real-time transaction tracking.

## Technical Features
- **Kafka Producer (`producer.py`)**:
  - Publishes transactions to the `transactions` Kafka topic.
  - Generates random transactions with account IDs, amounts, and transaction types.
  - Maintains a transaction summary for each account.

- **Kafka Consumers**:
  - `logging-consumer.py`: Logs received transaction messages.
  - `balance-calculator-consumer.py`: Processes transactions and computes the running balance for each account.
  - Uses in-memory storage to track balances dynamically.

- **JSON-based Data Format**:
  ```json
  {
    "account": 3,
    "transaction_id": "3-Debit-abc123",
    "transaction_type": "Debit",
    "amount": 8,
    "new_balance": 97,
    "transaction_summary": {
      "Transactions for Customer ID 3": 5
    }
  }
  ```

## How to Run the Project

### **1. Start Kafka Locally**
Ensure you have Kafka running:
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &
```

### **2. Create the Kafka Topic**
```bash
bin/kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092
```

### **3. Run the Producer**
```bash
python producer.py
```
This script generates and sends random transactions to Kafka.

### **4. Run the Consumers**
Run the logging consumer:
```bash
python logging-consumer.py
```
Run the balance calculator consumer:
```bash
python balance-calculator-consumer.py
```

Each consumer listens to transaction messages and processes them in real time.

## Technical Challenges
- **Ensuring Correct Order of Messages**: Kafka does not guarantee message order across partitions, so designing an effective consumer processing strategy was key.
- **Handling Missing Transactions**: Implementing error handling to ensure that failed messages do not break the consumer logic.
- **Maintaining State Efficiently**: Since balances need to be updated dynamically, designing a lightweight in-memory solution was necessary.

## Key Learnings
- **Kafka Basics**: How to set up a producer and consumers.
- **Event-Driven Processing**: Handling real-time transactions efficiently.
- **State Management**: Keeping track of balances and transaction counts.
- **Error Handling**: Managing missing keys and ensuring robust message processing.
- **Scalability Considerations**: How Kafka consumers can be scaled to handle high-throughput transaction processing.
