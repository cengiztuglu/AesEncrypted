from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from tkinter import Tk, Button,filedialog, Text
import socket
import pickle

def encrypt_image(input_file, key):
    with open(input_file, 'rb') as file:
        image_bytes = file.read()
    
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(image_bytes)
    
    return cipher.nonce, tag, ciphertext

def encrypt_text(plain_text, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode('utf-8'))
    return cipher.nonce, tag, ciphertext

def send_encrypted_data(image_data, text_data, key):
    HOST = '127.0.0.1'
    PORT = 8910
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        serialized_data = pickle.dumps((image_data, text_data, key))
        s.sendall(serialized_data)
        print("Şifrelenmiş resim ve metin gönderildi.")

def on_button_click():
    root = Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename() 
    
    if file_path:
        key = get_random_bytes(16)
        
        # Resmi şifrele ve gönder
        encrypted_image_data = encrypt_image(file_path, key)
        
        # TextBox'tan metni al
        text = text_box.get("1.0", "end-1c")
        
        # Metni şifrele
        encrypted_text_data = encrypt_text(text, key)
        
        # Resmi ve metni gönder
        send_encrypted_data(encrypted_image_data, encrypted_text_data, key)
        print("Şifrelenmiş veri:", encrypted_image_data)

# Buton oluştur
root = Tk()
root.title("Resmi ve Metni Şifreli Gönder")
window_width = 400
window_height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

text_box = Text(root, height=5, width=50)
text_box.pack()

button = Button(root, text="Resim Seç ve Gönder", command=on_button_click)
button.pack()

root.mainloop()
y