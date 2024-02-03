import streamlit as st
from transformers import pipeline

# Initialize the intent classification and NER pipelines
intent_classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
ner_extractor = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

to_do_list = []

def process_command(input_text):
    # Simple heuristic to interpret any input as an intent to add a task, unless specified otherwise
    if "show" in input_text.lower() or "list" in input_text.lower():
        if to_do_list:
            return "Your to-do list:\n" + "\n".join(to_do_list)
        return "Your to-do list is empty."
    elif "exit" not in input_text.lower():
        # Simplified extraction of task description
        # Assumes the phrase following "add" is the task description
        task_description = input_text
        task_keywords = ["add", "want to", "will"]
        for keyword in task_keywords:
            if keyword in input_text.lower():
                start_index = input_text.lower().find(keyword) + len(keyword)
                task_description = input_text[start_index:].strip()
                break
        to_do_list.append(task_description)
        return f"Added task: {task_description}"
    else:
        return "Sorry, I didn't understand that command."

def main():
    st.title("AI-Powered To-Do List")
    st.write("Type your commands in the input box below.")
    st.write("Example commands: 'Add buy groceries', 'Show my to-do list', 'Exit'")

    user_input = st.text_input("You:")
    if user_input.lower() == "exit":
        st.write("Bot: Goodbye!")
    else:
        response = process_command(user_input)
        st.write(f"Bot: {response}")

if __name__ == "__main__":
    main()
