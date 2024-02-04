import streamlit as st
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_md")

to_do_list = []

st.title('AI-powered To-Do List')

st.write("""
    Use commands like:
    - "Add [task]" to add a new task.
    - "Remove [task]" to delete an existing task.
    - "Modify [task] to [new task]" to change a task.
    - "Show" or "List" to display all tasks.
""")

user_input = st.text_input("What's on your mind?", '')

def process_command(input_text):
    doc = nlp(input_text.lower())
    task_name = ' '.join(chunk.text for chunk in doc.noun_chunks)
    
    if "add" in input_text.lower():
        to_do_list.append(task_name)
        return f"Added task: {task_name}"
    elif "remove" in input_text.lower():
        if task_name in to_do_list:
            to_do_list.remove(task_name)
            return f"Removed task: {task_name}"
        else:
            return "Task not found."
    elif "modify" in input_text.lower():
        parts = input_text.lower().split("modify",1)[1].split("to",1)
        if len(parts) == 2:
            original_task, new_task = parts[0].strip(), parts[1].strip()
            if original_task in to_do_list:
                to_do_list[to_do_list.index(original_task)] = new_task
                return f"Modified task from '{original_task}' to '{new_task}'."
            else:
                return "Original task not found."
    elif "show" in input_text.lower() or "list" in input_text.lower():
        return "\n".join(f"- {task}" for task in to_do_list) if to_do_list else "Your to-do list is empty."
    else:
        return "Sorry, I didn't understand that command."

if user_input:
    result = process_command(user_input)
    st.write(result)

if st.button('Show My To-Do List'):
    if to_do_list:
        st.write("\n".join(f"- {task}" for task in to_do_list))
    else:
        st.write("Your to-do list is empty.")
