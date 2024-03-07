import streamlit as st
from agent import agent_execution

# Title of the page
st.title('RevHire')
 

# Code to add the first ai message
if 'chat' not in st.session_state:
  st.session_state['chat'] = [{
    "content": "Hi, I'm an agent for RevHire. How can I help you today?",
    "role": "ai"
  }]

user_input = st.chat_input('message:', key= "user_input")

# adding user input to session
if user_input:
  st.session_state['chat'].append({
    "content": user_input,
    "role": "user"
  })
  # calling the langchain sales agent
  agent = agent_execution
  try:
      # generating completeion for users prompt by invoking the agent
      agent_response = agent.invoke({'input':user_input})
       # adding ai agent response to the session state
      st.session_state['chat'].append({
      "content": agent_response['output'],
      "role": "ai"})
  except :
    # handlinig any parsing errors
      st.session_state['chat'].append({
      "content": "Sorry, I'm not sure I can help with that.",
      "role":"ai"})

# rendering the messesges from chat
if st.session_state['chat']:
  for i in range(0, len(st.session_state['chat'])):
    user_message = st.session_state['chat'][i]
    st.chat_message(user_message["role"]).write(user_message["content"])