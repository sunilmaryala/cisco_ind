# This script is for Cisco Industrial Network Director (IND)
# It uses IND Rest API
# This script is used to retrive No of Duplicate links exist between 2 devices
# In your network if there are duplicate links use this script to identify such links and fnd if these are any cause of network loops
# The output of this script is printing of all devices along with total links to that device and then no of duplicate links along with the devices to which it has duplicate links

import requests

# ind_info is a dict in the form of {'ip': {ind_ip}, 'username': {username}, 'password': {password}
# un comment the line below after entering the IND IP address and login details username and password
#ind_info = {'ip': 'xxx.xxx.xxx.xxx', 'username': 'xxxxxx', 'password': 'xxxxxx'}


#######################################################################################################################################
def request_get(url, auth_info):
    assert type(url) == str, 'URL not a string'
    assert type(auth_info) == tuple, 'Auth info not a tuple'
    try:
        request_data = requests.request('GET', str(url), auth=auth_info, verify=False, headers={'Content-Type': 'application/json'})
        return [request_data, request_data.json()]
    except Exception as msg:
        return [requests.get('http://httpbin.org/status/500'), {}]

#######################################################################################################################################
def find_duplicate(x):
# generic function to detect duplicate items in a list
    _size = len(x) 
    repeated = [] 
    for l in range(0, _size): 
        k = l + 1
        for j in range(k, _size): 
            if x[l]['name'] == x[j]['name']: 
                repeated.append(x[l]['name'])
                
    return repeated 


#######################################################################################################################################
# This function is called in the program
def main_routine(ind_info):

# ind_info is a dict in the form of {'ip': {ind_ip}, 'username': {username}, 'password': {password}
    
    url = 'https://' + ind_info['ip'] + ':8443/api/v1/devices'
    print (url)
    print (ind_info['username'], ind_info['password'])
    
    [device_get_response, device_get_json] = request_get(url, (ind_info['username'], ind_info['password']))
       
    assert (device_get_response.status_code == 200 and device_get_json['status'] == 200), \
        'GET Devices response incorrect'

    for i in range (0, device_get_json['recordCount']):
                    print(device_get_json['records'][i]['name'],"-","Total links", len(device_get_json['records'][i]['links']), "No of Duplicate links-", len(find_duplicate(device_get_json['records'][i]['links'])), "links -", find_duplicate(device_get_json['records'][i]['links']))
        
    
    return

###########################################################################################################################################
main_routine(ind_info)
