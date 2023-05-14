

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


def main(): 
    command = "make logbruh"
    data = os.popen(command).readlines()
    
    # parameter_grid = get_parameter_grid(data)        
    data = parse_data(data)
    # pprint(parameter_grid)
    df = pd.DataFrame(data, columns=["N","NB","P","Q","Time","Gflops"])
    # pprint(df)
    df["Time"] = df["Time"].astype(float)
    df["P"] = df["P"].astype(int)
    df["Q"] = df["Q"].astype(int)
    df["PQ"] = df["P"] * df["Q"]
    df["Time/mins"] = round(df["Time"]/60,2)
    # df["Gflops"] = df["Gflops"].astype(float)

    df = df[["N","NB","P","Q","PQ","Time","Time/mins","Gflops"]]

    print(df.sort_values(by=["Time"], ascending=[True]))



if __name__ == "__main__":
    main()




