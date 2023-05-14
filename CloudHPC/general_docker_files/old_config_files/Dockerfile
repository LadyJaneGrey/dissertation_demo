
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
    tar zxf NPB3.4.2.tar.gz


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

FROM mpioperator/openmpi:0.3.0

# # include dependencies
RUN apt update && apt install -y \
    wget \
    build-essential \
    gcc \
    # libopenblas-dev 
    libopenblas-dev \
    libopenmpi-dev


COPY --from=builder /hpl /home/mpiuser/hpl
COPY --from=builder /hpcg /home/mpiuser/hpcg
COPY --from=builder /NPB3.4.2.tar.gz /home/mpiuser/NPB3.4.2.tar.gz

WORKDIR "/home/mpiuser/hpl/testing"

COPY HPL.dat .


CMD ["/bin/bash"]

