# Tracking the international Space Station (Midterm Project / Surf Wax ISS) 

Scenario: In Homework 05, we added more routes to our ISS tracker. Now, we will finish off this project by adding a few final routes, automate deployment with Docker 
Compose, and write up a short document describing the project.

The purpose of this project was to add onto homework04 and homeowrk05. In homework04 The purpose of the project was to read in the ISS data from an xml link. Using the 
link I had to find the data associated with the epochs. Then using that data with the epochs I created a path to a single epoch. Once the single epoch was returned I
calculated the instantaneous velocity using the x_dot, y_dot, and z_dot value in the data set. In this homework there is three added routes with two of them using completley
new methods "DELETE" and "POST." One of the routes deletes the entire data set, one posts it all back and the other gives a help sting to the user.
Within this project aswell I used defensive coding to bar the user from crashing the program using bad inputs. For the project there are five additional routes with two of 
them using a new python library called GeoPy. Three of the routes give data associated with a certain key: header, metadata, and comment. The other two use the GeoPy
library to find the exact location of the ISS at a certain epoch or at the current time. 

## Important Files
`iss_tracker.py`: This is the main script of the project. The iss_tracker script has twelve total routes all described in the table below. This script uses defensive 
programming strategies to make sure it runs without breaking and will give a message if something is incorrect. 

`Dockerfile`: This file containerize the `iss_tracker.py` script. The image created by the Dockerfile contains the same version of python used to create the script and 
other dependencies such as: `pyyaml`, `Flask`, `requests`, `GeoPy` and `xmltodict`. 

`docker-compose.yml`: This file is a compose file to automate the development of the app. It configures the build image with the specific tag and binds the appropriate 
ports from the container to the host. 

## How to Download and Build App
To Download and use the containerized app follow these instructions. 

### 1. 
Pull the image from docker hub using this command
```
docker pull jetp104/iss_tracker:midterm
```
### 2. 
Build this image by using this command 
```
docker build -t jetp104/iss_tracker:midterm .
```
### 3. 
Run the docker image by using this command
```
docker run -it --rm -p 5000:5000 jetp104/iss_tracker:midterm
```

To check if the image was succesfully built use this command 
```
docker images
```

### Optional Step in process 
Once you docker pull image from docker hub you if you have the `docker-compose.yml` file 
you can use the command 
```
docker-compose up 
```
to fully automate the development of the app. 

## How To Interact with the App 
This app has a total of 12 different routes that are listed in this table. 

|Routes|What They Do| 
|------|------------|
|   /  |This route returns the entire data set used for the app| 
