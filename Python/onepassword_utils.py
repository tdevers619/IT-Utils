# filename: onepassword_utils.py

import subprocess
import json
import os

def get_1password_secret(item_name, fields, session_token=None):
    """
    Retrieves a secret from a 1Password item.

    Parameters:
    - item_name (str): The name or UUID of the 1Password item.
    - fields (str): The field of the item to retrieve (e.g., "password").
    - session_token (str, optional): The 1Password CLI session token.

    Returns:
    - str: The secret from the specified item field.

    Raises:
    - Exception: If there is an error executing the command or parsing the output.
    """
    # Use provided session token or fetch from environment
    if not session_token:
        session_token = os.environ.get('OP_SESSION_my')
        if not session_token:
            raise Exception("Session token is not set.")

    # Prepare the command to retrieve the secret
    command = f"op get item {item_name} --fields {fields}"

    # Set up the session token environment variable
    env = os.environ.copy()
    env["OP_SESSION_my"] = session_token
    
    # Run the command
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, env=env)
    
    # Check for errors
    if result.returncode != 0:
        raise Exception(f"Error executing command: {result.stderr}")

    # Parse the JSON output
    secret_data = json.loads(result.stdout.strip())
    
    # Retrieve and return the secret value
    return secret_data[fields]

# Example usage within this module if needed
if __name__ == "__main__":
    try:
        item_to_retrieve = "example-item-name"
        field_to_retrieve = "password"
        secret = get_1password_secret(item_to_retrieve, field_to_retrieve)
        print(f"The secret is: {secret}")
    except Exception as e:
        print(f"An error occurred: {e}")
