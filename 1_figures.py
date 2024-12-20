
import threading
import time
import random

class Printer:
    def __init__(self):
        self.lock = threading.Lock()
    
    def print_ticket(self, client_id):
        with self.lock:
            print(f"Printer started printing ticket for Client {client_id}.")
            time.sleep(random.uniform(0.5, 1.5))  # Simulate printing time
            print(f"Printer finished printing ticket for Client {client_id}.")

class TicketingWindow:
    def __init__(self, printer):
        self.lock = threading.Lock()
        self.printer = printer
    
    def serve_client(self, client_id):
        with self.lock:
            print(f"Ticketing Window is serving Client {client_id}.")
            time.sleep(random.uniform(1, 2))  # Simulate serving time
            self.printer.print_ticket(client_id)
            print(f"Client {client_id} has left the ticketing window.")

class Client(threading.Thread):
    def __init__(self, client_id, ticketing_window):
        threading.Thread.__init__(self)
        self.client_id = client_id
        self.ticketing_window = ticketing_window
    
    def run(self):
        print(f"Client {self.client_id} is arriving at the ticketing window.")
        self.ticketing_window.serve_client(self.client_id)

def main():
    printer = Printer()
    windows = [TicketingWindow(printer) for _ in range(2)]  # 2 ticketing windows
    clients = [Client(client_id, windows[client_id % 2]) for client_id in range(6)]  # 6 clients

    for client in clients:
        client.start()  # Start all client threads

    for client in clients:
        client.join()  # Wait for all client threads to finish

if __name__ == "__main__":
    main()