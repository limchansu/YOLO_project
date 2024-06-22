import socket
import json
import threading
from counter import Counter
from counter_ui import CounterUI
import tkinter as tk

def start_server(counter):
    host = 'localhost'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Server started. Waiting for connections...")

        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                if not data:
                    break
                data = json.loads(data.decode('utf-8'))
                if "products" in data:
                    products = data["products"]
                    timestamp = data["timestamp"]
                    counter.add_payment_record(products, timestamp)
                    print("Payment record added:", products, timestamp)
                elif "cctv_start_time" in data and "cctv_end_time" in data:
                    cctv_start_time = data["cctv_start_time"]
                    cctv_end_time = data["cctv_end_time"]
                    counter.add_cctv_record(cctv_start_time, cctv_end_time)
                    print("CCTV record added:", cctv_start_time, cctv_end_time)

def run_server(counter):
    server_thread = threading.Thread(target=start_server, args=(counter,))
    server_thread.daemon = True
    server_thread.start()

if __name__ == "__main__":
    counter = Counter()

    root = tk.Tk()
    app = CounterUI(root, counter)
    root.mainloop()

    run_server(counter)