from flask import Flask, request 
import xmltodict
import requests
import math  
import time
import yaml
from geopy.geocoders import Nominatim 


app = Flask(__name__)

def get_data() -> list:
    """
    Gets the data from the NASA website for the ISS trejectories 

    Args: 
        No args for this function 
    
    Returns: 
        data (list): The data from the ISS trajectory xml 

    """
    r = requests.get("https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml")
    if r.status_code == 200:
        data = xmltodict.parse(r.text)
        return data
 

@app.route('/', methods=['GET']) 
def data() -> list:  
    """
    Gets the ISS Trajectory data from the NASA website. 

    Args: 
        No args for this function.

    Returns: 
        iss_data (dict): The dictionary of the data that was imported using the requests library, the imported data was an 
        xml file. 
    """
    if iss_data == {}: 
        return "Data has been deleted\n"
    else:
        return iss_data 

@app.route('/keys', methods=['GET'])
def keys() -> list:   
    """
    Goes thrrough all the keys in the data set to find which one epochs is under. 

    Args:
        No args for this function.

    Returns: 
        list1 (list): returns a list of keys associated with the xml data
        list2 (list): returns a list of keys associated with the "ndm" key
        list3 (list): returns a list of keys associated with the "oem" key
        list4 (list): returns a list of keys associated with the "body" key
        list5 (list): returns a list of keys associated with the "segment" key
        list6 (list): returns a list of keys associated with the "data" key
        list7 (list): returns the epochs and the values associated with it using the stateVector key. 
    """

    key_data = data() 
    
    try:
        list1 = list(key_data.keys())
        # return list1
        list2 = list(key_data['ndm'].keys()) 
        #return list2 
        list3 = list(key_data['ndm']['oem'].keys())
        #return list3
        list4 = list(key_data['ndm']['oem']['body'].keys())
        #return list4
        list5 = list(key_data['ndm']['oem']['body']['segment'].keys())
        #return list5
        list6 = list(key_data['ndm']['oem']['body']['segment']['data'].keys())
        #return list6
        list7 = list(key_data['ndm']['oem']['body']['segment']['data']['stateVector'])
        return list7
    except AttributeError: 
        return "Data has been deleted\n" 

@app.route('/epochs', methods=['GET']) 
def epochs()->  list:  
    """
    Returns the epochs in the dictionary and every value assoicated with the epochs.

    Args: 
        No args for this function. 

    Returns: 
        epochs_data (list): returns the epoch data from the dictionary as a list along with all values
        associated with it.
    """    
    epochs_data = keys()  
   
    offset = request.args.get('offset',0)
    if offset: 
        try: 
            offset = int(offset)
        except ValueError: 
            return "Invalid start parameter; start must be an integer. \n"
    limit = request.args.get('limit', len(epochs_data)) 
    if limit: 
        try: 
            limit = int(limit)
        except ValueError: 
            return "Invalid start parameter; start must be an integer. \n" 
    if limit > len(epochs_data) or offset > len(epochs_data) or offset < 0 or limit < 0:
        return "Change query paramater \n"

    counter = 0 
    result = [] 
    for d in range(len(epochs_data)): 
        if counter == limit: 
            break 
        if d >= offset:
            try: 
                result.append(epochs_data[d]['EPOCH'])
                counter = counter + 1
            except TypeError: 
                return "Data has been deleted\n" 
    return result   


@app.route('/epochs/<string:epoch>', methods=['GET'])
def an_epoch(epoch: str) -> list:
    """
    This function returns a single epoch from the list of epochs

    Args: 
        epoch (string): The epoch value this function takes in is a string of the specific 'EPOCH' value 
        associated with this certain epoch 

    Returns: 
        single_epoch (list): The single_epoch is the list that stores the values associated with the certain
        epoch chosen by the user 
        

    """  
    try:     
        epochs_data = keys()
        single_epoch = [] 
        for i in range(len(epochs_data)): 
            if epoch == str(epochs_data[i]['EPOCH']):
                single_epoch = epochs_data[i] 
                return  single_epoch  
        if single_epoch == []: 
            return "Please enter a valid epoch ID\n" 
    except TypeError: 
        return "Data has been deleted\n" 
    
     

@app.route('/epochs/<string:epoch>/speed', methods=['GET'])
def speed(epoch: list) -> dict:
    """
    This function calculates the instantaneous speed of the epoch by squaring each x_dot,y_dot,z_dot 
    respectively adding them toghether and then taking the square root of the total.

    Args: 
        epoch (string): The epoch value this function takes in is a string of the specific 'EPOCH' value
        associated with this certain epoch

    Returns: 
        awnser (f string): Returns the insatntaneous speed in an F string with the message "The speed of 
        the epoch is:"  
    """
    try: 
        single_epoch = an_epoch(epoch) 

        x_dot = float(single_epoch['X_DOT']['#text'])
        y_dot = float(single_epoch['Y_DOT']['#text'])
        z_dot = float(single_epoch['Z_DOT']['#text']) 

        speed = math.sqrt(x_dot**2+y_dot**2+z_dot**2)

        awnser = {'value': speed, 'units': "km/s" }
        return awnser
    except TypeError: 
        return "Data has been deleted or try changing the epoch id\n" 


@app.route('/help', methods=['GET'])
def help() -> str:
    """
    Pulls up a help menu for the user to know the commands for the program

    Args:
        None

    Returns: 
        paths (str): A string with all the commands for this function 

    """

    paths = """These are the paths and methods used for this application

Paths:
    t(/)                           This path uses the GET method and returns the entire data set
    (/epochs)                      This path uses the GET method and returns the list of all Epochs in the data set
    (/epochs?limit=int&offset=int) This path uses the GET method and returns a modified list of Epochs given query parameters
    (/epochs/<epoch>)              This path uses the GET method and returns the state vectors for a sepecifc Epoch from the data set
    (/keys)                        This path uses the GET method to find all the keys within the data set
    (/epochs/<epoch>/speed)        This path uses the GET method to return instantaneous speed for a specific Epoch in the data set 
    (/help)                        This path uses the GET method to return help text that briefly describes each route
    (/delete-data)                 This path uses the DELETE method to delete all data from the dictioanry object
    (/post-data)                   This path uses the POST method to reload the dictionary object with data from the web""" 
    return paths

@app.route('/delete-data', methods=['DELETE'])
def delete() -> str:
    """
    Deletes all the data from the iss_data set

    Args: 
        No args 

    Returns: 
        (str): A string that says deleted to show the data has been deleted

    """
    global iss_data
    iss_data.clear()

    return "Deleted \n"

@app.route('/post-data', methods=['POST'])
def post() -> str:
    """
    Deletes all the data from the iss_data set

    Args:
        No args

    Returns:
        (str): A string that says "data posted" to show the data has been deleted

    """
    global iss_data
    iss_data = get_data()    
    return "data posted\n"   

#Global variable called iss_data 
iss_data = get_data()

@app.route('/comment', methods=['GET'])
def comment() -> list:
    """
    Gives the comments that are associated with the data set 

    Args: 
        None
    Returns: 
        list_of_comments (list): The comments associated with the data set as a list
        (str): A string that says data deleted if command is called after the data has been deleted
    
    """
    try:
        comment_data = data()
        list_of_comments = list(comment_data['ndm']['oem']['body']['segment']['data']['COMMENT'])
        return list_of_comments
    except TypeError: 
        return "Data has been deleted\n" 

@app.route('/header', methods=['GET'])
def header() -> dict:
    """
    Gives the header that is associated with the data set
    Args:
        None
    Returns:
        header (dict): The header associated with the data set as a dictioanry  
        (str): A string that says data deleted if command is called after the data has been deleted
    """
    try:
        header_data = data() 
        header = header_data['ndm']['oem']['header'] 
        return header
    except TypeError: 
        return "Data has been deleted\n" 

@app.route('/metadata', methods=['GET'])
def metadata() -> dict:
    """
    Gives the metadata that is associated with the data set

    Args:
        None
    Returns:
        meta (dict): The metadata associated with the data set as a dictionary
        (str): A string that says data deleted if command is called after the data has been deleted
    """
    try: 
        metadata = data() 
        meta = metadata['ndm']['oem']['body']['segment']['metadata'] 
        return meta
    except TypeError: 
        return "Data was deleted\n" 


@app.route('/epochs/<string:epoch>/location', methods=['GET'])
def location(epoch: list) -> dict:
    """
    This route finds the location of a given epoch 

    Args: 
        epoch (list): The single epoch and all values associated with it

    Returns: 
        location (dict): A dictionary with latitude, longitude, altitude with its units, and its
                         geopostion for the epoch specified. 

    """
    try:
        MEAN_EARTH_RADIUS = 6371 #km 

        the_epoch = an_epoch(epoch)
        units = "km" 

        x = float(the_epoch['X']['#text']) 
        y = float(the_epoch['Y']['#text'])
        z = float(the_epoch['Z']['#text'])
   
        hrs = float(the_epoch['EPOCH'][9:11])
        mins = float(the_epoch['EPOCH'][12:14]) 
     
        lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2))) 
        lon = math.degrees(math.atan2(y,x)) - ((hrs-12)+(mins/60))*(360/24) + 24
        alt = math.sqrt(x**2 + y**2 + z**2) - MEAN_EARTH_RADIUS
    
        lon = lon_correct(lon)   
         

        geocoder = Nominatim(user_agent='iss_tracker')
        geoloc = geocoder.reverse((lat,lon), zoom=15, language='en') 

        if geoloc == None: 
            position = 'ISS is over the Ocean'
        else: 
            position = {'Address': geoloc.address} 

        location = {'latitude': lat, 'longitude': lon, 'altitude': {'value': alt,  'units': units}, 'geo': position }  
        return location
    except TypeError: 
        return "Make sure epoch ID is correct or the data was deleted\n" 
    
def lon_correct(lon) -> float:
    """ 
    Normalizes the longitude value when it leaves the -180 range
    Args: 
        lon (float): The longitude value given from the equation 
    returns: 
        lon (float): The longitude value after the correection
    """
    while lon >= 180:
        lon -= 360
    while lon <= -180:
        lon += 360

    return lon

@app.route('/now', methods = ['GET'])
def now() -> dict:
    """
    The route returns the closest epoch at the current time 

    Args: 
        None
    Returns: 
        now (dict): This dictionary contains the ID for the closest epoch, it's geogrpahical location, and 
                    its speed and how many seconds it is away from now 

    """
    try: 
        time_now = time.time()
        epochs_data = epochs() 
        time_epoch = time.mktime(time.strptime(epochs_data[0][:-5], '%Y-%jT%H:%M:%S'))
        minimum = time_now - time_epoch 

         
        for epoch in epochs_data:
            time_epoch = time.mktime(time.strptime(epoch[:-5], '%Y-%jT%H:%M:%S'))
            compare = time_now - time_epoch
            if abs(compare) < abs(minimum):  
                minimum = compare 
                closest_epoch = epoch 
                
        now_loc = location(closest_epoch)
        now_speed = speed(closest_epoch) 

        now = {} 
        now['closest_epoch'] = closest_epoch 
        now['seconds_from_now'] = minimum 
        now['location'] = now_loc
        now['speed'] = now_speed

        return now 
    except ValueError: 
        return "The data was deleted\n" 


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
   
