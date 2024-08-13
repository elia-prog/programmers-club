import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 9090))

while True:
    print("Choose what you want to do:")
    print("1: to upload file")
    print("2: to download file")
    x = input("Enter your choice here -> ")
    
    s.send(x.encode())
    
    if x == '1':
        file = input("Enter your file location here -> \n")
        s.send(file.encode())
        print("File uploaded successfully!")
        
    elif x == '2':
        name = input("Enter the file name you want to download -> \n")
        s.send(name.encode())
        
        # First, receive the file size
        file_size = int(s.recv(1024).decode())
        
        with open("downloaded_" + name, "wb") as f:
            total_received = 0
            while total_received < file_size:
                bytes_read = s.recv(1024)
                if not bytes_read:
                    break
                f.write(bytes_read)
                total_received += len(bytes_read)
                
        print("File downloaded successfully to 'C:\Users\User' ")

s.close()
