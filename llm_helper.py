#import os
#from dotenv import load_dotenv
from langchain_groq import ChatGroq
GROQ_API_KEY="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"
#load_dotenv()
llm=ChatGroq(groq_api_key=GROQ_API_KEY,model="llama-3.2-90b-vision-preview")

if __name__=="__main__":
    response=llm.invoke("What is difference between GenAI and LLM")
    print(response.content)
