import socket
import pyaudio
import select
import threading
# from beepy import beep
import sys
import os
import simpleaudio as sa
from multiprocessing import Process

speaker = 0
enable_tone = 1

class AudioSender:

    def __init__(self, host, port, audio_format=pyaudio.paInt32, channels=1, rate=44100, frame_chunk=800):
        self.__host = host
        self.__port = port

        self.__audio_format = audio_format
        self.__channels = channels
        self.__rate = rate
        self.__frame_chunk = frame_chunk

        self.__sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__audio = pyaudio.PyAudio()

        self.__running = False
        self.__connect = False

    #
    # def __callback(self, in_data, frame_count, time_info, status):
    #     if self.__running:
    #         self.__sending_socket.send(in_data)
    #         return (None, pyaudio.paContinue)
    #     else:
    #         try:
    #             self.__stream.stop_stream()
    #             self.__stream.close()
    #             self.__audio.terminate()
    #             self.__sending_socket.close()
    #         except OSError:
    #             pass # Dirty Solution For Now (Read Overflow)
    #         return (None, pyaudio.paComplete)

    def start_stream(self):
        if self.__running:
            print("Already streaming")
        else:
            self.__running = True
            thread = threading.Thread(target=self.__client_streaming)
            thread.start()

    def stop_stream(self):
        if self.__running:
            self.__running = False
        else:
            print("Client not streaming")

    def __client_streaming(self):
        self.__sending_socket.connect((self.__host, self.__port))
        self.__stream = self.__audio.open(format=self.__audio_format, channels=self.__channels, rate=self.__rate, input=True, frames_per_buffer=self.__frame_chunk)
        while self.__running:
            # conn, addr = self.__sending_socket.accept()
            # with conn:
            #      print(f"Connected by {addr}")
            self.__sending_socket.send(self.__stream.read(self.__frame_chunk))


class AudioReceiver:

    def __init__(self, host, port, slots=8, audio_format=pyaudio.paInt32, channels=1, rate=44100, frame_chunk=800):
        self.__host = host
        self.__port = port
        self.tone_started = False
        self.thread2 = None

        self.__slots = slots
        self.__used_slots = 0

        self.__audio_format = audio_format
        self.__channels = channels
        self.__rate = rate
        self.__frame_chunk = frame_chunk

        self.__audio = pyaudio.PyAudio()

        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server_socket.bind((self.__host, self.__port))
        
        self.__block = threading.Lock()
        self.__running = False

        self.__client = None
        self.AUDIO_DIR = self.resource_path("assets")


    def check_client(self):
        if(self.__client):
            try:
                self.__client.settimeout(3)
                data = self.__client.send("1".encode())
                # print(data)
                print("yes done")
                return True, self.tone_started
            except Exception as e:
                print("check_client Exception: " , e)
                self._run = False
                return False , False
        return False, False
    
    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def alert(self):
        wave_obj_file = "short_.wav"
        WAVE_PATH = os.path.join(self.AUDIO_DIR, wave_obj_file)
        wave_obj = sa.WaveObject.from_wave_file(WAVE_PATH)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    def Tone(self, n):
        for i in range(n):
            self.alert()
            # beep(sound=1)


    def is_socket_closed(self) -> bool:
        try:
            
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = self.__server_socket.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception as e:
            return False
        return False

    def isRunning(self):
        return self.__running

    def start_server(self):
        if self.__running:
            print("Audio server is running already")

        else:
            self.__running = True
            self.__stream = self.__audio.open(format=self.__audio_format, channels=self.__channels, rate=self.__rate, output=True, frames_per_buffer=self.__frame_chunk)
        
            self.thread = threading.Thread(target=self.__server_listening, daemon=True)
            self.thread.start()

    def getRunning(self):
        return self.__running

    def __server_listening(self):
        global speaker, enable_tone
        self.__server_socket.listen()
        # print("running : " + str(self.__running))
        while self.__running:
            # print("waiting for client")
            # if (speaker):
                self.__block.acquire()
                connection, address = self.__server_socket.accept()
                self.tone_started = False
                self.__client = connection

                self.__block.release()

                try:
                    tone = connection.recv(1024).decode()
                    # print("tone: ", tone)
                    if (tone=="#"): self.Tone(2)
                except Exception as e:
                    print("Exception tone:  " , e)
                    self.Tone(2)

                self.tone_started = True
                self._run = True
                # if (self.thread2): print("thread 2 is alive :" , self.thread2.is_alive())
                # self.process = Process(target=self.__client_connection, args=(connection, address,), daemon=True)
                # self.process.start()
                self.thread2 = threading.Thread(target=self.__client_connection, args=(connection, address,), daemon=False)
                self.thread2.start()

    def __client_connection(self, connection, address):
        while self._run:
            try:
                if (connection):
                    # print("connection : ", connection)
                    data = connection.recv(self.__frame_chunk)
                    # print("data : ", data)
                    self.__stream.write(data)
                    # print("streaming... ")
            except Exception as e: 
                print("__client_connection Exception: " , str(e))
                self.__client = None
                break
                # self.__running = False
        print("Finish ------")

    def stop_server(self):
        if self.__running:
            self.__running = False
            # closing_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # closing_connection.connect((self.__host, self.__port))
            # closing_connection.close()
            # self.__block.acquire()
            # self.__server_socket.close()
            # self.__block.release()
        else:
            print("Server not running!")


class ServerConnection:

    def __init__(self, host, port):
        self.__host = host
        self.__port = port

        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server_socket.bind((self.__host, self.__port))
        
        self.__block = threading.Lock()
        self.__running = False
        self.__client = None
        self.__speaker = 0
        self.room = ""

    def get_room(self):
        return self.room
    
    def set_speaker(self, sp):
        global speaker
        self.__speaker = sp
        speaker = sp

    def set_tone(self, tone):
        global enable_tone
        enable_tone = tone

    def start_server(self):
        self.__server_socket.listen()
        thread = threading.Thread(target=self.listening, daemon=True)
        thread.start()

    def listening(self):
        global speaker, enable_tone
        while True:
            # print("waiting for speaker client")
            # self.__block.acquire()
            try:
                connection, address = self.__server_socket.accept()

                # print("connected === " + str(address))

                # self.__block.release()

                if (connection):
                    self.connection_result = connection.recv(1024).decode()
                    # print("connection_result : ", self.connection_result)
                    if (':' in self.connection_result):
                        if (self.connection_result.split(":")[0]!="-"):
                            self.room = self.connection_result.split(":")[0]
                        self.enable_tone = int(self.connection_result.split(":")[1])
                    else:
                        self.room = self.connection_result
                        # self.enable_tone = 1
                    # print("room: ", self.room)
                    # print("enable_tone: ", self.enable_tone)
                    data = str(speaker).encode()
                    connection.send(data)
                    # print("data sent : " + str(speaker))
                    connection.close()
            except Exception as e:
                print("listening Exception: " , e)
        


class ClientConnection:

    def __init__(self, host, port):
        self.__host = host
        self.__port = port

        self.__client_socket = socket.socket()
    
        
        self.__block = threading.Lock()
        self.__running = False
        self.__client = None
        self.__speaker = 0

    def start_request(self):
        self.__client_socket.connect((self.__host, self.__port))
        data = self.__client_socket.recv(1024).decode()
        # print ("speaker: " , data)
        self.__client_socket.close() 
        return data