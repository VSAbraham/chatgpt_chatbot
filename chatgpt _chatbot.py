import openai
import pyttsx3
import speech_recognition as sr
r = sr.Recognizer()
print("Recognizing...")
# confs for pyttsx3
engine = pyttsx3.init()

openai.api_key = 'sk'
def speak(text):
    engine.say(text)
    engine.runAndWait()


def recognize_voice():
    text = ''

    # create an instance of the Microphone class
    with sr.Microphone() as source:
        # adjust for ambient noise
        r.adjust_for_ambient_noise(source)

        # capture the voice
        voice = r.listen(source)

        # let's recognize it
        try:
            text = r.recognize_google(voice)
        except sr.RequestError:
            speak("Sorry, the I can't access the Google API...")
        except sr.UnknownValueError:
            speak("Sorry, Unable to recognize your speech...")
    return text.lower()


messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},
]

while True:

    message = recognize_voice()
    print(f"User : {message}")
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat.choices[0].message.content
    if "quit" in message or "exit" in message:
        speak("ok! see you later...")
        print("ChatGPT: ok! see you later...")
        exit()

    speak(reply)
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
