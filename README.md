# Federated Recommender System

This project leverages Fedn to implement a distributed federated learning framework for a music recommendation system. Collaboratively developed by Umeå University and Linköping University, it utilizes Spotify datasets to train and evaluate the model. The following provides an overview of the project, setup instructions, usage guide, and results.

## Authors
+ Lukas Eveborn, Linköping University
+ Christian Gustavsson, Linköping University
+ Olle Hansson, Linköping University
+ Yangyang Wen, Umeå University

## Project Description
### Objective
To design and demonstrate a distributed recommendation system using federated learning that suggests personalized music playlists based on user preferences.

### Key features
+ Distributed federated learning using Fedn.
+ Music recommendation model adapted from an Amazon Book neural network.
+ Preprocessed Spotify dataset for training and evaluation.
+ API support for seamless client integration with automatic token installation.
+ Demonstrates real-time model updates and federated weight aggregation in action. 

## Oral Presentation Document  
https://docs.google.com/presentation/d/1vwBrOeIUwzV4vr9qLPf-0gjrwkwZA6DJtOSQCfVIUS4/edit#slide=id.p

## Author Contributions  
- **Lukas Eveborn**: Responsible for client deployment, i.e. handling connections to clients, distribution of data via google-drive/google-cloud and creating the necessary environment for clients to do the training. Code-wise, this would be the content of the client-deployment folder. 
- **Christian Gustavsson**:  Data pre-processing, i.e., repurposing the original dataset and working with Olle to prepare the relevant data for client distribution. The code for this work is uploaded into the data-processing folder.
- **Yangyang Wen**: Configured the virtual machine in Umeå with Ubuntu OS, ensuring sufficient resources (at least 4-core CPU, 8GB RAM) for client deployment and federated learning. Collaborated with Linköping nodes to train the seed model and perform federated learning. Initiated the project PPT and collaborated on refining its content. Set up the GitHub repository and compiled the README file.
- **Olle Hansson**: 

| Role                | Resposibility                                              |
| ------------------- | ---------------------------------------------------------- |
| Model Adaptation    | Modifying the Amazon Book NN to fit Spotify's music data.  |
| Data Preprocessing  | Preparing Spotify data into training-ready datasets.       |
| API Development     | Automating token installation and client model integration.|
| Client Setup & Management | Setting up and configuring distributed clients at Umeå University for federated learning.            |


## License  
MIT License 

## Code and Repository Structure  
This repository contains the code used in our group project. The structure is as follows:  
- `client-deployment/`: Scripts to deploy the clients to the cloud and step-by-step instructions.
- `data-processing/`: Scripts for downloading and preprocessing the synthetic datasets used during the experiments.
- `fedn-lightgcn/client/`: Documentation and presentation materials.
- `research/`: Contain a paper related to Fedn in scalable federated machine learning.
- `README.md`: This file.
- `lightgcn.py`: The core code of the recommendation system based on the LightGCN model.

# Installation and Setup
## Requirements
+ Python: Version >= 3.7, recommended: Python >=3.9, <=3.12.
+ Fedn: Ensure that Fedn is installed and configured.
+ Required libraries: See files fedn-lightgcn/client/python_env.yaml and client-deployment/requirements.txt.

## Steps
1. Clone the Repository:
2. Setup Virtual Environment:
3. Install Dependencies:
4. Prepare the Dataset:
   + Download the Spotify dataset from [Spotify Dataset Link].
   + Prepare the data using:
     
5. Run the API (set up the client tokens)
6. Deploy the Clients:
   + Ensure all clients are configured for training.
   + Run clients on distributed machines:
  
## Usage 
1. Start the federated server
2. Train the model across clients
3. Monitor weight updates and performance using the Fedn dashboard.
4. Evaluate the model

## Results
- Federated Learning:
  + Demonstrated weight aggregation across clients.
- Model Performance:
  + Personalized playlist recommendations.
 
