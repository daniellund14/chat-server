# SocketIO events for Chat application (SENDER)
  - message - send message to room (CLIENT)
    ```json
        {
         "room": "daniel_dylan",
          "from": "daniel",
          "to": "dylan",
          "text": "Hello"
        }
    ```
 - create room - create new room for two users (CLIENT)
    ```json
    {
      "room": "daniel_dylan",
      "user_id_1": 1,
      "user_id_2": 2
    }
    ```
   
- create username - create a new user (CLIENT)
    ```json
      {
        "username": "test"
      } 
    ```

 - new message - new message received (SERVER)
    ```json
     {"display_text": "Daniel: Hello"}
    ```
      
- room created - room successfully created (SERVER)
    ```json
      {
          "room": "daniel_val",
          "user_id_1": 2,
          "user_id_2": 5
       }
    ```

- room exists - room trying to be created exists (SERVER)
    ```json
      {
          "msg": "room you are trying to create already exists",
          "room": {
            "id": 2,
            "uuid": "0c493bc1-1a68-46e1-8f15-133c87d7376e",
            "room": "daniel_lauren",
            "user_1": 2,
            "user_2": 1
          }
      }
    ```
- message error - message failed to post
    ```json
      {
        "msg": "new message failed to post",
        "reason": "message missing fields"
      }
    ```
