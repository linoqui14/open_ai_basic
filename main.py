import io
from openai import OpenAI
import speech_recognition as sr
import pyaudio
from pydub import AudioSegment
r = sr.Recognizer() 
audio = pyaudio.PyAudio()

client = OpenAI(
    api_key= "",
    organization=""
)

def playSpeech(audio_data):
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
    chunk_size = 1024

    stream = audio.open(
        format=audio.get_format_from_width(audio_segment.sample_width),
        channels=audio_segment.channels,
        rate=audio_segment.frame_rate,
        output=True
    )

    try:
        data = audio_segment.raw_data
        while len(data) > 0:
            stream.write(data[:chunk_size])
            data = data[chunk_size:]
    finally:
        stream.stop_stream()
        stream.close()

def answer(content):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=content
    )

    return response.content


while(True):    
     
    # Exception handling to handle
    # exceptions at the runtime
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            print("NAMINAW.....")
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source2, duration=0.2)
             
            #listens for the user's input 
            audio2 = r.listen(source2)
             
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
 
            print("Did you say ",MyText)

            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": MyText}
                ]
            )
            answer_gpt = completion.choices[0].message.content
            # print(completion.choices[0].message.content)
            res = answer(answer_gpt)
            playSpeech(res)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occurred")