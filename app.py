import streamlit as st
import spacy

nlp = spacy.load("en_core_web_md")

if 'to_do_list' not in st.session_state:
    st.session_state.to_do_list = []

st.title('🤖 AI-powered Chatbot To-Do List')

# Instructions
st.write("Use commands like: Add [task], Remove [task], Modify [task] to [new task], Show or List.")

# user_input = st.text_input("What's on your mind?", '')
user_input = st.text_input("", placeholder="What's on your mind?", key="input")

def process_command(input_text):
    doc = nlp(input_text.lower())
    task_name = ' '.join(chunk.text for chunk in doc.noun_chunks)
    
    if "add" in input_text.lower():
        st.session_state.to_do_list.append(task_name)
        st.success(f"✅ Added task: {task_name}")
    elif "remove" in input_text.lower():
        if task_name in st.session_state.to_do_list:
            st.session_state.to_do_list.remove(task_name)
            st.success(f"❌ Removed task: {task_name}")
        else:
            st.error("Task not found.")
    elif "modify" in input_text.lower():
        parts = input_text.lower().split("modify", 1)[1].split("to", 1)
        if len(parts) == 2:
            original_task, new_task = parts[0].strip(), parts[1].strip()
            if original_task in st.session_state.to_do_list:
                st.session_state.to_do_list[st.session_state.to_do_list.index(original_task)] = new_task
                st.success(f"✏️ Modified task from '{original_task}' to '{new_task}'.")
            else:
                st.error("Original task not found.")
    elif "show" in input_text.lower() or "list" in input_text.lower():
        if st.session_state.to_do_list:
            st.info("Your to-do list:")
            for task in st.session_state.to_do_list:
                st.markdown(f"- {task}")
        else:
            st.info("Your to-do list is empty.")
    else:
        st.error("Sorry, I didn't understand that command.")

if user_input:
    process_command(user_input)
