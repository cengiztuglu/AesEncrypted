import socket
from Crypto.Cipher import AES
import pickle
from tkinter import Tk, Label
from PIL import Image, ImageTk

def decrypt_image(encrypted_data, key):
    nonce, tag, ciphertext = encrypted_data
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_image = cipher.decrypt_and_verify(ciphertext, tag)
    
    with open('received_image.jpg', 'wb') as file:
        file.write(decrypted_image)
    
    print("Resim başarıyla çözüldü.")
    show_decrypted_image('received_image.jpg')

def receive_encrypted_image():
    HOST = '127.0.0.1'
    PORT = 8910
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f'{addr} tarafından bağlantı sağlandı')
         
            serialized_data = b''  
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                serialized_data += chunk
            
            received_data = pickle.loads(serialized_data)
            decrypt_image(*received_data)

def show_decrypted_image(image_path):
    root = Tk()
    root.title("Çözülmüş Resim")
    window_width = 400
    window_height = 300

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    label = Label(root, image=photo)
    label.image = photo
    label.pack()

    root.mainloop()

# Program başladığında resmi çözüp göster
receive_encrypted_image()
