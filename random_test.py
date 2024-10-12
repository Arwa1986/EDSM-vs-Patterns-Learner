import subprocess
import os

# Ensure the NuSMV executable is in the PATH
nusmv_path = "/home/arwa/Programs/NuSMV-2.6.0-linux64/NuSMV-2.6.0-Linux/bin/NuSMV"  # Replace with the actual path to NuSMV

# Full path to the input file
input_file = "/smv/model.smv"

# Print the current working directory
print("Current working directory:", os.getcwd())

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Error: The file {input_file} does not exist.")
else:
    # Run the command

    result = subprocess.run([nusmv_path, input_file], capture_output=True, text=True)

    # Print the output and error
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)