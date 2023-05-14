import subprocess
import os
from printcolours import *
import time 


def run_command(command): 
    print("Starting Cluster")
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, b''):
        print(line.decode().strip())

    process.wait()

def static_command(command): 
    output = []  # Initialize an empty list to store the output lines

    print("Starting Cluster")
    print(command)

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    for line in iter(process.stdout.readline, b''):
        line = line.decode().strip()
        output.append(line)  # Append each output line to the list

    process.wait()

    return output




def start_cluster(num_nodes = 1): 
    # set kubectl config: 
    os.chdir("../terraform_scripts")

    # -var="region=us-west-2"

    command = f'terraform apply -auto-approve -var="numNodes={num_nodes}"'    
    run_command(command)
    print("Waiting...")
    time.sleep(10)
    run_command("gcloud container clusters get-credentials ron-tf-gke-cluster --region=us-central1")
    run_command("gcloud config set container/cluster ron-tf-gke-cluster")
    run_command("kubectl config set-cluster ron-tf-gke-cluster")

    run_command("kubectl apply -f /home/rohanjain_durham/rohan-jain/mpi-operator/deploy/v2beta1/mpi-operator.yaml")


def destroy_cluster(): 
    os.chdir("../python_scripts")

    print("Destroying Cluster")
    command = f'terraform destroy -auto-approve -var="numNodes=0"'    
    
    run_command(command)

def run_benchmark(): 
    print("Running Benchmarks")
    # Setup configs and deploy mpi-operator

    
    os.chdir("../python_scripts")

    run_command("make delete")
    print("Waiting for deletion process")
    time.sleep(10)
    run_command("make all")

    printgreen("All commands ran sucesfully")
    

def check_benchmarks(): 
    # get all pods and check if completed, if completed log outputs return 
    os.chdir("../python_scripts")
    while True: 
        command = "kubectl get pods"
        output = []  # Initialize an empty list to store the output lines
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        for line in iter(process.stdout.readline, b''):
            line = line.decode().strip()
            output.append(line)  # Append each output line to the list
        process.wait()

        print("\n".join(output))

        if "Completed" in "\n".join(output): 
            printgreen("Tasks completed, saving files to configs")
            contents = static_command("make logbruh")
            print(contents)
            contents = "\n".join(contents)


            with open("/home/rohanjain_durham/deliverables_submitted/python_scripts/hpl-mpi.yaml", "r") as file:
                # contents += "\n".join(file.readlines())
                contents += "".join(file.readlines())
            
            with open("/home/rohanjain_durham/deliverables_submitted/python_scripts/HPL.dat", "r") as file:
                # contents += "\n".join(file.readlines())
                contents += "".join(file.readlines())
                



            file_name = f"hpl_benchmark_contents{time.time()}.txt" 
            print(file_name)
            with open(f"/home/rohanjain_durham/deliverables_submitted/backup_results/{file_name}", "w") as file: 
                file.write(contents)


            break 
        time.sleep(10)

def main(num_nodes):
    start_cluster(num_nodes)
    
    
    run_benchmark()
    check_benchmarks()
    
    # destroy_cluster()
    