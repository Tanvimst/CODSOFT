import re

def fetch_reply(user_input):
    if re.search(r'\bhi\b', user_input, re.IGNORECASE):
        return "Hey there! How can I assist you?"

    elif re.search(r'\bfeeling\b', user_input, re.IGNORECASE):
        return "I'm a program, so no feelings here. How can I help you?"

    elif re.search(r'\b(who are you|introduce yourself)\b', user_input, re.IGNORECASE):
        return "I'm your friendly chatbot created to help answer your queries."

    elif re.search(r'\b(what can you do|abilities)\b', user_input, re.IGNORECASE):
        return "I can answer basic questions, share fun facts, or chat with you."

    elif re.search(r'\b(fact|share a fact)\b', user_input, re.IGNORECASE):
        return "Did you know? Honey never spoils—it can last for thousands of years!"

    elif re.search(r'\b(thanks|thank you)\b', user_input, re.IGNORECASE):
        return "You're welcome! Anything else you want to know?"

    elif re.search(r'\b(help)\b', user_input, re.IGNORECASE):
        return "I can provide fun facts, answer simple questions, or just chat. What would you like to talk about?"

    else:
        return "I didn't quite get that. Could you ask me something else?"

def simple_chatbot():
    print("Hey! I'm your personal chatbot. What can I do for you today?")
    while True:
        user_input = input("You: ")
        
        if re.search(r'\b(bye|quit|exit)\b', user_input, re.IGNORECASE):
            print("Chatbot: Goodbye! Take care.")
            break
        
        response = fetch_reply(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    simple_chatbot()
