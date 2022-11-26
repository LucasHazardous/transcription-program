import requests
from time import sleep
from configure import auth_key
import pyaudio
import wave

UPLOAD = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT = "https://api.assemblyai.com/v2/transcript"
HEADERS = {
    "content-Type": "application/json",
    "authorization": auth_key
}

AUDIO_FILENAME = "output.wav"
FRAMES_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


def listenAudio(time):
    p = pyaudio.PyAudio()
    stream = p.open(rate=RATE, channels=CHANNELS, format=FORMAT,
                    frames_per_buffer=FRAMES_BUFFER, input=True)

    frames = []
    framesToCollect = RATE//FRAMES_BUFFER*time
    for i in range(framesToCollect):
        data = stream.read(FRAMES_BUFFER)
        frames.append(data)
        printProgressBar(i, framesToCollect-1, "Speech recorded:")

    stream.stop_stream()
    stream.close()
    p.terminate()

    obj = wave.open(AUDIO_FILENAME, "wb")

    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))

    obj.close()


def transcribe():
    def stage(i):
        printProgressBar(i, 4, "Transcribing:")

    uploadRes = requests.post(
        UPLOAD, headers=HEADERS, data=readFileGenerator(AUDIO_FILENAME))
    uploadRes = uploadRes.json()

    stage(1)

    transcriptReq = {
        "audio_url": uploadRes["upload_url"],
        "language_detection": True
    }
    transcriptRes = requests.post(
        TRANSCRIPT, headers=HEADERS, json=transcriptReq)

    stage(2)

    pollingURL = f"https://api.assemblyai.com/v2/transcript/{transcriptRes.json()['id']}"

    completed = False
    while not completed:
        pollingRes = requests.get(pollingURL, headers=HEADERS).json()
        if (pollingRes["status"] == "completed"):
            completed = True
        sleep(3)

    stage(3)

    finalRes = requests.get(
        pollingURL + "/paragraphs", headers=HEADERS).json()

    transcript = ""
    for paragraph in finalRes["paragraphs"]:
        transcript += paragraph["text"]

    stage(4)

    with open("output.txt", "w") as output:
        output.write(transcript)

    print("Transcription saved")


def readFileGenerator(target):
    with open(target, "rb") as f:
        while True:
            data = f.read(5 * 1024 * 1024)
            if not data:
                break
            yield data


def printProgressBar(i, total, stage):
    percent = ("{0:.1f}").format(100 *
                                 (i / float(total)))
    filledLength = int(10 * i // total)
    bar = "█" * filledLength + "-" * (10 - filledLength)
    print(f"\r{stage}: |{bar}| {percent}%", end="\r")
    if i == total:
        print()


if __name__ == "__main__":
    time = input("Enter time of your speech: ")
    time = int(time) if time.isdecimal() else quit()
    listenAudio(time)
    transcribe()
