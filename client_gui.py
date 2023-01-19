import tkinter as tk
from tkinter import messagebox
import socket
import threading
import rsa





window = tk.Tk()
window.title("Client")
username = ""
topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Name:").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)
btnConnect = tk.Button(topFrame, text="Connect", command=lambda : connect())
btnConnect.pack(side=tk.LEFT)
#btnConnect.bind('<Button-1>', connect)
topFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="*********************************************************************").pack()
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="blue")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)



bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)

# The client frame shows the client area

# clientFrame = tk.Frame(window)
# lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
# scrollBar = tk.Scrollbar(clientFrame)
# scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
# clients_Display=tk.Text(clientFrame, height=15, width=30)
# clients_Display.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
# scrollBar.config(command=clients_Display.yview)
# clients_Display.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
# clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))
def connect():
    global username, client
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        username = entName.get()
        connect_to_server(username)


# network client
client = None
HOST_ADDR = "172.27.64.1"
HOST_PORT = 8080

def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        server_public_key = rsa.PublicKey.load_pkcs1(client.recv(1024))
        client.send(public_key.save_pkcs1("PEM"))
        client.send(rsa.encrypt(name.encode().server_public_key) # Send name to server after connecting

        entName.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)

        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")

#list of alll conected clients
name_list=[]
def update_client_names_display(name_list):
    clients_Display.config(state=tk.NORMAL)
    clients_Display.delete('1.0', tk.END)

    for c in name_list:
        clients_Display.insert(tk.END, c+"\n")
    clients_Display.config(state=tk.DISABLED)

def receive_message_from_server(sck, m):
    while True:
        from_server = rsa.decrypt(sck.recv(1024), private_key).decode())
        if not from_server: break
        # display message from server on the chat window

        # enable the display area and insert the text and then disable.
        # why? Apparently, tkinter does not allow us insert into a disabled Text widget :(
            texts = tkDisplay.get("1.0", tk.END).strip()
            tkDisplay.config(state=tk.NORMAL)
            if len(texts) < 1:
                tkDisplay.insert(tk.END, from_server)
            else:
                tkDisplay.insert(tk.END, "\n\n"+ from_server)

            tkDisplay.config(state=tk.DISABLED)
            tkDisplay.see(tk.END)

        # print("Server says: " +from_server)

    sck.close()
    window.destroy()


def getChatMessage(msg):

    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()

    # enable the display area and insert the text and then disable.
    # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
    tkDisplay.config(state=tk.NORMAL)
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message") # no line
    else:
        tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")

    tkDisplay.config(state=tk.DISABLED)

    send_mssage_to_server(msg)

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)


def send_mssage_to_server(msg):
    client_msg = str(msg)
    client.send(rsa.encrypt(client_msg)server_public_key.encode())
    if msg == "exit":
        client.close()
        window.destroy()
    print("Sending message")





window.mainloop()
