FROM tensorlayer/tensorlayer:latest-cpu-py2

RUN apt-get update -y
RUN apt-get install git -y
RUN apt-get install python-tk -y
RUN git clone https://github.com/fangde/TensorLab.git
RUN pip install -e TensorLab

WORKDIR /root/TensorLab-master/examples
