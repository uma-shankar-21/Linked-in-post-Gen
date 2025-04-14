#!/usr/bin/env python
# coding: utf-8

# In[7]:

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


# In[12]:


load_dotenv()
llm=ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"),model="llama-3.2-90b-vision-preview")


# In[13]:


if __name__=="__main__":
    response=llm.invoke("What is difference between GenAI and LLM")
    print(response.content)


# In[ ]:




