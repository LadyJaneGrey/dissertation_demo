
FROM mpioperator/openmpi-builder:0.3.0 as builder


# set contextual labels

# include dependencies
RUN apt update && apt install -y \
    wget \
    build-essential \
    gcc \
    # libopenblas-dev 
    libopenblas-dev \
    libopenmpi-dev


# download HPL and HPCG
RUN wget https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz && \
    tar -xzf hpl-2.3.tar.gz && \
    mv hpl-2.3 hpl && \
    wget http://www.hpcg-benchmark.org/downloads/hpcg-3.0.tar.gz && \
    tar -xzf hpcg-3.0.tar.gz &&  \
    mv hpcg-3.0 hpcg && \
    wget https://www.nas.nasa.gov/assets/npb/NPB3.4.2.tar.gz && \
    tar zxf NPB3.4.2.tar.gz && \
    mv NPB3.4.2 NPB


# compile HPL
WORKDIR "hpl"

COPY "Make.Linux_Intel64" .
RUN ./configure && make arch=intel64 -j$(nproc)


## ------ Configuring HPCG 

WORKDIR "../hpcg/setup"
RUN cp Make.Linux_MPI Make.linuxmpi

WORKDIR "../"
RUN mkdir build

WORKDIR "build"
RUN ../configure linuxmpi && make

WORKDIR "bin"
COPY hpcg.dat .

WORKDIR "../../../NPB/NPB3.4-MPI/config"
COPY NAS_benchmark_files/make.def make.def
WORKDIR "../"
# RUN for benchmark in EP IS CG MG FT BT SP LU; do     make $benchmark CLASS=S;     if [ $? -ne 0 ]; then         echo -e "\033[31mError building $benchmark. Exiting loop.\033[0m";         break;     fi; done
# RUN make EP CLASS=S
# RUN make CG CLASS=S


FROM mpioperator/openmpi:0.3.0

# # include dependencies
RUN apt update && apt install -y \
    wget \
    build-essential \
    gcc \
    # libopenblas-dev 
    libopenblas-dev \
    libopenmpi-dev


# Install OpenSSH for MPI to communicate between containers
RUN apt-get install -y --no-install-recommends openssh-client openssh-server && \
    mkdir -p /var/run/sshd

# Allow OpenSSH to talk to containers without asking for confirmation
# by disabling StrictHostKeyChecking.
# mpi-operator mounts the .ssh folder from a Secret. For that to work, we need
# to disable UserKnownHostsFile to avoid write permissions.
# Disabling StrictModes avoids directory and files read permission checks.
RUN sed -i 's/[ #]\(.*StrictHostKeyChecking \).*/ \1no/g' /etc/ssh/ssh_config && \
    echo "    UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config && \
    sed -i 's/#\(StrictModes \).*/\1no/g' /etc/ssh/sshd_config



COPY --from=builder /hpl /home/mpiuser/hpl
COPY --from=builder /hpcg /home/mpiuser/hpcg
COPY --from=builder /NPB /home/mpiuser/NPB

WORKDIR "/home/mpiuser/hpl/testing"

COPY HPL.dat .

# WORKDIR "../../NPB/NPB3.4-MPI"

# RUN for benchmark in EP IS CG MG FT BT SP LU; do     make $benchmark CLASS=S;     if [ $? -ne 0 ]; then         echo -e "\033[31mError building $benchmark. Exiting loop.\033[0m";         break;     fi; done

WORKDIR "/home/mpiuser/NPB/NPB3.4-MPI"



RUN make EP CLASS=S; \
    make IS CLASS=S; \
    make CG CLASS=S; \
    make MG CLASS=S; \
    make FT CLASS=S; \
    make BT CLASS=S; \
    make SP CLASS=S; \
    make LU CLASS=S;

WORKDIR "/home/mpiuser"
CMD ["/bin/bash"]

# cd NPB/NPB3.4-MPI/ && make EP CLASS=S && cd bin && mpirun -np 1 --allow-run-as-root ./ep.S.x §