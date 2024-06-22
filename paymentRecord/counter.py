import socket
import json
from datetime import datetime, timedelta
from paymentRecord import PaymentRecord


class PaymentRecord:
    def __init__(self, totalPrice, products, date):
        self.totalPrice = totalPrice
        self.products = products
        self.date = date

class Counter:
    def __init__(self):
        self.products = {"shin": 1600, "choco": 1400}
        self.paymentRecords = []
        self.cctv_records = []  # CCTV 기록을 저장할 리스트 (처음과 마지막 시간)

    def add_payment_record(self, product_names, timestamp):
        totalPrice = sum(self.products.get(name, 0) for name in product_names)
        date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        self.paymentRecords.append(PaymentRecord(totalPrice, product_names, date))

    def add_cctv_record(self, start_time, end_time):
        start_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        self.cctv_records.append((start_date, end_date))

    def display_payment_records(self):
        records_text = ""
        for record in self.paymentRecords:
            records_text += f"Date: {record.date}, Products: {record.products}, Total Price: {record.totalPrice}\n"
        return records_text

    def check_payment_times(self):
        mismatched_times = []
        for record in self.paymentRecords:
            matched = False
            for start_time, end_time in self.cctv_records:
                if start_time <= record.date <= end_time:
                    matched = True
                    break
            if not matched:
                mismatched_times.append(record.date)
        return mismatched_times

# 서버 소켓 설정
host = 'localhost'
port = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        data = client_socket.recv(1024).decode('utf-8')
        received_data = json.loads(data)

        if 'start_time' in received_data and 'end_time' in received_data:
            start_time = received_data['start_time']
            end_time = received_data['end_time']

            # 처리된 데이터를 카운터에 추가
            counter = Counter()
            counter.add_cctv_record(start_time, end_time)

            # 불일치하는 시간대 확인
            mismatched_times = counter.check_payment_times()

            # 불일치하는 시간대를 클라이언트에게 전송
            mismatched_times_json = json.dumps({
                "mismatched_times": [time.strftime("%Y-%m-%d %H:%M:%S") for time in mismatched_times]
            })
            client_socket.sendall(mismatched_times_json.encode('utf-8'))

        client_socket.close()
