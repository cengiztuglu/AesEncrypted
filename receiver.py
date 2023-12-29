from Crypto.Cipher import AES
import socket
import pickle
from tkinter import Tk, Text,Label, Toplevel
from PIL import Image, ImageTk
import io

decrypted_image = None  # Resmi saklamak için global değişken

def decrypt_image(encrypted_data, key):
    global decrypted_image
    
    nonce, tag, ciphertext = encrypted_data

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_image_data = cipher.decrypt_and_verify(ciphertext, tag)

    with open('received_image.jpg', 'wb') as file:
        file.write(decrypted_image_data)

    print("Resim başarıyla çözüldü.")
    decrypted_image = Image.open('received_image.jpg')
    decrypted_image.thumbnail((300, 300))  # Resmi boyutlandırma
    photo = ImageTk.PhotoImage(decrypted_image)

    return photo

def decrypt_text(encrypted_data, key):
    nonce, tag, ciphertext = encrypted_data

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)

    return decrypted_text.decode('utf-8')

def show_decrypted_data(image, text):
    top = Toplevel()
    top.title("Çözülmüş Veri")
    window_width = 400
    window_height = 350

    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2

    top.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    image_label = Label(top, image=image)
    image_label.pack()

    text_box = Text(top, height=5, width=50)
    text_box.pack()
    text_box.insert("1.0", text)

    top.mainloop()

def receive_encrypted_data():
    HOST = '127.0.0.1'
    PORT = 8910

    root = Tk()
    root.withdraw()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        while True:
            serialized_data = b''
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                serialized_data += chunk

            received_data = pickle.loads(serialized_data)
            decrypted_image = decrypt_image(received_data[0], received_data[2])  # Resmi çöz
            decrypted_text = decrypt_text(received_data[1], received_data[2])  # Metni çöz
            print("Alınan şifrelenmiş metin:", decrypted_text)
            show_decrypted_data(decrypted_image, decrypted_text)  # Çözülen resmi ve metni göster

receive_encrypted_data()
