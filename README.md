# Federated Recommender System

This project leverages Fedn to implement a distributed federated learning framework for a music recommendation system. Collaboratively developed by Umeå University and Linköping University, it utilizes Spotify datasets to train and evaluate the model. The following provides an overview of the project, setup instructions, usage guide, and results.

## Authors
+ [Lukas Eveborn], [Linköping University]
+ Christian Gustavsson, Linköping University
+ Olle Hansson, Linköping University
+ Yangyang Wen, Umeå University

## Project Description
### Objective
To design and demonstrate a distributed recommendation system using federated learning that suggests personalized music playlists based on user preferences.

### Key features
+ Distributed federated learning using Fedn.
+ Music recommendation model adapted from an Amazon Book neural network.
+ Preprocessed Spotify dataset for training.
+ Automatic token installation API for client integration.
+ Demonstration of real-time model updates and weights aggregation.

[Write a concise and informative description of your project here (100-400 words). Focus on the purpose, key features, and goals of the project. For example, what problem does it solve, how does it work, and what makes it unique?]  

## Oral Presentation Document  
https://docs.google.com/presentation/d/1vwBrOeIUwzV4vr9qLPf-0gjrwkwZA6DJtOSQCfVIUS4/edit#slide=id.p

## Author Contributions  
- **[Lukas]**: Responsible for client deployment, i.e. handling connections to clients, distribution of data via google-drive/google-cloud and creating the necessary environment for clients to do the training. Code-wise, this would be the content of the client-deployment folder. 
- **[Christian]**:  Data pre-processing, i.e., repurposing the original dataset and working with Olle to prepare the relevant data for client distribution. The code for this work is uploaded into the data-processing folder.
- **[Yangyang Wen]**: [Brief description of their contributions.]

| Role                | Resposibility                                              |
| ------------------- | ---------------------------------------------------------- |
| Model Adaptation    | Modifying the Amazon Book NN to fit Spotify's music data.  |
| Data Preprocessing  | Preparing Spotify data into training-ready datasets.       |
| API Development     | Automating token installation and client model integration.|
| Client Deployment   | Running distributed clients at Umeå University.            |


## License  
MIT License 

## Code and Repository Structure  
This repository contains the code used in our group project. The structure is as follows:  
- `src/`: Source code for the project.  
- `data/`: Example or synthetic datasets used during experiments.  
- `docs/`: Documentation and presentation materials.  
- `README.md`: This file. 

# Installation and Setup
## Requirements
+ Python: Version >= 3.7, recommended: Python >=3.9, <=3.12.
+ Fedn: Ensure that Fedn is installed and configured.
+ Required libraries:

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
 
