from langchain.agents import ConversationalChatAgent, AgentExecutor, create_react_agent
from langchain.agents import load_tools
from langchain_openai.llms import ChatAnthropic
from langchain.memory import ConversationBufferWindowMemory
import streamlit as st

import os

os.environ["ANTHROPIC_API_KEY"] = st.secrets["openai"]
# creating tools for sales agent

llm = ChatAntropic(api-key=st.secrets["openai"])
agent_prompt = """
You are an honest and helpful AI job assistant for a Job Portal RevHire. Help users find jobs and employers hire top talent. 
RevHire is a job portal for recruiting. Below are the capabilities of RevHire.
Capabilities:
- Understand job search, resume, interview queries
- Access job listings and career resources 
- Guide job seekers with personalized recommendations
- Assist employers with job posts, resumes, interviews
- Provide advice on resumes, interviews, career planning

Guidelines:
- Prioritize user satisfaction with accurate, relevant info
- Maintain privacy and avoid discrimination
- Be honest about knowledge limitations  
- Encourage verifying critical info from authoritative sources
- Use a friendly, professional tone
"""
tools = load_tools(['ddg-search'], llm=llm)
model = ChatOpenAI(openai_api_key=st.secrets["openai"]) 
memory = ConversationBufferWindowMemory(k=3, memory_key='chat_history', return_messages=True)
prefix = agent_prompt
# chain = prompt | model
agent_definition = ConversationalChatAgent.from_llm_and_tools(
    llm = model,
    tools  = tools,
    verbose =True,
    system_message = agent_prompt,

)
agent_execution = AgentExecutor.from_agent_and_tools(
    agent=agent_definition,
    llm=model,
    tools= tools,
    verbose = True,
    max_iterations=3,
    memory = memory,
    handle_parsing_erros= True

)




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
