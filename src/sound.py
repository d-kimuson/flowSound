from scipy import *
import pyaudio
import wave
import sys
import time

path = "/Users/kaito/Apps/flowSound/src/static/strings.wav"

class Player:
    def __init__(self, path=path):
        self.task =  None
        self.path = path
        self.p = pyaudio.PyAudio()
        self.chunk = 1024
        self.isstart = False
        self.prepare()

    def prepare(self):
        self.wf = wave.open(self.path, "rb")
        self.stream = self.p.open(format =
                    self.p.get_format_from_width(self.wf.getsampwidth()),
                    channels = self.wf.getnchannels(),
                    rate = self.wf.getframerate(),
                    output = True
                    )
        self.origin_data = self.wf.readframes(self.chunk)
        self.data = self.wf.readframes(self.chunk)
        self.current_speed = 1.0

    def setTask(self, *task):
        """
        - play
        - pause(save position)
        - stop(go_start)
        - change_speed mag
        """
        print("setTask is called!")
        print(task)
        if task[0] in ["play", "pause", "stop", "change_speed"]:
            self.task = task
        if not self.isstart and self.task[0] == "play":
            self.isstart = True
            self.play()


    def pause(self):
        while(True):
            if self.task is None:
                continue
            elif self.task[0] == "play":
                self.task = None
                break
            elif self.task[0] == "change_speed":
                self.changePlaySpeed(self.task[1])
                self.task = None

    def stop(self):
        self.data = self.current_data
        self.pause()

    def play(self, firstrate=1.0):
        self.changePlaySpeed(firstrate)
        while len(self.data) > 0:
            self.stream.write(self.data)
            self.data = self.wf.readframes(self.chunk)
            self.data = frombuffer(self.data, dtype = "int16")
            if self.task is None:
                pass
            elif self.task[0] == "pause":
                self.task = None
                self.pause()
            elif self.task[0] == "stop":
                self.task = None
                self.stop()
            elif self.task[0] == "change_speed":
                self.changePlaySpeed(self.task[1])
                self.task = None
        self.data = self.current_data
        self.instart = False

    def changePlaySpeed(self, rate):
        print("changePlaySpeed is called")
        print(f"curren_speed -> {self.current_speed}")
        print(f"new_rate -> {rate}")
        outp = []
        rate = rate / self.current_speed
        self.current_speed = rate
        print(f"sp_rate -> {rate}")
        for i in range(int(len(self.data) / rate)):
            outp.append(self.data[int(i * float(rate))])
        self.data = int16(array(outp)).tostring()

    def done(self):
        self.stream.close()
        self.p.terminate()
        self.wf.close()


if __name__ == "__main__":
    P = Player()
    P.play()
