import urequests

def notify(fcm_server_key):
  print( "notify") 
  headers = {
  "Content-Type": "application/json",
  "Authorization": "key="+fcm_server_key
  }

  payload = """{
     "message":{
       "topic" : "doorbell",
        "notification":{
          "body":"Someone is at the doorbell",
          "title":"The doorbell ringed!!"
        }
     }
  }"""

  response = urequests.post("https://fcm.googleapis.com/v1/projects/doorbell-3f305/messages:send", data=payload, headers=headers)      
  print(response.text)
notify()
