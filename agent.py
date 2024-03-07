from langchain.agents import ConversationalChatAgent, AgentExecutor, create_react_agent
from langchain.agents import load_tools
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.llms import OpenAI
from langchain.memory import ConversationBufferWindowMemory

from dotenv import load_dotenv

load_dotenv()
# creating tools for sales agent

llm = ChatOpenAI()
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
model = ChatOpenAI() 
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

