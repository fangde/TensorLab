FROM tensorlayer/tensorlayer:latest-cpu-py2

RUN apt-get update -y
RUN apt-get install git -y

WORKDIR /root
RUN git clone https://github.com/fangde/TensorLab
WORKDIR /root/TensorLab-master/examples
