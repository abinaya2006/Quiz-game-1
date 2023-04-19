import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address ='127.0.0.1'
port =8000

server.bind((ip_address,port))
server.listen()
clients=[]

questions =[
    "What is the Italian word for PIE? \n a.Mozarella\n b.Pasty\n c.Patty\n d.Pizza",
    "Hg stands for? \n a.Mercury\n b.Hulgerium\n c.Argenine\n d.Halfnium",
    "The chief constituent of gobar gas is \n a.ethane\n b.methane\n c.hydrogen\n d.carbon dioxide",
    "Hitler party which came into power in 1933 is known as \n a.Labour Party\n b.Nazi Party\n c.Ku-Klux-Klan\n d.Democratic Party",
    "Entomology is the science that studies\n a.The origin and history of technical and scientific terms\n b.Behavior of human beings\n c.Insects\n d.The formation of rocks",
    "The beaver is the national embelem of which country? \n a.Zimbabwe\n b.Iceland\n c.Argentina\n d.Canada",
    "Which planet is closest to the sun?\n a.Mercury\n b.Pluto\n c.Earth\n d.Venus"
    "What is the currency of Japan?\n a.Yen\n b.Yuan\n c.Rupee\n d.Dollar"
]

answers=['d','a','b','b','c','d','a','a']

print("Server has started...")

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions))
    random_que = questions[random_index]
    random_ans = answers[random_index]
    conn.send(random_que.encode('utf-8'))
    return random_index,random_que,random_ans

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def remove(conn):
    if conn in clients:
        clients.remove(conn)


def clientThread(conn):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one of a, b, c or d\n".encode('utf-8'))
    conn.send("Good Luck:)!\n\n".encode('utf-8'))

    index,que,ans = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue



while True:
    conn,addr = server.accept()
    clients.append(conn)
    print (addr[0] + " connected")
    new_thread = Thread(target= clientThread,args=(conn))
    new_thread.start()