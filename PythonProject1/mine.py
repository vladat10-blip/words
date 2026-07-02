import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
from googletrans import Translator

print("")
print("-" * 65)
print("Привет!Это викторина где ты говоришь русские слова на английском")
print("-" * 65)
print("")

sample_rate = 44100
duration = 4  # секунд записи
point = 0
error = 0

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
    }
print ("какой уровень сложности вы хотите выбрать? ")
print ("1. easy")
print ("2. medium")
print ("3. hard\n")

number = input("Введите номер:")

while number not in ["1", "2", "3"]:
    print("Ошибка! Введи 1, 2 или 3.")
    number = input("Выбери уровень: ")

if number == "1":
    level = "easy"
    word_list = words_by_level["easy"]
elif number == "2":
    level = "medium"
    word_list = words_by_level["medium"]
elif number == "3":
    level = "hard"
    word_list = words_by_level["hard"]
else:
    print("Ошибка! Выбирай 1, 2 или 3.")

#level = input().lower()
#while level not in words_by_level:
    #print("какой уровень сложности вы хотите выбрать? easy, medium, hard ")
    #level = input().lower()
word_list = words_by_level[level]
random.shuffle(word_list)

recognizer = sr.Recognizer()
translator = Translator()

for word in word_list:
    print(word)
    print("🎙 Говори...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", sample_rate, recording)
    print("✅ Запись завершена, распознаём...")
    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        recognized = recognizer.recognize_google(audio, language="en-US").lower()
        print("📝 Ты сказал:", recognized)
        translation =translator.translate(word,src="ru", dest="en").text.lower()
        print("🔤 Перевод:", translation)
        if recognized == translation:
            point += 1
            print("правильно")
        else:
            error += 1
            print("нет")
        if error >= 3:
            print("игра окончена")
            break

    except sr.UnknownValueError:
        print(f"😕 Не удалось распознать речь. Ошибок: {error}/3")

    except sr.RequestError as e:
        print(f"❗ Ошибка сервиса: {e}")
        break
print("кол-во баллов за игру")
