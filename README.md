# Python - MongoDB project using Apache Kafka

A simple purchase service that allows users to buy items and check all purchased items. This project uses Python for the API and client servers, MongoDB for data storage, Kafka for messaging, and Kubernetes for orchestration.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Usage](#usage)
- [License](#license)

## Features

- Buy items and store purchase information in MongoDB.
- Retrieve a list of all purchased items.
- Asynchronous communication using Kafka.
- Containerized deployment using Docker and Kubernetes.

## Technologies

- **Programming Language**: Python
- **Web Framework**: Flask
- **Database**: MongoDB
- **Messaging Queue**: Kafka
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Local Development**: Minikube

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

### Setting Up the Environment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd purchase_service
   ```

2. **Start Minikube**:
   ```bash
   minikube start
   eval $(minikube docker-env)
   ```

3. **Build Docker Images**:
   ```bash
   # Build API server image
   cd src/api
   docker build -t api-server:latest .

   # Build Client image
   cd ../client
   docker build -t client-server:latest .
   ```

4. **Create the Kubernetes Namespace**:
   ```bash
   kubectl create namespace python-mongodb
   ```

5. **Apply Kubernetes Manifests**:
   ```bash
   kubectl apply -f k8s-manifests/ --namespace=python-mongodb
   ```

## Deployment

This project deploys the following services in the `python-mongodb` namespace:

- **MongoDB**: Stores purchase data.
- **Zookeeper**: Manages Kafka cluster.
- **Kafka**: Handles messaging between services.
- **API Server**: Provides endpoints for buying items and retrieving purchase history.
- **Client Server**: User interface for interacting with the purchase service.

## Usage

1. **Access the Client**:
   After deploying, you can access the client at `http://<minikube-ip>:30002`. Use the following command to get the Minikube IP:
   ```bash
   minikube ip
   ```

2. **Buy an Item**:
   Use the interface to submit a buy request.

3. **Get All Purchased Items**:
   Click the button to retrieve and display all purchased items.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
