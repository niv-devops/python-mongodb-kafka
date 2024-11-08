# Python - MongoDB project using Apache Kafka

A simple purchase service that allows users to buy items and check all purchased items. This project uses Python and Flask for the API and client servers, MongoDB for data storage, Kafka and Zookeeper for messaging, and Kubernetes for orchestration. The application is also deployed in a Kubernetes environment using Helm for easy management.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Usage](#usage)
- [License](#license)

## Features

- Buy/Remove items and store purchase information in MongoDB.
- Retrieve a list of all purchased items.
- Asynchronous communication using Kafka.
- Containerized deployment using Docker and Kubernetes.
- Manage deployment using Helm Charts.

## Technologies

- **Programming Language**: Python
- **Web Framework**: Flask
- **Database**: MongoDB
- **Messaging Queue**: Kafka
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Local Development**: Minikube
- **Deployment**: Helm

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Helm](https://helm.sh/docs/intro/install/)

### Setting Up the Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/niv-devops/python-mongodb-kafka.git
   cd python-mongodb-kafka
   ```

2. **Start Minikube**:
   ```bash
   minikube start
   eval $(minikube docker-env)
   ```

3. **Build Docker Images**:
   ```bash
   docker build -t kafka-python:latest .
   docker tag kafka-python:latest devopsgoofy/kafka-python:latest
   docker push devopsgoofy/kafka-python:latest
   ```

4. **Apply The Cluster**:
   ```bash
   # Create the Kubernetes namespace
   kubectl create namespace python-mongodb
   
   # Apply manifest files
   kubectl apply -f k8s-manifests/ --namespace=python-mongodb
   kubectl get pods
   
   # Obtain IP Address for external access
   minikube ip
   ```

5. **Setup MongoDB**:
   ```bash
   # Access the pod and create DB & Collections
   kubectl exec -it -n python-mongodb <mongodb-pod-name> -- bash
   mongosh
   use shop;
   db.createCollection("customers");
   db.createCollection("items");

   # Insert data into collections
   db.items.insertMany([
     { "item": "Blue Jersey", "price": 80, image: 'https://cdn.jerseyaz.com/wp-content/uploads/2024/04/gexdimzsguAdgmjugCAtmnrxgexdambqgaxdkmjrgaAdqmrwgCxtkmztgexdknjt-510x510.jpeg' },
     { "item": "Orange Jersey", "price": 90, image: 'https://fanatics.frgimages.com/denver-broncos/youth-denver-broncos-peyton-manning-nike-orange-team-color-game-jersey_pi787000_altimages_ff_787747alt1_full.jpg?_hv=2&w=900' },
     { "item": "White Jersey", "price": 100, image: 'https://fanatics.frgimages.com/denver-broncos/youth-denver-broncos-peyton-manning-nike-white-game-jersey_pi787000_altimages_ff_787753alt1_full.jpg?_hv=2&w=900' }
   ]);

   db.customers.insertMany([
     { "username": "admin", "password": "adminpass", "Blue Jersey": 0, "Orange Jersey": 0, "White Jersey": 0 },
     { "username": "user", "password": "userpass", "Blue Jersey": 0, "Orange Jersey": 0, "White Jersey": 0 }
   ]);

   # Verify Data and exit
   show dbs
   db.items.find()
   db.customers.find()
   exit
   ```

6. **Create Helm Chart**:
   ```bash
   helm create kafka-mongo-chart
   helm dependency update
   helm install kafka-mongo-chart . --namespace chart-python-mongodb --create-namespace
   helm status kafka-mongo-chart --namespace chart-python-mongodb
   ```

7. **(Optional) For test environment on local machine**:
   ```bash
   # Create virtual environment
   sudo apt install python3-venv
   python3 -m venv .venv
   source .venv/bin/activate

   # Install requirments
   pip install flask kafka-python pymongo

   # Start the ZooKeeper server
   bin/zookeeper-server-start.sh config/zookeeper.properties

   # Start the Kafka server (On another terminal)
   bin/kafka-server-start.sh config/server.properties
   ```

## Deployment

This project deploys the following services in the `python-mongodb` namespace:

- **MongoDB**: Stores purchase data.
- **Zookeeper**: Manages Kafka cluster.
- **Kafka**: Handles messaging between services.
- **API Server**: Provides endpoints for buying items and retrieving purchase history.
- **Client Server**: User interface for interacting with the purchase service.

1. **Deploy using Helm**:

   Navigate to the main chart directory and install the application:

   ```bash
   helm install my-project ./ --namespace python-mongodb --create-namespace
   ```

2. **Verify the deployment**:

   Check the status of the deployed services:

   ```bash
   helm status my-project --namespace python-mongodb
   kubectl get pods -n python-mongodb
   kubectl get svc -n python-mongodb
   ```

## Usage

1. **Access the Client**:
   After deploying, you can access the client at `http://<minikube-ip>:30002`. Use the following command to get the Minikube IP:
   ```bash
   minikube ip
   ```

2. **Login**:
   Use the interface to into existing account or insert new data into the form, user will be created automatically.

2. **Buy an Item**:
   Use the interface to submit a buy request.

3. **Get All Purchased Items**:
   Click the `View Cart` button to retrieve and display all purchased items.

4. **Remove An Item**:
   Click the `Remove` button to remove item from the list, which will reset its quantity value to 0.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
