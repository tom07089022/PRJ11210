import socket
import tqdm
import os
import pandas as pd
import matplotlib.pyplot as plt
import time

# device's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create the server socket
# TCP socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
filename = "./Student/" + filename
# convert to integer
filesize = int(filesize)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()

csvPath = './Student/focus.csv'
figPath = './Student/Focus_Chart_Img/Focus_Chart_'+time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())+'.jpg'

focuschart = pd.read_csv(csvPath, encoding = 'unicode_escape')

plt.style.use("ggplot")
plt.figure(figsize=(10, 5))
plt.plot(focuschart["Time (min)"], focuschart["Focus Degree (%)"], c = "b")  

plt.legend(labels=["Time (min)", "Focus Degree (%)"], loc = 'best')
plt.xlabel("Time (min)", fontweight = "bold")
plt.xticks(rotation=45)
plt.ylabel("Focus Degree (%)", fontweight = "bold")
plt.ylim(-5,110)
plt.yticks(range(0, 110, 10))
plt.title("Realtime Focus Analysis Line Chart", fontsize = 16, fontweight = "bold")
plt.savefig(figPath, bbox_inches='tight', pad_inches=0.0)
plt.show()

plt.close()