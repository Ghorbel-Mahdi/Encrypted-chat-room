import tkinter as tk
import socket
import threading

class Client:
    def __init__(conn,adress, pk: object):
        self.conn=conn
        self.adress=adress
        self.pk=pk

    def __init__(conn, adress):
        self.name = ""
        self.adress = adress
    def send():
        pass
    def set_pk(pk):
        self.pk=pk
    def set_name(name):
        self.name=name


window = tk.Tk()
window.title("Sever")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Connect", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay=tk.Text(clientFrame,height=15,width=30)
tkDisplay.pack(side=tk.LEFT,fill=tk.Y,padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
HOST_ADDR = "172.27.64.1"
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []
public_key, private_key = rsa.newkeys (1024)
public_partner = None

# Start server function
def start_server():

    global server, HOST_ADDR, HOST_PORT # code is fine without this
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Host: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(the_server, y):
    while True:
        conn, addr = the_server.accept()
        conn.send(public_key.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(conn.recv(1024))
        client = Client(conn, addr,public_partner)
        clients.append(client)

        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_client_message, (client,))


# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client:Client):
    global server, client_name, clients, clients_addr
    client_msg = " "

    # send welcome message to client
    client_name  = client.conn.recv(4096).decode()
    client.set_name(client_name)
    welcome_msg = "Welcome " + client.name + ". Use 'exit' to quit"
    client.conn.send(welcome_msg.encode())
    client.conn.send(client_name.encode())

    clients_names.append(client_name)

    update_client_names_display(client)  # update client names display


    while True:
        data = rsa.decrypt((client.conn.recv(4096),private_key).decode())
        if not data: break
        if data == "exit": break

        client_msg = data

        idx = get_client_index(clients, client.conn)
        sending_client_name = clients_names[idx]

        for c in clients:
            if c.conn != client_connection:
                server_msg = str(c.name + "->" + client_msg)
                c.conn.send(rsa.encrypt(server_msg.encode(),c.pk))

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    server_msg = "BYE!"
    client.conn.send(rsa.encrypt(server_msg.encode(),client.pk)))
    clien.conn.close()

    update_client_names_display(clients_names)  # update client names display


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()