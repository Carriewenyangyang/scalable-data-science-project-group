# Client Deployment

This directory contains the necessary files and instructions for deploying the client-side application.

## Files

- `deployClients.py`: Script to automate the deployment process.
- `getData.py`: Script to fetch Google Drive data tokens which is used in the deployment
- `README.md`: This file, providing an overview and instructions.

## Prerequisites

Before running ensure you have the following tools installed:

### tmux

`tmux` is a terminal multiplexer that we use to manage multiple terminal sessions from a single window.

To install `tmux`, run the following command:

```sh
sudo apt-get update
sudo apt-get install tmux
```

### sshpass

`sshpass` is a non-interactive ssh password provider, used for automating ssh connections.

To install `sshpass`, run the following command:

```sh
sudo apt-get update
sudo apt-get install sshpass
```

### Python Requirements

Ensure you have Python and pip installed on your machine. Tests have been run with Python 3.10

To install the required Python packages, run the following command:

```sh
pip install -r requirements.txt
```

## Deployment Instructions

1. **Get the Service Account File**
   
   Obtain the service account file from Google Cloud and place it in the same directory as the deployment scripts.

2. **Update `getData.py`**
   
   Update the `getData.py` with correct name on the service account file.

3. **Run `getData.py`**
   
   Execute the `getData.py` script to fetch all necessary tokens and store them in a CSV file. Each computer will require one token for the `client.yaml` file and one for the data being used.

   ```sh
   python getData.py
   ```

4. **Update the Host List**
   
   Before running the deployment script, ensure that the host list in `deployClients.py` is updated with the correct information for each client machine.

5. **Run `deployClients.py`**
   
   Execute the `deployClients.py` script to start the deployment process. 

   ```sh
   python deployClients.py
   ```

6. **Monitor the clients with tmux**

    1. **List Clients in tmux**

        List all tmux sessions

        ```sh
        tmux ls
        ```

    2. **Attach to the Deployment Session**

        Attach to the tmux session named `client1`:

        ```sh
        tmux attach -t client1
        ```

    3. **Detach from the Session**

        To detach from the tmux session, press `Ctrl+b` followed by `d`.


