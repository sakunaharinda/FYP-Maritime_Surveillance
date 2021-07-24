# OBJECT DETECTION, TRACKING AND SUSPICIOUSACTIVITY RECOGNITION FOR MARITIME SURVEILLANCEUSING THERMAL VISION

## Introduction

Widespread, constant monitoring during both day and night by the naval security personnel is required to ensure that activities such as the transport of banned substances, unlawful fishing, and human trafficking are prevented. This is a human labor-intensive and monotonous task. Due to the difficult conditions at sea and the repetitive nature of the task, human error could also lead to significant lapses in security.
Therefore, the automation of this task is desirable. Through this project, we seek to automate the task of object detection, tracking, and suspicious activity detection. 
To detect objects in the maritime environment during the day and the night, we capture a live feed using a thermal camera. 
The images are fed in real-time to an object detection algorithm to detect and localize the objects of interest such as ships, boats, unidentified floating objects, humans, etc. 
We then track the detected objects over time and identify if suspicious activities are occurring based on the detected and tracked objects. 
We log and display all detected objects and actions on the user interface developed for this project. 

Thermal imaging is regularly used by naval vessels to monitor and detect objects both in the day and the night. Moving vessels and humans both give off a thermal signature that is easily detectable, especially at night. Thermal imaging is also used in a variety of other applications such as autonomous vehicles, and night-vision in combat situations. As being able to detect objects at night, when most illegal activities take place is of utmost importance, we choose to use thermal imaging to monitor the environment. 

Object detection is the identification and spatial localization of a set of predefined objects in a static image. It is used for a wide variety of applications such as autonomous vehicles, security, and traffic control. In the recent past, deep learning algorithms based on convolutional neural networks (CNN) have shown promising object detection results and has become the preferred method to carry out object detection. For our project, we adapt recent object detectors for the task of object detection. 

Object tracking is important in video analysis to monitor the path and the identity of objects. A variety of image processing algorithms and deep learning algorithms have been developed for this purpose, which we evaluate and adapt for our project. 

Activity detection is a recent area of interest in the academic community with the emergence of deep learning algorithms which are able to process video data. Activity detection is the identification and localization in both time and space of a set of predefined activities occurring in a video. This is an extremely challenging task, especially to carry out in real-time. However, with recent advances in computational capacity and deep learning algorithms, activity detection performance has significantly improved. For our project, we define and detect a set of suspicious activities, such as illegal fishing, human trafficking, etc.

The major barrier to the development of deep learning solutions to a variety of problems, including ours, is the need to collect a sufficient volume of data to train the deep learning algorithms. Specifically, for our problem, a thermal maritime activity detection dataset is required for the training and evaluation of our methods. We attempt to collect some such usable data for this purpose for our project. 

Finally, we developed a user-friendly interface for easy use of our application. As an automated surveillance system is primarily used by the security personnel on board the naval monitoring vessels, simplicity, and usability were of utmost importance in the development of our user interface. 

## Project Setup

### Dataset 

* Singapore Maritime Dataset - Link : [SMD](https://sites.google.com/site/dilipprasad/home/singapore-maritime-dataset) 
* FLIR Thermal Dataset - Link : [FLIR](https://www.flir.com/oem/adas/adas-dataset-form/)

To split the SMD, follow this [repo](https://github.com/tilemmpon/Singapore-Maritime-Dataset-Trained-Deep-Learning-Models) to take an idea.

### Object Detector

We use the CenterNet as our object detector introduced in this [paper](https://arxiv.org/abs/1904.07850 ).

To setup, train and test the object detector, use the instructions mentioned in their official [repository](https://github.com/xingyizhou/CenterNet).

If you face an error regarding DCNv2, follow the instructions below.

1. **Build NMS**

```
cd CenterNet\src\lib\external
#python setup.py install
python setup.py build_ext --inplace
```

Just comment the parameter in setup.py when building `nms` extension to solve invalid numeric argument `/Wno-cpp` :

`
#extra_compile_args=["-Wno-cpp", "-Wno-unused-function"]
`

2. **Clone and build original DCN2**

```
cd CenterNet\src\lib\models\networks
rm -rf DCNv2
git clone https://github.com/CharlesShang/DCNv2
cd DCNv2

vim cuda/dcn_va_cuda.cu
"""
# extern THCState *state;
THCState *state = at::globalContext().lazyInitCUDA();
"""

python setup.py build develop

```

### Demo

1. Follow the steps to setup CenterNet repository. [Change the repo name to `Centre_SMD` to avoid errors and confusion.]
2. Update the files in `CenterNet/src` with the provided files in `Center_SMD/src`
3. Follow the steps below.
```
cd Center_SMD/
mkdir -p exp/flir/dla_34/rgb/coco_dla
mkdir -p exp/smd/dla_34/rgb/smd_split1
```

4. Download the relevant checkpoints from the [google drive](https://drive.google.com/drive/folders/1QqPEGYg_mI7EMQypvQuzvi8myc1vy2YM?usp=sharing) and place it under the folders created before. 

5. Start the UI.

```
cd UI/
python app.py
```

If everything works perfectly, you will see an interface as follows.

![UI](https://github.com/sakunaharinda/FYP-Maritime_Surveillance/blob/main/Capture.PNG)


**Thank you !!**


