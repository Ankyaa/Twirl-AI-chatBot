import streamlit as st
import json
from difflib import get_close_matches

#to add title to my Twirl AI chatbot
st.title('Twirl - AI chatbot')

#to load the knowledge base into the py program
def load_knowledge_base(file_path:str) -> dict: #arrow indicates return. example load_knowledge base function will return str or none.
    with open(file_path,'r') as file:
        data:dict = json.load(file)
    return data


#to save the knowdge base data into a json file so that for next instance it can save the data.
def save_knowlegde_base(file_path:str, data:dict):
    with open(file_path,'w') as file:
        json.dump(data, file, indent=2)

#to find the best match of the user response from dictionary
def find_best_match(user_question:str, questions:list[str]) ->str | None:
    matches :list = get_close_matches(user_question,questions,n=1, cutoff=0.6) #n here is the no of best matches here. if set to 2 the it will return top 2 best matches
    return matches[0] if matches else None

#to get the answer
def get_answer_for_question (question:str, knowledge_base:dict) -> str | None:
    for q in knowledge_base ["questions"]:
        if q["question"] == question:
            return q["answer"]
        

def chatbot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input:str = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match: str|None = find_best_match(user_input,[q["question"] for q in knowledge_base["questions"] ])

        if best_match:
            answer: str = get_answer_for_question(best_match,knowledge_base)
            print(f'Bot: {answer}')

        else:
            print('Bot: I don\'t know the answer. Can you please teach me?')
            new_answer: str = input('Type the answer or "skip" to Skip. ')

            if new_answer != 'skip':
                knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
                save_knowlegde_base('knowledge_base.json',knowledge_base)
                print("Bot: Thank you! I learned a new response!")

if __name__ == '__main__':
    chatbot()
