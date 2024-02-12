import subprocess
import os
import shutil

# Define input directory and output directory
input_directory = "/home/yustinus/PneumoKITy/data"
output_directory = "/home/yustinus/PneumoKITy/output"

# Add Flye executable directory to PATH
flye_path = "/home/yustinus/anaconda3/envs/flye/bin"
os.environ['PATH'] += os.pathsep + flye_path

# List all files in the input directory
input_files = os.listdir(input_directory)

# Process each input file
for input_file in input_files:
    # Check if the file is a FASTQ file
    if input_file.endswith(".fastq.gz") or input_file.endswith(".fq.gz"):
        # Define input and output files
        input_fastq = os.path.join(input_directory, input_file)
        output_prefix = os.path.splitext(input_file)[0]
        output_assembly_dir = os.path.join(output_directory, f"flye_output_{output_prefix}")
        output_assembly = os.path.join(output_assembly_dir, "assembly.fasta")

        # Ensure the output directory exists
        os.makedirs(output_assembly_dir, exist_ok=True)

        # Step 1: Run Flye
        flye_command = f"flye --nano-raw {input_fastq} --out-dir {output_assembly_dir}"
        try:
            subprocess.run(flye_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running Flye for {input_file}: {e}")
            continue

        # Step 2: Copy assembly file to data directory
        assembly_file_src = os.path.join(output_assembly_dir, "assembly.fasta")
        assembly_file_dest = os.path.join(input_directory, f"{output_prefix}_assembly.fasta")
        try:
            shutil.copy(assembly_file_src, assembly_file_dest)
        except shutil.Error as e:
            print(f"Error copying assembly file for {input_file}: {e}")
            continue

        print(f"Assembly completed successfully for {input_file}!")

print("All samples processed successfully!")
# Define input directory and output directory
input_directory = "/home/yustinus/PneumoKITy/data"
output_directory = "/home/yustinus/PneumoKITy/data/serotyping_results"

# List all files in the input directory
input_files = os.listdir(input_directory)

# Process each input file
for input_file in input_files:
    # Check if the file is an assembly file
    if input_file.endswith("_assembly.fasta"):
        # Define input and output files
        input_assembly = os.path.join(input_directory, input_file)
        output_prefix = os.path.splitext(input_file)[0]
        output_dir = os.path.join(output_directory, f"{output_prefix}_pneumokity_output")

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Run PneumoKITy script for serotyping
        serotyping_command = f"python pneumokity.py pure -a {input_assembly} -m mash -o {output_dir}"
        try:
            subprocess.run(serotyping_command, shell=True, check=True)
            print(f"Serotyping completed successfully for {input_assembly}")
        except subprocess.CalledProcessError as e:
            print(f"Error running PneumoKITy for {input_assembly}: {e}")
            continue

print("All samples processed successfully!")

