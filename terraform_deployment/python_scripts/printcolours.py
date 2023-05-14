
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def printgreen(command=None): 
    print(f"\033[92m{command}\033[0m")

def printred(command=None): 
    print(f"\033[91m{command}\033[0m")