# Endpoints
This document can be utilized to view endpoints for the chat-server.

## chat
- `localhost:5000/chat`: SocketIO URL
- `localhost:5000/chat/channels/user/<user_id>`
    - GET - all private channels for an existing user
        - 200 - list of private channels
        - 400 - Bad Request if user_id doesn't exist

## users
- `localhost:5000/users/login`
    - POST - logs in existing user or creates new
        - BODY: application/json `{"username": "test"}`
    - 200 - Created User
        - Response
            ```json
            {
                "created": "Sun, 03 May 2020 00:00:00 GMT",
                "id": 2,
                "status": "online",
                "username": "daniel"
            }
            ```

- `localhost:5000/users/logout`
    - POST - logouts user
        - BODY: application/json `{"username": "test"}`
    - 200 - `Logged Out`   

- `localhost:5000/users/username/check/<username>`
    - GET - returns whether or not a username is available 
    
- `localhost:5000/users/online`
    - GET - returns list of users online
    - Response
        ```json
          {
            "online_users": [
                {
                    "created": "Sun, 03 May 2020 00:00:00 GMT",
                    "id": 1,
                    "status": "online",
                    "username": "test"
                }
            ]
          }
        ```

## messages
- `localhost:5000/messages/all`
    - GET - returns all messages unless filtered
        - params: filter_type
            - count
                - returns the last 100 messages
            - days
                - returns all messages within the last 30 days
    - Response
    ```json
        {
            "messages": [
                {
                    "channel_id": 1,
                    "created": "Sun, 03 May 2020 20:17:09 GMT",
                    "id": 1,
                    "text": "Hello!"
                },
                {
                    "channel_id": 1,
                    "created": "Sun, 03 May 2020 20:17:09 GMT",
                    "id": 2,
                    "text": "How are you?"
                },
                {
                    "channel_id": 1,
                    "created": "Tue, 24 Mar 2020 20:43:43 GMT",
                    "id": 3,
                    "text": "Hey"
                }
            ]
        }
    ```
  
- `localhost:5000/messages/from/<creator>/to/<receiver>`
    - GET - messages sent from <creator> to receiver
    - Response
    ```json
      {
        "messages": [
                {
                    "channel_id": 1,
                    "created": "Sun, 03 May 2020 20:17:09 GMT",
                    "id": 2,
                    "text": "How are you?"
                },
                {
                    "channel_id": 1,
                    "created": "Tue, 24 Mar 2020 20:43:43 GMT",
                    "id": 3,
                    "text": "Hey"
                }
            ]
        }
    ```

- `localhost:5000/messages/room/<room_name>`
    - GET - messages for a given room name
    ```json
      {
        "messages": [
                {
                    "channel_id": 1,
                    "created": "Sun, 03 May 2020 20:17:09 GMT",
                    "id": 2,
                    "text": "How are you?"
                },
                {
                    "channel_id": 1,
                    "created": "Tue, 24 Mar 2020 20:43:43 GMT",
                    "id": 3,
                    "text": "Hey"
                }
            ]
        }
    ```
