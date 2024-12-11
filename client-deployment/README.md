# Client Deployment

This directory contains the necessary files and instructions for deploying the client-side application.

## Files

- `deployClients.py`: Script to automate the deployment process.
- `getData.py`: Script to fetch Google Drive data tokens which is used in the deployment

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
1. **Upload Data to Google Drive**

    We used Google Drive for storage. There should be one `client.yaml` file for each client and one data package for each client in the drive. The files should be named as follows:
    
    - `client-1.yaml`, `client-2.yaml`, etc.
    - `packet-1.zip`, `packet-2.zip`, etc.

    The `client.yaml` files can be generated at FEDn/Scaleout website and are used to connect to the project.

2. **Get the Service Account File**
   
   In order to be able to fetch the data from the drive a service account at Google Cloud is needed. The service account then needs to be shared access to the drive. When that is done a service account file for the service account should be downloadedand put in the same directory as `getData.py`.

3. **Update `getData.py`**
   
   Update the `getData.py` with correct name on the service account file.

4. **Run `getData.py`**
   
   Execute the `getData.py` script to fetch all necessary tokens and store them in a CSV file. Each computer will require one token for the `client.yaml` file and one for the data being used.

   ```sh
   python getData.py
   ```

5. **Update the Host List**
   
   Before running the deployment script, ensure that the host list in `deployClients.py` is updated with the correct information for each client machine.

6. **Run `deployClients.py`**
   
   Execute the `deployClients.py` script to start the deployment process. 

   ```sh
   python deployClients.py
   ```
   The script will create a folder with copies of all the bash scripts executed during the actual deployment.
   You can perform a dry-run of the deployment process which then only generates the scripts. This is done by changing the dry_run variable in the script.

7. **Monitor the clients with tmux**

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


