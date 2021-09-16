import sys
import struct
import socket

class Connection:
    
    def __init__(self, socket):
        self.socket = socket


    def _recvAll(self, bufferSize) -> str:
        data = b''
        while sys.getsizeof(data) < bufferSize:
            received = self.socket.recv(bufferSize - sys.getsizeof(data))
            data += received
        return data


    def _sendData(self, dataToSend) -> None:
        if type(dataToSend) == str:
            dataToSend = dataToSend.encode()
        size = sys.getsizeof(dataToSend)
        sizeInfo = struct.pack('i', size)
        self.socket.sendall(sizeInfo)
        response = self._recvAll(45) #expect recipient to send back encoded string "Got the size"
        if response.decode() == "Got the size":
            self.socket.sendall(dataToSend)


    def _recvData(self) -> str:
        packedSize = self._recvAll(37) #size of sizeInfo sent by _sendData
        bufferSize, = struct.unpack('i', packedSize)
        self.socket.sendall("Got the size".encode())
        info = self._recvAll(bufferSize)
        return info
