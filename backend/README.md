# Elastiticty Template App

## What is Elasticity and Why Do We Need a Template?

Elasicity is an internal libary built by Vivacity labs. It allows us to standadise the process of taking a device message saving it to serve to an API, post processing it if needed and backing it up to secure long term storage.

The benfits of this is the process can be very robust. It also means a tool to use this libary can be quickly as all the hard work is done in the liabry. 

This is where the template comes in. The liabry can be quite intimidating and using it even more so. This template allows an easy entry point to learn how to use elasticity and how it works. It also make setting up an app to use it really quick even it you dont know how it all works behind the curtains.

### Contents
* .eslint.rc - Eslint file for checkstyle standardization
* .gitignore - ignore files that are unneeded or user specific for the git repo
* package.json - Package file for NPM to run basic elastiticity project. [Read more here](#nodejs-app)
* configTemplate.js - Template for project spefic config settings for all the supporting tools needed for elasticity like GCP Pub/Sub Topic, Bucket etc. [Read more here](#external-tools). This can be edited manually or use the automated script.
* app.js & server.js - To js files to spin up an express app on a port and run elasity from config setup, doing some basic message processing and template /raw and /processed routes. [Read more here](#nodejs-app)
* setup.sh - A semi-automated script to lead you through setting up all the external tools need to run elascity. [Read more here](#using-the-setup-script)

## Elastiticty Process

![Elasticity Process](assets/Elastcity.png?raw=true)

### External Tools
There is a number of external tools that we need to make elasticity work. Even though below tools from specific providers are mentioned these are general tools that could be aplied to any provided or setup ourselfs.

#### GCP PubSub

To send messages from devices we use a pub/sub service, Google Cloud Platform has a nice one so we use this. It works on a topic/subscription based serivce so the devices send to a topic and the subscribers subscribe to that topic so they can get all the messages published to the topic pretty simple. (You can get pretty complicated configurations but we try and K.I.S.S.). 

So to run Elasticity you need to give it some pubsub setting in the config, 
* **Topic** that the devices are sending messages too.
* **Subscription** to that topic for you app to recive the messages.
* The GCP **ProjectId** that both of the above live in.

Thats it for pub/sub, you can set these up manually or with the automated script.

These are stored in **config.gcp.topic**, **config.gcp.subscription** and **config.gcp.projectId** respectively.

If you want to know more about GCP Pub/Sub there is lots of documentation that can be found [here](https://cloud.google.com/pubsub/docs/)

#### Redis

For most projects we do we will want to serve a live API for a period of time. This means we need something that can serve this data as quick as possible, thats where Redis comes in. Redis is an inmemory Key/Value DB that can serve data very fast because of the nature of how it is set up. We use redis to serve up data for our **config.windowPeriod**, this is the ammount of time we want to serve up data to the customer from the live api, it may be 30 seconds or 5 minutes. 

For Elasticity you need to setup a redis instance and give it the host and optionally the password if you instance is protected.

These are stored in **config.redis.host** and **config.redis.password**.

If you want to know more about Redis there is lots of documentation that can be found [here](https://redis.io/documentation)

#### Storage

We dont want to keep data in redis forever because of the nature of redis being an inmemory DB its not fisable for long term storage.

This is where cloud storage comes in, we take the data from redis over the window and backlog period, split it into chunks of window period and save the raw and processed to a bucket in cloud storage. Then when the save is successfully completed remove from redis. It is now slower to access this data but it is in long term storage.

To support this we need the bucket stored in **config.gcp.bucket**.

If you want to know more about storage there is lots of documentation that can be found [here](https://cloud.google.com/storage/docs/)

### Config Time Varibles

In the config there is some time varibles that need to be set,
* windowPeriod - The time window of data shown on the live API
* backlogPeriod - The time window of data kept in redis after the live API and before it is backup to cloud storage.
* writeInterval - The time interval at which the storage process is run to save data above backlog period to cloud storage and remove from redis. This should be aleast more than window and backlog.
* dataProcessInterval - The time interval that the data process is run. So the time interval at which the process callback from you app is called and run to process raw data.

### Node.js App

So if we have all our external tools setup there is only one thing left our node.js app implementing elasticity. A basic app only has to do start an instance on Elasticity with the config we have create but we also need a process callback function. There will be cases where we want to post processes messsages from the device, maybe we can only do with with messages from every device or range of devices whatever the case may be elasticity requires the process callback to be passed in.

The process callbacks has all raw data from redis and current processed set as an input it can use that data in anyway it wants but it must return a single json object which will be stored in redis as the new processed object and returned the next time process callback is called. The template app handly comes with a super simple process callback in **server.js** that can be studied to userstand what the best approach for each project might be.

Once we have that we can start it and it should all just work.

If there is a problem a handy way to debug it is to set the logging level in the config, **config.logginglevel**. This means elasticity will return more logs to give more details of what is going on inside the liabry.

## Using the Setup Script

### Pre-Requistes 
* gsutil
* gcloud
* redis instance
* some understanding of Elasiticity

The setup script is a script that can be run once (or multiple time if you wish) and write most of the config for you, promoting you with input when needed, it will also automate setting up topics, subscriptions and buckets if they are not already set up.

As it does that gcp setup, the gcloud and gsutil command line tools are required to be on the machine running. It would also be advised that the user has some knowledge of what they are doing to stop, lots of unused gcp objects being created for no reason.

Running the script is as simple as **./setup.sh** inside the directory or template-elasticity-app/setup.sh outside. The rest you will be guilded through.