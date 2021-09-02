import sys
import struct
import socket

class Connection:


    def __init__(self, socket):
        self.socket = socket

    def _recvAll(self, bufferSize):
        """Given a buffer size, socket will go through a loop and continue
        to read from the buffer until the length of the data read matches
        the stated buffersize."""
        data = b''
        while sys.getsizeof(data) < bufferSize:
            received = self.socket.recv(bufferSize - sys.getsizeof(data))
            data += received
        return data



    def _sendData(self, info):
        """Works in conjunction with _recvData. Sends information to other party,
        telling them how long the data it is going to send is. After receiving
        an acknowledgement from the other party, will proceed to send all of
        the data to other party."""
        if type(info) == str:
            info = info.encode()
        size = sys.getsizeof(info)
        sizeInfo = struct.pack('i', size)
        self.socket.sendall(sizeInfo)
        response = self._recvAll(45) #expect server to send back encoded string "Got the size"
        if response.decode() == "Got the size":
            self.socket.sendall(info)



    def _recvData(self):
        """Works in conjunction with _sendInfo. Will wait to receive data that
        dictates how much of the buffer needs to be read to receive the message
        the other party is trying to send. Acknowledges the receiving of the
        size-data and will wait to read that amount from the buffer"""
        packedSize = self._recvAll(37)
        bufferSize, = struct.unpack('i', packedSize)
        self.socket.sendall("Got the size".encode())
        info = self._recvAll(bufferSize)
        return info
