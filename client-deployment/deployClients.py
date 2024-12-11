import csv
import os


def generate_unique_bash_script(host, nr):
    # Same as your existing function
    csv_file = "file_mapping.csv"
    with open(csv_file, mode="r") as file:
        reader = list(csv.DictReader(file))
        if nr <= 0 or nr > len(reader):
            raise ValueError(f"Row number {nr} is out of range for the CSV file.")
        row = reader[nr - 1]
        packet_id = row["Packet_id"]
        client_id = row["Client_id"]

        return f"""#!/bin/bash
mkdir fedn_{host}
cd fedn_{host}
export DATA_PT_ID="{packet_id}"
export CLIENT_YAML_ID="{client_id}"
python3.10 -m venv venv
source venv/bin/activate
pip install gdown
gdown "https://drive.google.com/uc?export=download&id=$DATA_PT_ID" -O "data.zip"
gdown "https://drive.google.com/uc?export=download&id=$CLIENT_YAML_ID" -O "client.yaml"
unzip data.zip -d data
sed -i "s/^name: .*/name: {host}/" client.yaml
pip install fedn==0.19.0
export FEDN_PACKAGE_EXTRACT_DIR=package
export FEDN_DATA_PATH=../../data
fedn client start -in client.yaml
"""


def create_local_tmux_session(host, username, password, bash_script_content, dry_run):
    """
    Create a tmux session locally that SSHs into the remote host and runs a script.
    """
    if not bash_script_content:
        return f"Error: No bash script content provided for {host}."

    output_dir = "generated_scripts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the bash script content to a file - to know what we have done
    output_file = os.path.join(output_dir, f"{host}_script.sh")
    with open(output_file, "w") as script_file:
        script_file.write(bash_script_content)
    
    if not dry_run:
        os.chmod(output_file, 0o755)  # Make the script executable

        # Command to start the tmux session
        session_name = f"{host}"
        tmux_command = (
            f"tmux new-session -d -s {session_name} "
            f"\"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{host} 'bash -s' < {output_file}\""
        )

        # Execute the tmux command locally
        result = os.system(tmux_command)
        if result == 0:
            return f"Local tmux session '{session_name}' created for {host}."
        else:
            return f"Error creating tmux session for {host}."
    else:
        return f"DRY RUN: Local tmux session would be created for {host}."


def main():
    dry_run = False
    # Define your list of hosts and credentials
    hosts = [
        {"host": "asgard1-401", "username": "lukev81", "password": "xxxxx", "nr": 1},
        {"host": "asgard1-402", "username": "lukev81", "password": "xxxxx", "nr": 2},

    ]
    
    # Sequentially process each host
    for host_info in hosts:
        host = host_info["host"]
        username = host_info["username"]
        password = host_info.get("password")
        nr = host_info["nr"]

        # Generate the bash script for the host
        bash_script_content = generate_unique_bash_script(host, nr)

        # Create a tmux session locally for this host - and run the script
        result = create_local_tmux_session(
            host, username, password, bash_script_content, dry_run
        )
        print(f"Host: {host}")
        print(f"Output:\n{result}")
        print("-" * 40)


if __name__ == "__main__":
    main()
