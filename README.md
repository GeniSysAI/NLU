# GeniSys NLU Engine
[![GeniSys NLU Engine](images/GeniSys.png)](https://github.com/GeniSysAI/NLU)

[![CURRENT RELEASE](https://img.shields.io/badge/CURRENT%20RELEASE-0.0.4-blue.svg)](https://github.com/GeniSysAI/NLU/tree/0.0.4)
[![UPCOMING RELEASE](https://img.shields.io/badge/UPCOMING%20RELEASE-0.0.5-blue.svg)](https://github.com/GeniSysAI/NLU/tree/0.0.5)

# About GeniSys AI

GeniSys AI is an open source Artificial Intelligence Assistant Network using Computer Vision, Natural Linguistics and the Internet of Things. GeniSys uses a system based on [TASS A.I](https://github.com/TASS-AI/TASS-Facenet "TASS A.I") for [vision](https://github.com/GeniSysAI/Vision "vision"), an [NLU engine](https://github.com/GeniSysAI/NLU "NLU engine") for natural language understanding, in browser speech synthesis and speech recognition for speech and hearing, all homed on a dedicated Linux server in your home and managed via a secure UI.

# About GeniSys NLU Engine

I orginally developed what is now the [GeniSys NLU Engine](https://github.com/GeniSysAI/NLU "GeniSys NLU Engine") back in 2017 ([How I built a fully functional Deep Learning Neural Network chatbot platform (NLU Engine) in under a week....](https://www.techbubble.info/blog/artificial-intelligence/chatbots/entry/deep-learning-neural-network-nlu-engine "How I built a fully functional Deep Learning Neural Network chatbot platform (NLU Engine) in under a week....")). The project was originally developed to be used in some commercial AI projects I had built, after I closed the business down it became a personal project for my home and as I have open sourced most of my other projects, it made sense to open source this one.

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
>Hi
2018-09-30 22:58:37|Human|Intent: Hi
2018-09-30 22:58:37|GeniSys|Reponse: Hello human, please tell me your GeniSys user

>It is Adam of course!
2018-09-30 22:58:44|Human|Intent: It is Adam of course!
2018-09-30 22:58:44|GeniSys|Reponse: Hello Adam, what can I do for you?

>If I was your friend, what would I call you?
2018-09-30 22:58:54|Human|Intent: If I was your friend, what would I call you?
2018-09-30 22:58:54|GeniSys|Reponse: Call me Geni

>Ok but what is your real name?
2018-09-30 22:59:01|Human|Intent: Ok but what is your real name?
2018-09-30 22:59:01|GeniSys|Reponse: My name is GeniSys

>Ok thanks
2018-09-30 22:59:10|Human|Intent: Ok thanks
2018-09-30 22:59:10|GeniSys|Reponse: Any time!

>Please tell me, what is my name?
2018-09-30 22:59:22|Human|Intent: Please tell me, what is my name?
2018-09-30 22:59:22|GeniSys|Reponse: Your name is Adam, how can I help you?

>I don't suppose you know what time it is?
2018-09-30 22:59:32|Human|Intent: I don't suppose you know what time it is?
2018-09-30 22:59:32|GeniSys|Reponse: The time is Sun Sep 30 22:59:32 2018

>Ah cool thanks
2018-09-30 22:59:37|Human|Intent: Ah cool thanks
2018-09-30 22:59:37|GeniSys|Reponse: My pleasure
```

In the conversation above, when I asked the time, the extension attached to the related intent in the training data is triggered, basically an extension is the path to a function in one of your custom classes, you can find out more about this later in the tutorial. Although hardly any of the things I said were entirely provided in the training data, the AI was capable of identifying my intent.

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

# Prerequisites

You must of already completed the setup following project:

- [GeniSys Server](https://github.com/GeniSysAI/Server "GeniSys Server")

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

Now it is time to think about training data. In the [data/training.json](https://github.com/GeniSysAI/NLU/blob/master/data/training.json "data/training.json") file I have provided some starter data, it is not a lot but enough to have a good test and show the example further on in the tutorial. 

## Extensions

Extensions are external Python classes that you can use to extend the functionality used to generate a response. Extensions should be stored in the [extensions](https://github.com/GeniSysAI/NLU/tree/0.0.4/extensions "extensions") directory. Below is an example configuration that is used to execute the gTime -> getTime function. Defined responses with placeholders specified by %%, once the function is ready it will return a modified response replacing %%TIME%% with the actual time. This response will override any response previously selected. For a more detailed extension, check out gHumans which uses MySql to manage the users GeniSys interacts with. 

```
"extension":  {
    "function": "extensions.gTime.getTime",
    "entities": false,
    "responses": [
        "The time is %%TIME%%",
        "Right now it is %%TIME%%",
        "It is around %%TIME%%"
    ]
}
```

# Training Your NLU Engine

[![Training Your NLU Engine](images/train-confirmation.jpg)](https://github.com/GeniSysAI/NLU/blob/master/Train.py)

Now everything is set up, it is time to train. The main functionality for the training process can be found in [Train.py](https://github.com/GeniSysAI/NLU/blob/master/Train.py "Train.py"), [tools/Data.py](https://github.com/GeniSysAI/NLU/blob/master/tools/Data.py "tools/Data.py"), [tools/Model.py](https://github.com/GeniSysAI/NLU/blob/master/tools/Model.py "tools/Model.py") and  [tools/Mitie.py](https://github.com/GeniSysAI/NLU/blob/master/tools/Mitie.py "tools/Mitie.py"), the configuration for training can be found and modified in [required/confs.json](https://github.com/GeniSysAI/NLU/blob/master/required/confs.json "required/confs.json"). If you have modified your training data, you may need to update your configuration from time to time. 

To begin training, make sure you are all set up, navigate to the root of the project and execute the following command:

```
 $ python3 run.py TRAIN
```

[![Training Your NLU Engine](images/train-results.jpg)](https://github.com/GeniSysAI/NLU/blob/master/Train.py)

# Tensorboard

You can use Tensorboard to see how your deep neural network has done during training. If you used the [default Nginx configuration](https://github.com/GeniSysAI/Server/blob/master/etc/nginx/sites-available/default "default Nginx configuration") then you should be able to access Tensorboard on **YourDomainName/tensorboard/**, note the / at the end of **tensorboard/** is required.

Once training has finished you can start Tensorboard with the following commands: 

```
 $  tensorboard --logdir model/TFLearn
```

[![NLU Engine Accuracy](images/accuracy.jpg)](https://github.com/GeniSysAI/NLU/blob/master/Train.py)

[![NLU Engine Accuracy](images/loss.jpg)](https://github.com/GeniSysAI/NLU/blob/master/Train.py)

# Communicating with your AI Locally

Now you have trained your AI, it is time to test her out! In this tutorial I will base my explanation on the conversation block at the beginning of this tutorial. 

As your AI is now trained, all you need to do (assuming you are in the project root), is execute the following code:

```
 $ python3 run.py INPUT
```

If you have looked through the example data, you may notice that almost none of the things that I said in the above dialogue had been directly trained to the AI. For example, with the question **If I was your friend, what would I call you?**, the actual training data provided to the AI related to this question is actually:

```
"intent": "NameQuery",
"text": [
    "What is your name?",
    "What could I call you?",
    "What can I call you?",
    "What do your friends call you?",
    "Who are you?",
    "Tell me your name?"
]
```

You can see that the example above was not in the training data, but the AI was still able to classify and respond correctly. 

# Joking With Your AI

Basic functionality exists for parsing AIML documents into a format suitable for training the NLU and adding it to the training data. Below is an example after training with a few jokes found in an AIML file provided by [Pandorabots]( https://github.com/pandorabots/Free-AIML/blob/master/jokes.aiml "Pandorabots"), this file actually turned out to be written by one of my friends, 4 time Loebner Prize winner for most human like AI, Steve Worswick.

```
2018-09-08 22:03:38|Inference|INFO: Inference Started In INPUT Mode
2018-09-08 22:03:38|Session|INFO: NLU Session Ready For User #1

>I bet you are not funny, can you tell me a joke?
2018-09-08 22:03:51|Human|Intent: I bet you are not funny, can you tell me a joke?
2018-09-08 22:03:51|GeniSys|Reponse: A man returns from an exotic holiday and is feeling very ill. He goes to see his doctor, and is immediately rushed to the hospital to undergo some tests. The man wakes up after the tests in a private room at the hospital, and the phone by his bed rings. 'This is your doctor. We have the results back from your tests and we have found you have an extremely nasty disease called M.A.D.S. It's a combination of Measles, AIDS, Diphtheria, and Shingles!'  'Oh my gosh', cried the man, 'What are you going to do, doctor?'  'Well we're going to put you on a diet of pizzas, pancakes, and pita bread.' replied the doctor.  'Will that cure me?' asked the man.  The doctor replied, 'Well no, but, it's the only food we can slide under the door.'

>Not bad, tell me another joke
2018-09-08 22:04:12|Human|Intent: Not bad, tell me another joke
2018-09-08 22:04:12|GeniSys|Reponse: A doctor thoroughly examined his patient and said, 'Look I really can't find any reason for this mysterious affliction. It's probably due to drinking.' The patient sighed and snapped, 'In that case, I'll come back when you're damn well sober!'

>Alcohol jokes are always funny! You can tell me another joke
2018-09-08 22:04:40|Human|Intent: Alcohol jokes are always funny! You can tell me another joke
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

# Useful Links

Links to related articles that helped at various stages of the project for research / code examples:

- [TFLearn Quickstart](http://tflearn.org/tutorials/quickstart.html "TFLearn Quickstart")
- [Bag of Words Algorithm in Python Introduction](http://insightsbot.com/blog/R8fu5/bag-of-words-algorithm-in-python-introduction "Bag of Words Algorithm in Python Introduction")
- [Chatbot Architecture](https://medium.com/@surmenok/chatbot-architecture-496f5bf820ed "Chatbot Architecture")
- [Contextual Chatbots with Tensorflow](https://chatbotsmagazine.com/contextual-chat-bots-with-tensorflow-4391749d0077 "Contextual Chatbots with Tensorflow")
- [RasaNLU](https://github.com/RasaHQ/rasa_nlu/ "RasaNLU")

# Stay Tuned!!

There are more features from my original version that are still yet to be implemented plus some other cool features, pluse the combined system of all three GeniSys AI repos.

# Contributing
Please read [CONTRIBUTING.md](https://github.com/GeniSysAI/NLU/blob/master/CONTRIBUTING.md "CONTRIBUTING.md") for details on our code of conduct, and the process for submitting pull requests to us.

# Versioning
We use SemVer for versioning. For the versions available, see [GeniSysAI/NLU/releases](https://github.com/GeniSysAI/NLU/releases "GeniSysAI/NLU/releases").

# License
This project is licensed under the **MIT License** - see the [LICENSE](https://github.com/GeniSysAI/NLU/blob/master/LICENSE "LICENSE") file for details.

# Bugs/Issues
We use the [repo issues](https://github.com/GeniSysAI/NLU/issues "repo issues") to track bugs and general requests related to using this project. 

# Author
[![Adam Milton-Barker: BigFinte IoT Network Engineer & Intel® Software Innovator (IoT, AI, VR)](images/Adam-Milton-Barker.jpg)](https://github.com/AdamMiltonBarker)