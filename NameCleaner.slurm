#!/bin/bash
#SBATCH -J namecleaning
#SBATCH -p general
#SBATCH -o python%j.txt
#SBATCH -e python_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=8:00:00
#SBATCH --mail-user=gklinge@iu.edu
#SBATCH --mail-type=BEGIN,END
#SBATCH --mem 100G
#SBATCH -A r00638
#SBATCH --array=1-6

# Load Python module
module load python

# Create and activate the virtual environment
python -m venv ~/myenv
source ~/myenv/bin/activate

#Remember that the column number is 0-indexed, so column A is 0, B is 1, etc.

# Define file paths and column numbers for each job in the array
case "$SLURM_ARRAY_TASK_ID" in
    1)
        INPUT_FILE="/N/u/gklinge/Quartz/assignees_dirty_all.csv"
        OUTPUT_FILE="/N/u/gklinge/Quartz/cleaned_assignee_all.csv"
        COLUMN_TO_READ=1  # Assuming 'assignee' is the column to clean
        COLUMN_TO_COPY_TO=3
        ;;
    2)
        INPUT_FILE="/N/u/gklinge/Quartz/assignees_unique_dirty.csv"
        OUTPUT_FILE="/N/u/gklinge/Quartz/cleaned_assignee_all_unique.csv"
        COLUMN_TO_READ=1
        COLUMN_TO_COPY_TO=3
        ;;
    3)
        INPUT_FILE="/N/u/gklinge/Quartz/capitaliq_cusip_dirty.csv"
        OUTPUT_FILE="/N/u/gklinge/Quartz/cleaned_capitalcusip.csv"
        COLUMN_TO_READ=1  # Assuming 'company name' is the column to clean
        COLUMN_TO_COPY_TO=2
        ;;
    4)
        INPUT_FILE="/N/u/gklinge/Quartz/crsp_permco_dirty.csv"
        OUTPUT_FILE="/N/u/gklinge/Quartz/cleaned_csrp_permco.csv"
        COLUMN_TO_READ=0
        COLUMN_TO_COPY_TO=2
        ;;
    5)
        INPUT_FILE="/N/u/gklinge/Quartz/gvkey_dirty.csv"
        OUTPUT_FILE="/N/u/gklinge/Quartz/cleaned_gvkey.csv"
        COLUMN_TO_READ=1
        COLUMN_TO_COPY_TO=2
        ;;
    6)
        INPUT_FILE="/N/u/gklinge/Quartz/sec_cik_dirty.csv"
        OUTPUT_FILE="/N/u/gklinge/Quartz/cleaned_SEC_CIK.csv"
        COLUMN_TO_READ=1
        COLUMN_TO_COPY_TO=2
        ;;
esac

# Move to the directory from where you submitted the job
cd $SLURM_SUBMIT_DIR

# Run the Python program with the specified arguments
srun python Name_Cleaner.py "$INPUT_FILE" "$OUTPUT_FILE" "$COLUMN_TO_READ" "$COLUMN_TO_COPY_TO"
