import requests


BASE_URL = "http://127.0.0.1:5000/"

#### THIS DATA CAN BE GATHERED THROUGH FRONTEND VIA A FORM ETC

song_data = """ {"type" : "song", "data" : {"name" : "The Box" ,"duration" : "4435" , "upload_time" : "01/03/2021 06:20:11 PM"}} """
audiobook_data = """ {"type" : "audiobook", "data" : {"name" : "damn son" ,"duration" : "4214435" , "upload_time" : "01/03/1921 06:20:11 PM", "author" : "Jordan Peterson", "narrator" : "Jordan Peterson"}} """
podcast_data = """ {"type" : "podcast", "data" : {"name" : "Andrew Schulz" ,"duration" : "68935" , "upload_time" : "01/03/1021 06:20:11 PM" , "host" : "Joe Rogan", "participants" : ""}} """


### CREATE REQUEST ARE CALLED AT THE BASEURL + "CREATE"
### THE DATA IS PASSED AN ARG CALLED 'json'
### DELETE UPDATE AND GET ARE CALLED THROUGH BASEURL + "<aduioFileType>/<audioFileID>"
### FOR GET, ID IS OPTIONAL


### ------------ PUT -------------###
#response = requests.put(BASE_URL+"upload" ,json = audiobook_data )



### ------------ GET -------------###
#response = requests.get(BASE_URL + "audiobook/")
#response = requests.get(BASE_URL + "audiobook/2")



### ------------ PATCH -------------###
#response = requests.patch(BASE_URL + "song/4",json = song_data)



### ------------ DELETE -------------###
#response = requests.delete(BASE_URL + "song/4")



### ------------ PRINTING RESPONSE ---------###
#print(response.json())
