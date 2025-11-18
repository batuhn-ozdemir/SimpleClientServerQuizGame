Project Description : 
 This project is a multiplayer real-time quiz game implemented in Python using TCP
 sockets and GUI-based clients built with Tkinter. The server manages multiple clients,
 broadcasts quiz questions, receives answers, calculates scores, and announces the winner(s).
 
 Technologies Used : 
 • Python 3.x
 • socket, threading, json modules
 • Tkinter for GUI
 
 System Workflow : 
 1. Server Initialization
 The server is started using python3 server.py. It begins listening on localhost.
 2. Client Nickname Input
 Each client runs client.py and is prompted to enter a nickname before joining the game.
 3. Server Receives Client Connections
 The server logs each connection and assigns the provided nickname.
 4. Quiz Questions Broadcast
 Once the minimum number of players (3) connect, the server broadcasts questions. Each
 client receives the same question simultaneously with a 10-second timer.
 5. Final Scores and Winners
 After all players complete the quiz, final scores are sent to each client and also displayed
 on the server terminal. Players with the highest score are marked as (Winner).

How to Run : 
 1. Run the server:
 python3 server.py
 2. Run at least 3 clients:
 python3 client.py
 3. Enter nickname when prompted.
 4. Answer questions within 10 seconds per question.
 5. Wait until the quiz ends and scores are displayed.

 Conclusion
 This project demonstrates real-time network programming with concurrency, GUI inte
gration, and synchronization in a multiplayer environment using Python sockets.
