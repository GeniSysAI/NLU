# GeniSys NLU Engine
[![GeniSys NLU Engine](images/GeniSys.png)](https://github.com/GeniSysAI/NLU)

[![CURRENT RELEASE](https://img.shields.io/badge/CURRENT%20RELEASE-0.0.3-blue.svg)](https://github.com/GeniSysAI/NLU/tree/0.0.3)
[![UPCOMING RELEASE](https://img.shields.io/badge/UPCOMING%20RELEASE-0.0.4-blue.svg)](https://github.com/GeniSysAI/NLU/tree/0.0.4)

# About GeniSys AI

GeniSys AI is an open source Artificial Intelligence Assistant Network using Computer Vision, Natural Linguistics and the Internet of Things. GeniSys uses a system based on [TASS A.I](https://github.com/TASS-AI/TASS-Facenet "TASS A.I") for [vision](https://github.com/GeniSysAI/Vision "vision"), an [NLU engine](https://github.com/GeniSysAI/NLU "NLU engine") for natural language understanding, in browser speech synthesis and speech recognition for speech and hearing, all homed on a dedicated Linux server in your home and managed via a secure UI.

# About GeniSys NLU Engine

I orginally developed what is now the [GeniSys NLU Engine](https://github.com/GeniSysAI/NLU "GeniSys NLU Engine") back in 2017 ([How I built a fully functional Deep Learning Neural Network chatbot platform (NLU Engine) in under a week....](https://www.techbubble.info/blog/artificial-intelligence/chatbots/entry/deep-learning-neural-network-nlu-engine "How I built a fully functional Deep Learning Neural Network chatbot platform (NLU Engine) in under a week....")). The project was originally developed to take over **DialogFlow**, or what was known back then as **API.AI** in some commercial AI projects I had built, after I closed the business down it became a personal project for my home and as I have open sourced most of my other projects, it made sense to open source this one.

The NLU Engine includes a combination of a custom trained DNN (Deep Learning Neural Network) built using [TFLearn](http://tflearn.org/ "TFLearn") for intent classification, and a custom trained [MITIE](https://github.com/mit-nlp/MITIE "MITIE") model for entity classification. The engine can can handle not only named entities, but synonyms also and both features are used by the core training module.

# What Will We Do?

This tutorial will help you setup the NLU Engine required for your GeniSys network, and also takes you through setting up iotJumpWay devices. In detail this guide will cover the following:

- Installing and setting up required software
- Creating your intent and entity training data
- Training your intent and entity classifiers
- Testing your classifier locally in real time
- Testing your classifier API via a client

# Example Output

The following is an unedited conversation within the basic capabilities provided by the example training data (The full response print out has been removed to make it easy to follow the conversation):

```
>Hi how are you today?
2018-09-08 20:07:18|Human|Intent: Hi how are you today?
2018-09-08 20:07:18|GeniSys|STATUS: Processing
2018-09-08 20:07:18|GeniSys|Reponse: Hi, I am good thank you, how are you?
>I am very good thank you for asking
2018-09-08 20:07:29|Human|Intent: I am very good thank you for asking
2018-09-08 20:07:29|GeniSys|STATUS: Processing
2018-09-08 20:07:29|GeniSys|Reponse: Good, how can I help you?
>What would I call you if I were to speak to you?
2018-09-08 20:07:47|Human|Intent: What would I call you if I were to speak to you?
2018-09-08 20:07:47|GeniSys|STATUS: Processing
2018-09-08 20:07:47|GeniSys|Reponse: You can call me Geni (Jenny), but my real name is GeniSys
>thank you
2018-09-08 20:07:55|Human|Intent: thank you
2018-09-08 20:07:55|GeniSys|STATUS: Processing
2018-09-08 20:07:55|GeniSys|Reponse: My pleasure
>Would you happen to know what time it is ?
2018-09-08 20:08:13|Human|Intent: Would you happen to know what time it is ?
2018-09-08 20:08:13|GeniSys|STATUS: Processing
2018-09-08 20:08:13|GeniSys|Reponse: Right now it is Sat Sep  8 20:08:13 2018
>cool thank you
2018-09-08 20:08:24|Human|Intent: cool thank you
2018-09-08 20:08:24|GeniSys|STATUS: Processing
2018-09-08 20:08:24|GeniSys|Reponse: No problem!
```

In the conversation above, when I asked the time, the action attached to the related intent in the training data is triggered, basically an action is the path to a function in one of your custom classes, you can find out more about this later in the tutorial. Although none of the things I said were in the training data, the AI was capable of identifying my intent.

# Operating System

- Tested on [Ubuntu 18.04.1 LTS (Bionic Beaver)](http://releases.ubuntu.com/18.04/ "Ubuntu 18.04.1 LTS (Bionic Beaver)"), previous versions have been tested in Windows successfully but you need to make sure you install MITIE correctly on your Windows machine.

# Python Versions

- Tested with Python 3.5

# Software Requirements

- [Tensorflow 1.4.0](https://www.tensorflow.org/install "Tensorflow 1.4.0")
- [TFLearn](http://tflearn.org/ "TFLearn")
- [MITIE](https://github.com/mit-nlp/MITIE "MITIE")
- [NTLK (Natural Language Toolkit)](https://www.nltk.org/ "NTLK (Natural Language Toolkit)")
- [iotJumpWay MQTT Client](https://github.com/iotJumpway/JumpWayMQTT "iotJumpWay MQTT Client")

# Hardware Requirements

- 1 x Desktop device or laptop for development and training, prefereably with an NVIDIA GPU

# Installation & Setup

The following guides will give you the basics of setting up a GeniSys NLU Engine. 

## Clone The GeniSys NLU Engine Repo

First you need to clone the NLU Engine repo to the machine you will be running it on. To do so, navigate to the directory you want to place it in terminal and execute the following command:

```
 $ git clone https://github.com/GeniSysAI/NLU.git
```

Once you have done this, you have all the code you need on your machine. 

## Install The Required Software

Now you need to install the required software, I have provided a requirements file that will contain all required modules for the project. You can use it to install the modules using the following command: 

```
 $ sh setup.sh 
```

The command execute the setup shell file which will istall the required software for the project including **NTLK**, **TFLearn**, **MITIE** and **iotJumpWay**.

# Set Up iotJumpWay

Now you need to setup some an iotJumpWay device that will represent your NLU Engine on the Internet of Things. The following part of the tutorial will guide you through the process. 

- [Find out about the iotJumpWay](https://www.iotjumpway.tech/how-it-works "Find out about the iotJumpWay") 
- [Find out about the iotJumpWay Dev Program](https://www.iotjumpway.tech/developers/ "Find out about the iotJumpWay Dev Program") 
- [Get started with the iotJumpWay Dev Program](https://www.iotjumpway.tech/developers/getting-started "Get started with the iotJumpWay Dev Program") 

[![iotJumpWay](images/iotJumpWay-Device.jpg)](https://www.iotJumpWay.tech/console)

First of all you should [register your free iotJumpWay account](https://www.iotjumpway.tech/console/register "register your free iotJumpWay account"), all services provided by the iotJumpWay are also entirely free within fair limits. Once you have registered you need to:

- Create your iotJumpWay location [(Documentation)](https://www.iotjumpway.tech/developers/getting-started-locations "(Documentation)") 
- Create your iotJumpWay zones [(Documentation)](https://www.iotjumpway.tech/developers/getting-started-zones "(Documentation)")  
- Create your iotJumpWay devices [(Documentation)](https://www.iotjumpway.tech/developers/getting-started-devices "(Documentation)") 

Once you have set up your iotJumpWay device, you should update the [configuration file](https://github.com/GeniSysAI/NLU/blob/master/required/confs.json "configuration file")  with your iotJumpWay credentials. 

# Training Data

Now it is time to think about training data. In the [data/training.json](https://github.com/GeniSysAI/NLU/blob/master/data/training.json "data/training.json") file I have provided some starter data, it is not a lot but enough to have a good test and show the example further on in the tutorial. The example will show how you can attach actions to your intents in your training data which map to functions in your custum python classes, if you have seen the videos on my YouTube about the AI Ecommerce I made last year, a similar approach was uses in that system using DialogFlow. 

# Training Your NLU Engine

[![Training Your NLU Engine](images/train-confirmation.jpg)](https://github.com/GeniSysAI/NLU/blob/master/Train.py)

Now everything is set up, it is time to train. The main functionality for the training process can be found in [Train.py](https://github.com/GeniSysAI/NLU/blob/master/Train.py "Train.py"), [tools/Data.py](https://github.com/GeniSysAI/NLU/blob/master/tools/Data.py "tools/Data.py"), [tools/Model.py](https://github.com/GeniSysAI/NLU/blob/master/tools/Model.py "tools/Model.py") and  [tools/Mitie.py](https://github.com/GeniSysAI/NLU/blob/master/tools/Mitie.py "tools/Mitie.py"), the configuration for training can be found and modified in [required/confs.json](https://github.com/GeniSysAI/NLU/blob/master/required/confs.json "required/confs.json").

To begin training, make sure you are all set up, navigate to the root of the project and execute the following command:

```
 $ python3 run.py TRAIN
```

[![Training Your NLU Engine](images/train-results.jpg)](https://github.com/GeniSysAI/NLU/blob/master/Train.py)

# Communicating with your AI Locally

Now you have trained your AI, it is time to test her out! In this tutorial I will base my explanation on the conversation block at the beginning of this tutorial. 

As your AI is now trained, all you need to do (assuming you are in the project root), is execute the following code:

```
 $ python3 run.py INPUT  1 0.5
```

What this does is starts up a session using the user ID of 1 and a threshold of 0.5, sometimes if your model is misclassifying it can help to play with this threshold. 

[![Communicating with your AI](images/talk.jpg)](https://github.com/GeniSysAI/NLU/blob/master/run.py)

In the case of the example, the action (actions.NLUtime.getTime) converts the %%TIME%% value in a randomly chosen action response and replaces the original response. You can write your own functionality or link the response to other modules as you like, the limit is your imagination ;) 

```
"action":  {
    "function": "actions.NLUtime.getTime",
    "responses": [
        "The time is %%TIME%%",
        "Right now it is %%TIME%%",
        "It is around %%TIME%%"
    ]
}
```

Regarding the classifications in general, if you have looked through the example data, you may notice that none of the things that I said in the above script had been directly trained to the AI. For example, with the question **What would I call you if I were to speak to you?**, the actual training data provided to the AI related to this question is actually:

```
"text": [
    "What is your name",
    "Whats your name",
    "What do they call you",
    "What can I call you",
    "Who are you",
    "Tell me your name"
]
```

You can see that the example above was not in the training data, but the AI was still able to classify and respond correctly. 

# Joking With Your AI

Due to a rather good idea I had, ;) basic functionality exists for parsing AIML documents into a format suitable for training the NLU and adding it to the training data. Below is an example after training with a few jokes found in an AIML file provided by [Pandorabots]( https://github.com/pandorabots/Free-AIML/blob/master/jokes.aiml "Pandorabots"), this file actually turned out to be written by one of my friends, 4 time Loebner Prize winner for most human like AI, Steve Worswick.

```
2018-09-08 22:03:38|Inference|INFO: Inference Started In INPUT Mode
2018-09-08 22:03:38|Session|INFO: NLU Session Ready For User #1

>I bet you are not funny, can you tell me a joke?

2018-09-08 22:03:51|Human|Intent: I bet you are not funny, can you tell me a joke?
2018-09-08 22:03:51|GeniSys|STATUS: Processing

2018-09-08 22:03:51|GeniSys|Reponse: A man returns from an exotic holiday and is feeling very ill. He goes to see his doctor, and is immediately rushed to the hospital to undergo some tests. The man wakes up after the tests in a private room at the hospital, and the phone by his bed rings. 'This is your doctor. We have the results back from your tests and we have found you have an extremely nasty disease called M.A.D.S. It's a combination of Measles, AIDS, Diphtheria, and Shingles!'  'Oh my gosh', cried the man, 'What are you going to do, doctor?'  'Well we're going to put you on a diet of pizzas, pancakes, and pita bread.' replied the doctor.  'Will that cure me?' asked the man.  The doctor replied, 'Well no, but, it's the only food we can slide under the door.'

>Not bad, tell me another joke

2018-09-08 22:04:12|Human|Intent: Not bad, tell me another joke
2018-09-08 22:04:12|GeniSys|STATUS: Processing

2018-09-08 22:04:12|GeniSys|Reponse: A doctor thoroughly examined his patient and said, 'Look I really can't find any reason for this mysterious affliction. It's probably due to drinking.' The patient sighed and snapped, 'In that case, I'll come back when you're damn well sober!'

>Alcohol jokes are always funny! You can tell me another joke

2018-09-08 22:04:40|Human|Intent: Alcohol jokes are always funny! You can tell me another joke
2018-09-08 22:04:40|GeniSys|STATUS: Processing

2018-09-08 22:04:40|GeniSys|Reponse: Man: Doctor, I've just swallowed a pillow. Doctor: How do you feel? Man: A little down in the mouth.

>Haha
```

# Communicating with your AI Via The Internet

In version 0.0.2, the functionality was added to enable accessing the NLU via a secure API endpoint. To start your NLU engine in server mode, you can enter the following commands into terminal:

```
 $ python3 run.py SERVER 0.5
```

This starts the server up and sets a threshold for classifications of 0.5. 

If you used the provided [NGINX configuration](https://github.com/GeniSysAI/Server/blob/master/etc/nginx/sites-available/default "NGINX configuration") of the [GeniSys Server](https://github.com/GeniSysAI/Server/ "GeniSys Server") guide,

```
server_name Subdomain.Domain.TLD;

location ~ ^/communicate/ {
    proxy_pass http://###.###.#.###:5824/$uri$is_args$args;
}
```

you will now be able to access your NLU by posting to http://www.YourDomain.com/communicate/infer/USERID, to do this, I provided an an API client programmed in Python which takes your input from console and sends it to the server for processing: [GeniSys API Client](https://github.com/GeniSysAI/NLU/blob/master/client.py "GeniSys API Client").

Navigate to the project root and execute the following command to send a query to your NLU engine, you can use any question or statement, but bear in mind it must be within the boundaries of variations of the training date.

```
 $ python3 client.py CLASSIFY 1 "Do you know what I am saying?"
```

In other GeniSys AI tutorials, you will build applications and use the UI to train and manage the engine.

# Interacting With TASS Computer Vision

The core and remote computer vision systems used by GeniSys are based on [TASS AI](https://www.tassai.tech "TASS AI"), if you have set up your [GeniSys AI Server](https://github.com/GeniSysAI/Server "GeniSys AI Server") and granted camera permissions to the UI, you will be able to see your self on the new dashboard. You can communicate with the NLU engine via the chat window to the right of the camera stream.

A new feature recently added to the upcoming 0.0.3 release is the ability for you to ask the AI who you are. This feature uses a combination of the iotJumpWay TASS REST API, the local server camera and TASS to determine who it saw in the last 10 seconds. 

[![Interacting With TASS Computer Vision](images/computer-vision.jpg)](https://github.com/GeniSysAI/Vision)

Each time a TASS device detects a known human or an intruder it updates the iotJumpWay enabling you to keep track as they move around the house, this allows the network to know where people at any one time as long as there are TASS units set up in each room. 

Using an action, the system will contact the iotJumpWay securely and retrieve any and all people it saw in the last five seconds. If it has not seen any one it will ask the user to look at the camera. 

These features are the first steps towards a system wide user management system which will include emotional analysis and a number of other features.

# Stay Tuned!!

There are more features from my original version that are still yet to be implemented plus some other cool features, pluse the combined system of all three GeniSys AI repos.

# Contributing
Please read [CONTRIBUTING.md](https://github.com/GeniSysAI/NLU/blob/master/CONTRIBUTING.md "CONTRIBUTING.md") for details on our code of conduct, and the process for submitting pull requests to us.

# Versioning
We use SemVer for versioning. For the versions available, see the tags on this repository and [RELEASES.md](https://github.com/GeniSysAI/NLU/blob/master/RELEASES.md "RELEASES.md").

# License
This project is licensed under the **MIT License** - see the [LICENSE](https://github.com/GeniSysAI/NLU/blob/master/LICENSE "LICENSE") file for details.

# Bugs/Issues
We use the [repo issues](https://github.com/GeniSysAI/NLU/issues "repo issues") to track bugs and general requests related to using this project. 

# Author
[![Adam Milton-Barker: BigFinte IoT Network Engineer & Intel® Software Innovator (IoT, AI, VR)](images/Adam-Milton-Barker.jpg)](https://github.com/AdamMiltonBarker)