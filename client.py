import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
import json

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
FORMAT = 'utf-8'
ADDR = (HOST, PORT)

# Create TCP client socket and connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Global variables
nickname = ""
current_question = None
answered = False
timer_id = None
countdown = 10

# Thread to listen for server messages
def receive():
    global current_question
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)      
            if msg == "NICK":
                client.send(nickname.encode(FORMAT))    # Send nickname
            elif "question" in msg:
                question = json.loads(msg)          # Decode JSON question
                show_question(question)             # Show on GUI
            elif "Quiz ended" in msg:
                messagebox.showinfo("Result", msg)      # Show result popup
                window.quit()
                break
        except:
            break

# Send selected answer to server
def send_answer(option):
    global answered
    if not answered:
        client.send(option.encode(FORMAT))
        answered = True
        stop_timer()

# Send empty answer if timeout occurs
def timeout():
    global answered
    if not answered:
        client.send("".encode(FORMAT))
        answered = True

# Countdown timer logic
def update_timer():
    global countdown, timer_id
    if countdown > 0:
        timer_label.config(text=f"Time left: {countdown} sec")
        countdown -= 1
        timer_id = window.after(1000, update_timer)
    else:
        timer_label.config(text="Time's up!")
        timeout()

# Cancel timer if user answered early
def stop_timer():
    global timer_id
    if timer_id:
        window.after_cancel(timer_id)
        timer_label.config(text="Answered.")

# Display a question and set up answer buttons
def show_question(question):
    global answered, countdown
    answered = False
    countdown = 10
    q_label.config(text=question["question"])
    for i, opt in enumerate(question["options"]):
        buttons[i].config(text=opt, command=lambda o=opt[0]: send_answer(o))
    update_timer()

# Ask for nickname at the beginning
def ask_nickname():
    global nickname
    nickname = simpledialog.askstring("Nickname", "Enter your nickname:")

# --- GUI Setup ---

# Create window
window = tk.Tk()
window.title("Quiz Client")
window.geometry("500x350")

# Question label
q_label = tk.Label(window, text="Waiting for question...", wraplength=400, font=("Arial", 14))
q_label.pack(pady=20)

# Answer buttons
buttons = []
for _ in range(4):
    b = tk.Button(window, text="", width=30, height=2)
    b.pack(pady=5)
    buttons.append(b)

# Timer label
timer_label = tk.Label(window, text="Time left: 10 sec", font=("Arial", 12), fg="red")
timer_label.pack(pady=10)

# Prompt nickname and start listening
ask_nickname()
threading.Thread(target=receive).start()

# Start GUI loop
window.mainloop()
