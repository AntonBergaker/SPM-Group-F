import socket
import queue
import threading
import pickle
from communication.server import PORT, CommunicationMessage, NetworkData


class Client:
    def __init__(self, player_name, server_ip):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._player_name = player_name
        self._read_queue = queue.Queue()
        self._write_queue = queue.Queue()
        self._server.connect((server_ip, PORT))

        # Start read thread
        threading.Thread(target=self._read_server, daemon=True).start()

        # Start write thread
        threading.Thread(target=self._write_server, daemon=True).start()

        self._server.sendall(pickle.dumps(player_name))

    def read(self):
        """
        Used to read income data to the client. If no data is received the thread waits until data is received.
        Data is read as first in, first out
        :return: Data that have arrived from the server
        """
        return self._read_queue.get()

    def write(self, data):
        """
        Used to send data to the server
        :data The NetworkData that are to be sent
        :return: None
        """
        return self._write_queue.put(data)

    def _read_server(self):
        while True:
            try:
                raw_data = self._server.recv(4096)
                if not raw_data:
                    self._read_queue.put(NetworkData(
                        None, CommunicationMessage.SERVER_DISCONNECTED))
                    return
                data = pickle.loads(raw_data)
                # Do something with data
                self._read_queue.put(data)
            except:
                return

    def _write_server(self):
        while True:
            data = self._write_queue.get()
            if not data:
                return
            raw_data = pickle.dumps(data)
            self._server.sendall(raw_data)

    def end(self):
        self.write(None)
        self._server.close()
