import pandas as pd 
import os 
import subprocess
import hpl_file_generator
import terraform_deploy_scripts
import time
# def get_configs_to_run(): 
#     delimeter = "|"
    
#     df = pd.read_csv("/home/rohanjain_durham/deliverables_submitted/python_scripts/config_files.csv")
#     print("Starting Benchmarks")
#     print(df)
#     for index, row in df.iterrows():
#         problemnsize = row["problemnsize"].split(delimeter)
#         NB_configs = row["NB_configs"].split(delimeter)
#         pqgrids = row["processgrids(pq)"].split(delimeter)
        
#         problemnsize = [int(value.strip()) for value in problemnsize]
        
#         hpl_file_generator.create_hpl_file(
#             N = problemnsize,

#             PQ = pqgrids,
#             NB = NB_configs,
#         )
#         # ------
#     print("All Benchmarks Ran")



def generate_config_files(
    mpi_processes,  # -np param
    num_nodes, # number of replicas to do 
    problem_size, 
    pqgrids, 
    NB_configs, 
    memory_per_worker = 10,  # default value as well 
    cpus_per_worker = 3, # likely default value
): 

    # generate hpl_file configurations
    hpl_file_generator.create_hpl_file(N=problem_size, PQ = pqgrids, NB = NB_configs)
    hpl_file_generator.create_mpi_yaml_files(mpi_processes, num_nodes, cpus_per_worker, memory_per_worker)

    



if __name__ == "__main__": 


    # terraform_deploy_scripts.destroy_cluster()
# 
    # time.sleep(60)

    memory_per_worker = 10
    cpus_per_worker = 3,

    configs_to_run = [
        {
            "mpi_processes": 3, 
            "num_nodes": 1,
            "problem_size": [10000], 
            "pqgrids": [(1,3)], 
            "NB_configs" : [192,222]

        },
       
        {
            "mpi_processes": 6, 
            "num_nodes": 2,
            "problem_size": [10000], 
            "pqgrids": [(2,3)], 
            "NB_configs" : [192,222]

        },
        {
            "mpi_processes": 12, 
            "num_nodes": 4,
            "problem_size": [10000], 
            "pqgrids": [(3,4)], 
            "NB_configs" : [192,222]

        }
    ]





    for config in configs_to_run: 
        mpi_processes = config["mpi_processes"]
        num_nodes = config["num_nodes"]
        problem_size = config["problem_size"]
        pqgrids = config["pqgrids"]
        NB_configs = config["NB_configs"]


        generate_config_files(
            mpi_processes = mpi_processes,
            num_nodes = num_nodes,
            problem_size = problem_size,
            pqgrids = pqgrids,
            NB_configs = NB_configs,
        )

        terraform_deploy_scripts.main(num_nodes)
        terraform_deploy_scripts.destroy_cluster()

    