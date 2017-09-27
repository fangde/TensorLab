FROM ubuntu
RUN apt-get update
RUN apt-get install wget  bzip2 git unzip build-essential -y
RUN wget https://repo.continuum.io/archive/Anaconda2-5.0.0-Linux-x86_64.sh
RUN bash Anaconda*.sh -b
ENV PATH "$PATH:/root/anaconda2/bin"


RUN pip install tensorflow
RUN pip install git+https://github.com/zsdonghao/tensorlayer.git


RUN conda install lz4 -y
RUN pip install pymongo
RUN pip install graphene

RUN pip install dash==0.18.3  # The core dash backend
RUN pip install dash-renderer==0.10.0  # The dash front-end
RUN pip install dash-html-components==0.7.0  # HTML components
RUN pip install dash-core-components==0.12.6  # Supercharged components
RUN pip install plotly --upgrade  # Latest Plotly graphing library




ADD https://github.com/fangde/TensorLab/archive/master.zip /root/
WORKDIR /root
RUN unzip /root/master.zip
WORKDIR /root/TensorLab-master/examples
