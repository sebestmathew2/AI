hi
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import os
import webbrowser
import requests
import smtplib

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a voice command and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Julius Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry Boss, I didn't catch that. Please repeat.")
            return None
        except sr.RequestError:
            speak("Sorry Boss, I'm having trouble connecting to the speech service.")
            return None
        except Exception as e:
            speak(f"An error occurred: {str(e)}")
            return None

# Function to get the weather report
def get_weather(city):
    API_KEY = "your_api_key_here"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            weather_info = f"The temperature in {city} is {temp}°C with {description}. Humidity is at {humidity}% and wind speed is {wind_speed} m/s."
            return weather_info
        else:
            return "I couldn't find weather data for that location."
    except Exception as e:
        return f"An error occurred while fetching weather data: {str(e)}"

# Function to send email securely
def send_email():
    speak("Boss, Please enter the recipient's email manually:")
    to_email = input("Enter recipient email: ")  # Get a valid email manually
    speak("What is the subject?")
    subject = listen()
    speak("What should I say in the email?")
    body = listen()

    sender_email = "mrunknow@gmail.com"
    sender_password = "your_app_password_here"  # Replace with Google App Password

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email_message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, to_email, email_message)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"Failed to send email. Error: {str(e)}")

# Main function to handle commands
def run_assistant():
    speak("Hello Boss! How can I assist you?")

    while True:
        command = listen()
        if command is None:
            continue

        if "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {now}")

        elif "date" in command:
            today = datetime.datetime.today().strftime("%B %d, %Y")
            speak(f"Today's date is {today}")

        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            if topic:
                speak(f"Searching Wikipedia for {topic}")
                try:
                    result = wikipedia.summary(topic, sentences=2)
                    speak(result)
                except wikipedia.exceptions.DisambiguationError:
                    speak("The search term is too broad. Boss, Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak("Boss, I couldn't find anything on Wikipedia about that topic.")
            else:
                speak("Boss, Please specify a topic to search.")

        elif "play" in command:
            song = command.replace("play", "").strip()
            if song:
                speak(f"Playing {song} on YouTube")
                pywhatkit.playonyt(song)
            else:
                speak("Boss, Please specify a song to play.")

        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open instagram" in command:
            speak("Opening Instagram")
            webbrowser.open("https://www.instagram.com")

        elif "weather" in command:
            speak("Which city's weather would you like to know?")
            city = listen()
            weather_info = get_weather(city)
            speak(weather_info)

        elif "send email" in command:
            send_email()

        elif "what is my name" in command:
            speak("Boss, your name is Sebest Mathew, you have created me and hence, you are my Creator!")

        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break

        else:
            speak("I didn't understand that command. Please try again.")

# Run the assistant
if __name__ == "__main__":
    run_assistant()
