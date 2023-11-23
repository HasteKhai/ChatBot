import json
from difflib import get_close_matches
import requests
import os
from datetime import datetime



def weather_app() -> str:
    user_api = os.environ['weather_app_key']
    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=Montreal&appid="+user_api
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    weather_desc = api_data['weather'][0]['description']
    tempature = ((api_data['main']['temp'])-273.15)
    feels_like = ((api_data['main']['feels_like'])-273.15)
    humidity = api_data['main']['humidity']
    date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

    return (f"There is {weather_desc}. The tempature in Montreal is {tempature:.2f}\u00b0C. It feels like {feels_like:.2f}\u00b0C. The humidity is at {humidity}%. Today's date: {date_time}")

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_bestMatch(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]




def chatBot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('Type something: ')

        if user_input.lower() == 'quit':
            break

        if user_input.lower().__contains__('weather'):
            answer: str | None = weather_app()
            print(f'Bot: {answer }')
        else:
            best_match: str | None = find_bestMatch(user_input, [q["question"] for q in knowledge_base["questions"]])

            if best_match:
                answer: str = get_answer_for_question(best_match, knowledge_base)
                print(f'Bot: {answer}')
            else:
                print("Bot: I don't know the answer. Can you tell me?")
                new_answer: str = input('Type the answer or "skip" to skip: ')

                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print('Bot: Thank you! I learned a new response.')

if __name__ == '__main__':
    chatBot()