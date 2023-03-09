# Tracking the international Space Station (Midterm Project / Surf Wax ISS) 

Scenario: In Homework 05, we added more routes to our ISS tracker. Now, we will finish off this project by adding a few final routes, automate deployment with Docker 
Compose, and write up a short document describing the project.

The purpose of this project was to add onto homework04 and homeowrk05. In homework04 The purpose of the project was to read in the ISS data from an xml link. Using the 
link I had to find the data associated with the epochs. Then using that data with the epochs I created a path to a single epoch. Once the single epoch was returned I
calculated the instantaneous velocity using the x_dot, y_dot, and z_dot value in the data set. In this homework there is three added routes with two of them using completley
new methods "DELETE" and "POST." One of the routes deletes the entire data set, one posts it all back and the other gives a help sting to the user.
Within this project aswell I used defensive coding to bar the user from crashing the program using bad inputs. For the project there are five additional routes with two of 
them using a new python library called GeoPy. Three of the routes give data associated with a certain key: header, metadata, and comment. The other two use the GeoPy
library to find the exact location of the ISS at a certain epoch or at the current time. Another purpose was to use containerization and automation when using the 
`docker-compose.yml` file.

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
If done correctly this is what should happen

![image](https://user-images.githubusercontent.com/122917623/224171410-efa74a22-9fcd-4363-967d-fbfed5ebd303.png)

### 2. 
Build this image by using this command 
```
docker build -t jetp104/iss_tracker:midterm .
```
If done correctly this is what should happen 

![image](https://user-images.githubusercontent.com/122917623/224171606-50af052c-1f7d-470b-bce0-d72fca6d0606.png)

### 3. 
Run the docker image by using this command
```
docker run -it --rm -p 5000:5000 jetp104/iss_tracker:midterm
```
If done correctly your shell should be taken over and look like this

![image](https://user-images.githubusercontent.com/122917623/224187207-00112451-0b49-424b-aa8d-3e0715e07cfb.png)

To check if the image was succesfully built use this command 
```
docker images
```
If the image was built correctly this will show up

![image](https://user-images.githubusercontent.com/122917623/224171932-0b2b8996-60a3-4b57-b5ea-71644a3b47ad.png)

### To use a pre-containerized copy of the app 
Once you docker pull image from docker hub you if you have the `docker-compose.yml` file 
you can use the command 
```
docker-compose up 
```
to fully automate the development of the app, which will look like this 

![image](https://user-images.githubusercontent.com/122917623/224187131-ae9e7f38-11dd-4568-8712-efb1b0f06e26.png)



## Routes 
This app has a total of 14 different routes that are listed in this table. 

|Routes|What They Do| 
|------|------------|
|   /  |This route returns the entire data set used for the app| 
|/keys|This route returns the list of keys used in the data set| 
|/epochs| A list of all Epochs in the data set| 
|/epochs/<epoch<epoch>>| State vectors for a specific Epoch from the data set|
| /epochs/<epoch<epoch>>/speed| Instantaneous speed for a specific Epoch in the data set| 
|/epochs?limit=int&offset=int| Return modified list of Epochs given query parameters| 
|/help| Return help text (as a string) that briefly describes each route| 
|/delete-data| Delete all data from the dictionary object| 
|/post-data| Reload the dictionary object with data from the web|
|/comment| Return ‘comment’ list object from ISS data| 
|/header| Return ‘header’ dict object from ISS data| 
|/metadata| Return ‘metadata’ dict object from ISS data| 
|/epochs/<epoch<epoch>>/location| Return latitude, longitude, altitude, and geoposition for given Epoch|
|/now| Return latitude, longitude, altidue, and geoposition for Epoch that is nearest in time| 

## How to interact with the app and Interpret the results from the routes 
To interact with the application you will use one of the three starting commands
### 1. 
```
curl localhost:5000
```
### 2. 
```
curl -X DELETE localhost:5000
```
### 3. 
```
curl -X POST localhost:5000
```
These three commands will give you the ability to access the routes. In order of the table 
here are the routes, what they output, and how to interpret the output. 

### 1. /
use the command 
```
curl localhost:5000/ 
```
If entetered correctly this will be the output 

![image](https://user-images.githubusercontent.com/122917623/224175166-6bee923e-21af-473b-859a-d6c7b9f14357.png)

Interpretation: This is the entire data set including all the keys and values assoicated with those keys 
  
### 2. /keys 
use the command
```
curl localhost:5000/keys
```
If entered correctly this will be the output 

![image](https://user-images.githubusercontent.com/122917623/224175467-b568efb7-f48e-4f2a-ad87-b9020b0f7117.png)

Interpretation: This function returns the keys assoicated with the data set in the case of the picture it returns the values attached to the statevectors key. 
  
### 3. /epochs
use the command
```
curl localhost:5000/epochs
```
If entered correctly this will be the output 
  
![image](https://user-images.githubusercontent.com/122917623/224175912-30be3af5-d88c-4f42-b42a-d542116a915d.png)

Interpretaion: This route returns the IDs of all the epochs in the data set associated with the statevectors key. 
  
### 4. /epochs/<epoch<epoch>>
use the command 
```
curl localhost:5000/epochs/"2023-082T12:00:00.000Z"
```
If entered correctly this will be the output

![image](https://user-images.githubusercontent.com/122917623/224176236-f0c9fee6-44d6-4465-a3cc-8b8f40e93098.png)

Interpretation: This route returns the values associated with the specified epoch 
  
### 5. /epochs/<epoch<epoch>>/speed
use the command 
```
curl localhost:5000/epochs/"2023-082T12:00:00.000Z"/speed 
```
If entered correctly this will be the output
  
![image](https://user-images.githubusercontent.com/122917623/224176580-4ef3e9d8-251e-49c8-b153-7722c9152d6e.png)

Interpreation: This gives the instantenous velocity of the specified epoch along with the units.
  
### 6. /epochs?limit=int&offset=int
use the command
```
curl 'localhost:5000/epochs?limit=5&offset=10'  
```
If entered correctly this will be the output 
  
![image](https://user-images.githubusercontent.com/122917623/224176973-6848108b-fb90-46df-879f-b7a744fb3112.png)

Interpretation: The offset value gives where in the list of epoch IDs you want to start and the limit asks how mnay you want to return from that starting point so in the picture I wanted to start at the 5th epoch in the list and only return 1 epoch. 

### 7. /help 
use the command
```
curl localhost:5000/help
```
If entered correctly this will be the output 

![image](https://user-images.githubusercontent.com/122917623/224178979-cb0e5df8-457c-4898-84d2-9090b891384c.png)

Interpretation: This just returns a string that tells the user what method each route uses and what they return 
  
### 8. /delete-data
use the command 
```
curl -X DELETE localhost:5000/delete-data  
```
If entered correctly this will be the output
  
![image](https://user-images.githubusercontent.com/122917623/224179300-8c37d775-7b6c-4862-8811-f85bd1df596a.png)

Interpretation: The string returned will say deleted and that means the entire data set was deleted
  
### 9. /post-data
use the command
```
curl -X POST localhost:5000/post-data
```
If entered correctly this will be the output 
  
![image](https://user-images.githubusercontent.com/122917623/224179558-51cfcd8c-5363-4e19-9799-d1107aaff2c3.png)

Interpretation: The string returned will say the data has been posted which means the entire data set is back and refreshed from the delete-data command

### 10. /comment
use the command
```
curl localhost:5000/comment
```
If done correctly this will be the output 
  
![image](https://user-images.githubusercontent.com/122917623/224180222-63540962-947f-4256-a17a-f71ccafb34be.png)

Interpretation: This returns the comments keys attached to the data set which is the comments made by the people who keep the data set updated. 
 
### 11. /header
use the command
```
curl localhost:5000/header
```
If done correctly this will be the output 

![image](https://user-images.githubusercontent.com/122917623/224180552-c54a36d4-ff61-4ddf-8d5f-6b371abfd0ab.png)

Interpretation: This returns the header key assigned to the data set which is just the date the data was created and the people who originated it. 
### 12. /metadata
use the command
```
curl localhost:5000/metadata
```
If done correctly this will be the output 

![image](https://user-images.githubusercontent.com/122917623/224180856-79fcb0b8-e22f-4c3a-b7c0-3ab2e3393aee.png)

Interpretation: This returns the metadata key which includes the refrence frame which is earth, the start time, and what the data tracks
  
### 13. /epochs/<epoch<epoch>>/location
use the command
```
curl localhost:5000/epochs/<epoch<epoch>>/location
```
If done correctly the output will be
  
![image](https://user-images.githubusercontent.com/122917623/224181191-235ba6ae-1b83-4f4e-b030-7849bfc2aa9b.png)

Interpretation: This returns the longitude, latitude, and altitude, along with altitude units, and where the ISS was over at the time of the specified epoch
  
### 14. /now
use the command 
```
curl localhost:5000/now
```
If done correctly the output will look like this
  
![image](https://user-images.githubusercontent.com/122917623/224182047-48573f66-570b-45cb-858f-1f1c1e34af46.png)
    
Interpretation: This returns the latitude, longitude, altidue along with the units, the speed of the epoch, the seconds the closest epoch was and geoposition for Epoch that is nearest in time to when the route was called. 
