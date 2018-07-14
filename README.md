# TensorLab
Cloud Machine Learning Platform based on TensorLayer

a video introduction at ICAI 2017 is at 


A documentation is at
https://paper.dropbox.com/doc/TensorLab-Autonomous-Deep-Learning-in-the-Cloud-sj2x90c3ZvaFJlpSH7QMH


## Introduction
TensorDB is a data managment platform for machine learning. TensorDB try to use big data to managagment the life cycle of machine learning model development, which is in prinicple similar to the mlflow system recently open sourced by databricks.

TensorDB native supports the TensorLayer, and using MongoDB as the storage backend. We test it for distributed training and also the async reinforcement learning.

It is under active develoment, we are now adding the backend, that support google storage, s3, dynamodb, datastore and  tablestore for public cloud provides like aws, azure, google cloud, and aliyun.




## Try It
there is a mnist example, containerized in docker, which has a docker for mongodb and also a docker for a tensordb training worker.
you can simply run it via the 
example/start.sh

then inside the docker 
type

python seed.py
python mnistdemo.py


It is highly recommand you use a gui client for mongodb to monitor the training, you can try the studio3T(https://studio3t.com/) and connecto the mongodb servier via ip:27019



