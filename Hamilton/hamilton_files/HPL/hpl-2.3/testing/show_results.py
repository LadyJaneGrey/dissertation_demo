

# pylint: disable=trailing-whitespace
from pprint import pprint
import pandas as pd
import os


RESULT_DELIMETER = "T/V                N    NB     P     Q               Time                 Gflops"

def get_parameter_grid(data): 
    
    start = None
    for i, value in enumerate(data):  
        if "The following parameter values will be used:" in value: 
            start = i 
    
    parameter_grid = { }

    for i, line in enumerate(data[start::]): 
        line = line.strip()
        if "----------------" in line: 
            break 
        else: 
            if line != "": 
                # value.split(":")
                value = line.split(":")

                key = value[0].strip()
                value = value[1].strip()
                parameter_grid[key] = value
            
    return parameter_grid
            


def parse_data(data): 
    results = []
    for i, line in enumerate(data): 
        if RESULT_DELIMETER in line: 
            value = data[i+2]
            value = value.split()
            results.append(
                {"N": value[1], 
                "NB": value[2], 
                "P": value[3],
                "Q": value[4],
                "Time": value[5], 
                "Gflops": value[6],})
            
    return results


def main(file_name): 
    # command = "make logbruh"
    # data = os.popen(command).readlines()
    
    data = None
    with open(file_name, "r") as file: 
        data = file.readlines()

    parameter_grid = get_parameter_grid(data)        
    data = parse_data(data)
    # pprint(parameter_grid)
    df = pd.DataFrame(data)
    # pprint(df)
    df["Time"] = df["Time"].astype(float)
    # df["Gflops"] = df["Gflops"].astype(float)
    print(df.sort_values(by=["Time"], ascending=[True]).iloc[:1])



def list_all(): 
    dir_name = "22-03-23-results"
    
    for file_name in os.listdir(dir_name):
        if "meta" not in file_name:
            print(file_name)
            main(f"{dir_name}/{file_name}")





if __name__ == "__main__":
    list_all()





