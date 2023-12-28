#!/bin/bash
#SBATCH -J FuzzTest              
#SBATCH -p general                    
#SBATCH -o cpp_program_%j.txt         
#SBATCH -e cpp_program_%j.err         
#SBATCH --nodes=1                     
#SBATCH --ntasks-per-node=1           
#SBATCH --cpus-per-task=1             
#SBATCH --time=4:00:00                
#SBATCH --mail-user=gklinge@iu.edu    
#SBATCH --mail-type=BEGIN,END         
#SBATCH --mem=100G                    
#SBATCH -A r00638                     

# Load the necessary modules, if needed (e.g., GCC module)
# module load gcc

# Move to the directory from where you submitted the job
cd $SLURM_SUBMIT_DIR

# Compile the C++ program
g++ -o my_cpp_program Fuzz.cpp

# Run the compiled C++ program
srun ./Fuzz
