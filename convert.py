import json


# Function to convert .ipynb to .txt
def convert_ipynb_to_txt(ipynb_file, txt_file):
    # Load the .ipynb file
    with open(ipynb_file, 'r') as f:
        notebook = json.load(f)

    # Open the .txt file for writing
    with open(txt_file, 'w') as f:
        # Iterate through the cells in the notebook
        for cell in notebook['cells']:
            # Check if the cell is a code cell
            if cell['cell_type'] == 'code':
                # Write the code to the .txt file
                f.write(''.join(cell['source']))
                f.write('\n\n')  # Add space between cells for readability

# Example usage
convert_ipynb_to_txt('GlobalWarmingPSO.txt','output.txt')