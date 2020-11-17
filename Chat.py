'''


@author: omar kalbouneh
'''

import requests
import tkinter

root = tkinter.Tk()
root.title('Chat')
root.configure(width = 600, height = 425, background = 'lightyellow')
url = 'https://posthere.io/35a6-46f7-acfe'

#Field for sender----------------------------------------------------
senderUsername = ""
def sender_pushed():
    #manipulate the global variable
    global senderUsername
    senderUsername = sender_field.get() #button extracts textfield input
    
#button to extract sender username
senderButton = tkinter.Button(root, text="Please type your username and click this button" , font = ("Calibri" , 8) , command = sender_pushed)
senderButton.place(relx = 0.24 , rely = 0.03 , anchor = tkinter.CENTER)

#field to type the sender's username
sender_field = tkinter.Entry(root)
sender_field.place(relx = 0.154 , rely = 0.11 , anchor = tkinter.CENTER)

#field for receiver---------------------------------------------------
receiverUsername = ""
def receiver_pushed(): 
    #manipulate the global variable
    global receiverUsername
    receiverUsername = receiver_field.get()
    
#button to extract the reciever's username (person that the message will be sent to)
receiverButton = tkinter.Button(root, text="Please type the other user's username and click this button" , font = ("Calibri" , 8) , command = receiver_pushed)
receiverButton.place(relx = 0.75 , rely = 0.03 , anchor = tkinter.CENTER)
  
#field to type the reciever's username
receiver_field = tkinter.Entry(root)
receiver_field.place(relx = 0.618 , rely = 0.11 , anchor = tkinter.CENTER)

#Title-------------------------------------------------------------------
label = tkinter.Label(root , text = "Welcome to the chat room!")
label.place(relx = 0.47 , rely = 0.2 , anchor = tkinter.CENTER)

#Field to send a message-------------------------------------------------

#sends and displays the meassage and the corresponding time
def send_message():
    global message
    message = send_field.get()
    global senderUsername
    sender_pushed() #calls the function to access the new global variable (typed sender username)
    myObj = {senderUsername: message}
    requests.post(url , data = myObj) #posts
    
    #gets  it and displays it
    response = requests.get(url , headers={'Accept': 'application/json'})
    json_response = response.json()
    time = json_response[0]['timestamp']
    exact_time = time[11:16] #parses over the string to only post the time
    
    display_message(message , exact_time) #function call for display
    
#button to send and post a message and extracts what was typed in the field
sendButton = tkinter.Button(root , text = "Send Message" , font = ("Calibri" , 8) , command = send_message  )
sendButton.place(relx = 0.65 , rely=0.9 , anchor = tkinter.CENTER)  

#field to type the message as an input
send_field = tkinter.Entry(root)
send_field.place(relx = 0.47 , rely = 0.9 , anchor= tkinter.CENTER)  
   
#Displays the messages sent on the right hand corner and the time underneath it

messageRoom = 0.8 #space between messages
def display_message(sent , time):
    #if the user sends more than one message, then the messages will be stacked above each other
    global messageRoom
    #Guarantees that messages won't go out of bounds
    if(messageRoom >= 0.2):
        #displays messages on top of each other
        disp_message = tkinter.Label(root , text = sent , font =('Helvatica' , 9))
        disp_message.place(relx = 0.75 ,  rely = messageRoom , anchor = tkinter.CENTER)
        
        #time of each message sent
        disp_time = tkinter.Label(root , text = time , font=('Helvatica' , 7))
        disp_time.place(relx = 0.95 , rely = messageRoom + 0.05 , anchor = tkinter.CENTER)
        messageRoom = messageRoom - 0.07 #make space for new messages
        
#field to clear the chat and quit   
def clear_chat():
    requests.delete(url)
     
quitButton = tkinter.Button(root , text ="Quit" , font=("Calibri" , 8) , command = clear_chat) 
quitButton.place(relx = 0.87 , rely = 0.11 , anchor = tkinter.CENTER)

#Updates and gets chat by the other user---------------------------------------
def update():
    response = requests.get(url , headers={'Accept': 'application/json'})
    json_response = response.json()
    length = len(json_response)
     
    i = 0
    while i < length:
        global receiverUsername
        receiver_pushed()
        newMessage = json_response[i]['body'][receiverUsername] #only reads messages with specific username
        time = json_response[i]['timestamp']
        exactTime = time[11:16]
        display_received_message(newMessage , exactTime)
        i = i + 1

updateButton = tkinter.Button(root , text = "Update" , font=("Calibri" , 8) , command = update)
updateButton.place(relx = 0.3 , rely = 0.9 , anchor = tkinter.CENTER)

messageSpace = 0.8
def display_received_message(message1 , time):
    #stack messages on top of one another
    global messageSpace
    #Guarantees messages won't go out of bounds
    if(messageSpace >= 0.2):
        #stacks messages
        disp_message = tkinter.Label(root , text = message1 , font=('Helvetica' , 9))
        disp_message.place(relx = 0.25 , rely = messageSpace , anchor = tkinter.CENTER)
        
        #time of each message sent
        disp_time = tkinter.Label(root, text = time , font = ('Helvetica' , 7))
        disp_time.place(relx = 0.05 , rely = messageSpace + 0.05 , anchor = tkinter.CENTER)
        messageSpace = messageSpace - 0.07

root.mainloop()        
            
      
        



