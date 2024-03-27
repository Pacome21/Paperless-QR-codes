import configparser
import os
from pathlib import Path

def get_asn_from_user():
    """
    Prompts the user for an ASN and returns it.
    """
    while True:
        try:
            asn = int(input("Enter start ASN : "))
            return asn
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            
            


# Define the config file path
config_path = Path(os.path.expanduser('~/.config/asn_config.ini'))

# Ensure the directory exists
os.makedirs(os.path.dirname(config_path), exist_ok=True)

# Create a ConfigParser object
config = configparser.ConfigParser()

def load_asn():
    # Check if the config file exists
    if config_path.exists():
        # Read the ASN number from the config file
        config.read(config_path)
        return int(config.get('StartASN', 'asn', fallback='ASN number not set'))
    else:
        # If the config file doesn't exist, create it and set a default ASN number
        try:
            asn = get_asn_from_user()
            config['StartASN'] = {'asn': asn}
            with open(config_path, 'w') as configfile:
                config.write(configfile)
            return asn
        except:
            return -1

def save_asn(asn_number):
    # Update the ASN number in the config file
    config['StartASN']['asn'] = str(asn_number)
    with open(config_path, 'w') as configfile:
        config.write(configfile)
        
def get_output_file_path(label_type, asn):
    downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    fname = "labels-{0}-{1}.pdf".format(label_type, asn)
    file_path = os.path.join(downloads_dir, fname)
    return file_path

# Example usage
#asn = load_asn()
#print(f'Loaded ASN: {asn}')
#asn+=1

# Update the ASN number
#save_asn(asn)
#print(f'Updated ASN: {load_asn()}')

            
