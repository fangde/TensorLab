FROM tensorlayer/tensorlayer:latest-cpu-py2

RUN apt-get update -y
RUN apt-get install git -y
RUN apt-get install python-tk -y
WORKDIR /root
RUN git clone https://github.com/fangde/TensorLab.git
WORKDIR /root/TensorLab
RUN  pip install -e .
WORKDIR /root/TensorLab/examples
ENTRYPOINT [ "/bin/bash" ]

