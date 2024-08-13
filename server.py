import socket
import os
import shutil

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "127.0.0.1"
port = 9090
s.bind((ip, port))
s.listen(6)

print("Server is listening")
connection, address = s.accept()

while True:
    received_message = connection.recv(1024).decode()
    
    if received_message == '1':
        source_path = connection.recv(1024).decode()
        destination_folder = "C:/Users/User/OneDrive/שולחן העבודה/server/"
        file_name = os.path.basename(source_path)
        destination_path = os.path.join(destination_folder, file_name)
        shutil.copy(source_path, destination_path)
        print(f"File {file_name} uploaded to server successfully!")

    elif received_message == '2':
        file_name = connection.recv(1024).decode()
        file_path = "C:/Users/User/OneDrive/שולחן העבודה/server/" + file_name
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            connection.send(str(file_size).encode())  # Send file size first
            with open(file_path, "rb") as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    connection.sendall(bytes_read)
            print(f"File {file_name} sent to client successfully!")
        else:
            connection.send(b"File not found")

connection.close()
s.close()
