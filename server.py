import socket
import threading
import json
import random
import time

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
MIN_PLAYERS = 3     # Minimum number of players to start the quiz
TIME_LIMIT = 10     # Time limit (in seconds) for each question

# Create a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Lists and dictionaries for managing players and scores
clients = []        # Stores (connection, nickname)
scores = {}         # Maps nickname to score
questions = []      # Holds the 10 randomly selected questions

# Synchronization tools
finished_count = 0               # Number of players who finished
lock = threading.Lock()          # To protect finished_count in threads
all_done = threading.Event()     # Event to signal when all players are done

# Load 10 random questions from questions.json
def load_questions():
    with open('questions.json', 'r') as file:
        all_questions = json.load(file)
        return random.sample(all_questions, 10)

# Handle individual client in its own thread
def handle_client(conn, addr, nickname):
    global finished_count
    print(f"[NEW CONNECTION] {addr} connected as {nickname}")
    scores[nickname] = 0
    clients.append((conn, nickname))

    # Wait until enough players have joined
    while len(clients) < MIN_PLAYERS:
        time.sleep(1)

    # Send each question to the client
    for q in questions:
        question_data = json.dumps(q)               # Convert question to JSON string
        conn.send(question_data.encode(FORMAT))     # Send question
        conn.settimeout(TIME_LIMIT)                 # Set a timeout for receiving answer
        try:
            answer = conn.recv(64).decode(FORMAT).strip()   # Receive answer
        except:
            answer = ""             # If timeout or error, count as blank

        # Check correctness
        if answer == q['answer']:
            scores[nickname] += 1

    conn.settimeout(None)      # Reset timeout

     # Mark this client as finished
    with lock:
        finished_count += 1
        if finished_count == len(clients):
            all_done.set()  # Signal that all players are done

    # Wait for all players to finish
    all_done.wait()

    # Prepare final result
    max_score = max(scores.values())
    result_lines = []
    for name, score in scores.items():
        tag = " (Winner)" if score == max_score else ""
        result_lines.append(f"{name}: {score}{tag}")
    final_message = "Quiz ended.\n" + "\n".join(result_lines)
    conn.send(final_message.encode(FORMAT))     # Send results
    conn.close()


# Main server loop
def start():
    print("[STARTING] Server is starting...")
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    global questions
    questions = load_questions()

    while True:
        conn, addr = server.accept()
        conn.send("NICK".encode(FORMAT))      # Ask for nickname
        nickname = conn.recv(64).decode(FORMAT)
        thread = threading.Thread(target=handle_client, args=(conn, addr, nickname))
        thread.start()

start()
