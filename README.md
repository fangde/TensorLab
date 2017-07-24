# TensorLab
Cloud Machine Learning Platform based on TensorLayer

a video introduction at ICAI 2017 is at 


## Why TensorLab

In his NIPS 2016 talk, Andrew Ng mentioned that all the AI research group should be equipped with some data warehouse technology.   
TensorLab started during the process of developing the TensorLayer system, with a focus on data managment aspect of AI development. The original motivation is Prof Yike Guo’s vision that democratise the deep learning technology the engineering and scientiests who are domain expert but not necessary deep learning gurus.
TensorLayer project created by Dr Hao Dong is great success which greatly simplify developing machine learning model. 
However, according to our experience, we still find researchers struggling mastering the deep learning technology, the management of models and data is becoming another big hurdles facing many deep learning learning.  
TensorLab is started with the vision to build an autonmous system to streamline the whole model development process. 
More specifically, we are targeting at the following questions.


1. How to manage training data. Deep learning sometime requires GB, TB or PB data, the first challenge is finding the training data from the enterpertise dataware house

2.  How to load the training data which is 100 times bigger than the computer node hard-drive

3. Model Managment, which includes model version, model mining and monitoring the training process of a fleet of models, like 100

4. How to streamline the whole process of training, validating and deployment

## TensorLab Architecture

TensorLab is designed as an pipeline system for machine learning development based on the big data technology. 
The lower layer is an data fusion management developed for machine learning application, which orginally named TensorDB. 
On the upper layer is an software framework with easy to use interface for many machine learning applications, which we called TensorCloudAPI. 
In the beginning, the development of TensorDB focusing on Database infrastructure to for machine learning pipeline. 
However, in recent development, we start to working on decouple the TensorLab system from the  the in house infrastructure at Data Science Institute (DSI), making the TensorLab system more like a middle ware. 
At the moment, TensorLab is aims to support both the DSI cloud computing infracture and also public cloud service such as google cloud platform (GCP). Support for other cloud providers will be added later

TensorLab is designed following three principle

1. Everything is Data
2. Everything is specified by Database Query
3. Lazy loading via stream  processing

