def create_hpl_file(N, PQ, NB): 
    
    
    pstring = []
    qstring = []
    print(PQ)
    for p,q in PQ: 
        pstring.append(p)
        qstring.append(q)

    print(pstring)
    print(qstring)
    pstring = "\t".join([str(value) for value in pstring])
    qstring = "\t".join([str(value) for value in qstring])

    stringNB = "\t".join([str(value) for value in NB])
    
    NString = "\t".join([str(value) for value in N])

    sample_files = f"""HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any) 
6            device out (6=stdout,7=stderr,file)
{len(N)}            # of problems sizes (N)
{NString}         Ns
{len(NB)}            # of NBs
{stringNB}           NBs
0            PMAP process mapping (0=Row-,1=Column-major)
{len(PQ)}            # of process grids (P x Q)
{pstring}            Ps
{qstring}            Qs
16.0         threshold
1            # of panel fact
2            PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
4            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1            RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
1            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
1            DEPTHs (>=0)
2            SWAP (0=bin-exch,1=long,2=mix)
64           swapping threshold
0            L1 in (0=transposed,1=no-transposed) form
0            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)"""

    with open("HPL.dat", "w") as file: 
        file.writelines(sample_files)

    print("Files Created")



def create_mpi_yaml_files(mpi_processes, num_nodes, cpus_per_worker, memory_per_worker): 



    mpi_template = f"""apiVersion: kubeflow.org/v2beta1
kind: MPIJob
metadata:
  name: hpl-mpi
spec:
  slotsPerWorker: {cpus_per_worker}
  runPolicy:
    cleanPodPolicy: Running
  mpiReplicaSpecs:
    Launcher:
      replicas: 1
      template:
        spec:
          containers:
          - image: ghcr.io/crambor/hpl:v0.2.1
            env:
              - name: OMP_NUM_THREADS
                value: "1"
              - name: OMP_PROC_BIND
                value: "TRUE"
              - name: OMP_PLACES
                value: "cores"


            name: hpl
            command:
            - mpirun
            args:
            - --allow-run-as-root
            - --bind-to-core
            - -np
            - "{mpi_processes}"
            - ./xhpl

    Worker:
      replicas: {num_nodes}
      template:
        spec:
          containers:
          - image: ghcr.io/crambor/hpl:v0.2.1
            name: hpl
            volumeMounts:
            - name: "config"
              mountPath: "/home/mpiuser/hpl/testing/HPL.dat"
              subPath: "HPL.dat"
    
            resources:
              requests:
                cpu: {cpus_per_worker}
              limits:
                cpu: {cpus_per_worker}
                memory: {memory_per_worker}Gi

          volumes:
          - name: "config"
            configMap:
              name: "config"
"""
    with open("hpl-mpi.yaml", "w") as file: 
        file.writelines(mpi_template)

