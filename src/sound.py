from scipy import frombuffer, int16, array
import pyaudio
import wave


class Player:
    def __init__(self, path):
        self.task = None
        self.path = path
        self.p = pyaudio.PyAudio()
        self.chunk = 1024
        self.isstart = False
        self.current_speed = 1.0
        self.wf = None
        self.stream = None

    def set_wave(self):
        if self.wf is not None:
            self.wf.close()
        self.wf = wave.open(self.path, "rb")

    def set_stream(self):
        if self.stream is not None:
            self.stream.close()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True
            )

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
        if (not self.isstart) and (self.task[0] == "play"):
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
                self.current_speed = self.task[1]
                self.task = None

    def stop(self):
        self.set_wave()
        self.set_stream()
        self.data = self.wf.readframes(self.chunk)
        self.pause()

    def play(self):
        self.set_wave()
        self.set_stream()
        self.data = self.wf.readframes(self.chunk)
        self.changePlaySpeed(self.current_speed)

        while len(self.data) > 0:
            self.stream.write(self.data)
            self.data = self.wf.readframes(self.chunk)
            self.data = frombuffer(
                self.data,
                dtype="int16"
                )
            if self.task is None:
                pass
            elif self.task[0] == "pause":
                self.task = None
                self.pause()
            elif self.task[0] == "stop":
                self.task = None
                self.stop()
            elif self.task[0] == "change_speed":
                print(f"curren_speed changed to: {self.task[1]}")
                self.current_speed = self.task[1]
                self.task = None
            self.changePlaySpeed(self.current_speed)
        print("play done")
        self.isstart = False

    def changePlaySpeed(self, rate):
        outp = []
        for i in range(int(len(self.data) / rate)):
            outp.append(self.data[int(i * float(rate))])
        self.data = int16(array(outp)).tostring()

    def done(self):
        if self.stream is not None:
            self.stream.close()
        if self.p is not None:
            self.p.terminate()
        if self.wf is not None:
            self.wf.close()


if __name__ == "__main__":
    P = Player()
    P.play()
