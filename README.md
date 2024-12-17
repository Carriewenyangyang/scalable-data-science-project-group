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
- **Lukas Eveborn**: Responsible for client deployment, i.e. handling connections to clients, distribution of data via Google Drive/Google Cloud and creating the necessary environment for clients to do the training. Code-wise, this would be the content of the client-deployment folder. 
- **Christian Gustavsson**:  Data pre-processing, i.e., repurposing the original dataset and working with Olle to prepare the relevant data for client distribution. The code for this work is uploaded into the data-processing folder.
- **Yangyang Wen**: Configured the virtual machines in Umeå with Ubuntu OS, ensuring sufficient resources <!--(at least 4-core CPU, 8GB RAM)--> for client deployment and federated learning. Collaborated with Linköping nodes for seed model training and federated learning. Created the project PPT, refined content with the team. Set up the GitHub repository and compiled the README file.
- **Olle Hansson**: Responsible for the adaptation of the Amazon Book neural network for the Spotify music dataset, modifying the architecture to optimize it for the music recommendation task. Conducted research to refine the model and ensure its effectiveness. Assisted in preparing and preprocessing the dataset, ensuring data quality and compatibility for training.

| Role                | Resposibility                                              |
| ------------------- | ---------------------------------------------------------- |
| Model Adaptation    | Modifying the Amazon Book NN to fit Spotify's music data.  |
| Data Preprocessing  | Preparing Spotify data into training-ready datasets.       |
| API Development     | Automating token installation and client model integration.|
| Client Setup & Management | Setting up and configuring distributed clients at Umeå University for federated learning.            |

## Code and Repository Structure  
This repository contains the code used in our group project. The structure is as follows:  
- `client-deployment/`: Scripts for automating client setup, connecting to the federated server, and data downloading.
- `data-processing/`: Preprocessing Spotify datasets for training and evaluation.
- `fedn-lightgcn/client/`: Contains the core recommendation model (LightGCN) and training/validation scripts. 
- `research/`: Contain a paper related to Fedn in scalable federated machine learning.
- `README.md`: This file.
- `lightgcn.py`: The core code of the recommendation system based on the LightGCN model.

## Installation and Setup
### Prerequisites
+ Python: Version >= 3.7, recommended: Python >=3.9, <=3.12.
+ Fedn: Ensure that Fedn is installed and configured.
+ Required libraries: See `fedn-lightgcn/client/python_env.yaml` and `client-deployment/requirements.txt`.

### Steps
1. Clone the Repository:
   ```
   git clone https://github.com/Carriewenyangyang/scalable-data-science-project-group.git
   ```
2. Setup Virtual Environment:
   ```
   pip install -r requirements.txt
   ```
3. Prepare the Dataset:
   - Download the Spotify dataset.
   - Preprocess the data:
     ```
     cd data-processing
     python preprocess_data.py
     ```
4. Deploy clients:
   ```
   cd client-deployment
   python deployClients.py
   ```
  
## Usage 
1. Start the federated learning server via Fedn.
2. Deploy clients to connect with the server.
3. Monitor training and weight updates via the Fedn dashboard.

## Results
- **Federated Learning**: Successfully demonstrated weight aggregation across distributed clients.
- **Model Performance**: Personalized playlist recommendations based on LightGCN.

## License  
MIT License 

## References
- [Research Papers on Fedn](https://github.com/Carriewenyangyang/scalable-data-science-project-group/tree/main/research)
