# Guild Chat Service API

## General
This service is a Python service utilizing Flask to serve as a basic API for a messenger application. It does not take into account security, authentication, etc.

The services utilizes REST endpoints and SocketIO connections to drive most of the app. The REST endpoints are shown via the postman collection included and inside the [Endpoints](Endpoints.md), and SocketIO events are documented in the [Events](Events.md) and included lucid chart image.

## Running the Server
- Requirements
 - Install virtualenv
 - Install Python3
 - Commands
  - `virtualenv venv`
  - `source venv/bin/activate`
  - Run Server
    - `pip install -r requirements.txt`
  - Run Tests
    - `pytest tests`
    
## Documentation
[Endpoints](Endpoints.md)
[Events](Events.md)

### Interaction Flow
- Create new SocketIO client
- Client initializes a connection to the servers Socket
- Client sends REST request to login a username (This will create a new user if one does not exist)
- Optionally client GETs all users chat rooms which are active private messages
- Client sends GET request to get all existing logged in users (/users/online)
- User clicks on an online user to message
- User types message and sends message
- Client emits `create room` event with the appropriate schema
- Server creates room and emits `room created` event onto the main socket
- Clients listen for `room created` amd if the user is one of the usernames Client should create chat interfaace
- Sending Client emits a `message` event with the room
- Server receives `message` event and creates a message entry inside the DB
- Server emits `new message` event inside the room specified by the Sender
- Clients listening on room receive `new message` and can notify appropriately

### Design
I chose to utilize SocketIO here due to the nature of chatting. There are many interactions back and forth inside a chat app, and I didn't feel that REST endpoints had enough functionality for Clients to code around. The REST endpoint utilize many of Flasks advantages, and I wanted to break the code up enough in order for each Blueprint to feel like an interaction point. The blueprints felt more like microservices, but for simplicity each Blueprint stayed inside the service.

### Simplifications and Assumptions
This app made a lot of simplifications and assumptions for the sake of time. Some examples include, not utilizing Foreign keys on the models. This made it easier to not get stuck writing queries around foreign key constraints, however it eliminates a lot of the error checking required. Another simplification and assumption is that Clients and Servers inside SocketIO can successfully handle the multitude of rooms on the API. There would be millions of different chat rooms inside a production server and in no way would this implementation be able to withstand that traffic. This was my first time utilizing SocketIO outside of a small demo app, so there may be some other limitations that I am not aware of, and any suggestions would be appreciated. Overall, the API has all of the expected functionality, and is something that could be utilized as a good starting point for future projects.

### Changes With More Time
- Wrap in Docker and Docker compose
- Move off of SQLite
- Swagger for REST endpoint documentation
- Fully document SocketIO events
- GraphQL for message retrievals
- Seperate users, messages, and chat (SocketIO) into seperate microservices 


