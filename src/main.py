import os
import time

from read_config import load_config
from query_SRA_for_size import generate_SRR_size_df
from balance_nodes import balance_nodes
from build_submit_file import populate_submit_file


def main():
    """
    This program orchestrates a distributed computing workflow for downloading and processing SRA (Sequence Read Archive) data.
    It consists of several key components:

    1. Configuration Management (read_config):
       - Reads JSON configuration specifying dates, queries, and processing parameters

    2. SRA Query Generation (generate_SRR_size_df):
       - Builds query to search SRA database based on date ranges and keywords
       - Returns dataframe of SRR accessions and file sizes

    3. Node Balancing (balance_nodes):
       - Distributes SRA downloads across compute nodes based on file sizes
       - Optimizes CPU and disk allocation
       - Generates node-specific SRA lists

    4. HTCondor Submit Generation (populate_submit_file):
       - Creates HTCondor submit file with computed resource requirements
       - Configures file transfer and execution parameters

    The workflow enables efficient parallel processing of SRA data by:
    - Querying recent submissions within specified date ranges
    - Load balancing based on file sizes
    - Generating optimal HTCondor configurations
    - Managing resource allocation across compute nodes

    Required configs are specified in config.json including:
    - Date ranges for SRA queries
    - Search keywords
    - Process configurations (CPUs, memory, etc)
    - Directory paths
    - Minimum submission thresholds
    """
    program_start_time = time.time()

    config = load_config("config.json")

    # Make the output directory on chtc that will hold our processed files
    if config["process_configs"]["on_chtc"]:

        print("On chtc")

        # Will throw an error if dir already exists
        os.makedirs(config["directory"]["output_results"], exist_ok=False)

    else:
        print("Not on chtc")

    srr_with_size = generate_SRR_size_df(config)

    submit_configs = balance_nodes(srr_with_size, config)

    populate_submit_file(submit_configs)

    end_time = time.time()
    ex_time = end_time-program_start_time
    print(f"\n\nTotal Time of program: {ex_time}")

if __name__ == "__main__":
    main()