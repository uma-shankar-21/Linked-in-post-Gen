import streamlit as st
from Few_shot import Fewshots
from post_generator import generate_post
length_options=["Short","Meduim","Large"]
Language_options=["English","Hindi","Hinglish"]
def main():
    st.title("LinkedIn Post Generator For Infulencers")
    col1,col2,col3=st.columns(3)
    fs=Fewshots()
    with col1:
        selected_tag=st.selectbox("Title",options=fs.get_tags())
    with col2:
        selected_length=st.selectbox("Length",options=length_options)
    with col3:
        selected_language=st.selectbox("Language",options=Language_options)
    if st.button("Generate"):
        post=generate_post(selected_length,selected_language,selected_tag)
        st.write(post)
if __name__=='__main__':
    main()
#########################################      FEW SHOT      #################################################################
import json
import pandas as pd
class Fewshots:
    def __init__(self, file_path=r"C:\Users\Dell\OneDrive\Desktop\US\LinkedinPost Generator\data\preprocess_post.json"):
        self.df=None
        self.unique_tags=None
        self.load_post(file_path)
    def load_post(self,file_path):
        with open(file_path,encoding="utf-8") as f:
            posts=json.load(f)
            self.df=pd.json_normalize(posts)
            self.df['length']=self.df['line_count'].apply(self.categorize_length)
            all_tags=self.df['tags'].apply(lambda x:x).sum()
            self.unique_tags=set(all_tags)
    def categorize_length(self,line_count):
        if line_count<5:
            return "Short"
        elif 5<=line_count<=10:
            return "Medium"
        else:
            return "Long"
    def get_tags(self):
        return self.unique_tags
    def get_filtered_posts(self,length,language,tag):
        df_filtered = self.df[
            (self.df['language']==language) &
            (self.df['length']==length) &
            (self.df['tags'].apply(lambda tags :tag in tags))
        ]
        return df_filtered.to_dict(orient="records")
if __name__=="__main__":
    fs=Fewshots()
    posts=fs.get_filtered_posts("Short","English","Job Search")
    print(posts)
############################################################# POST GENERATOR #######################################################
from llm_helper import llm
#from Few_shot import Fewshots

few_shot = Fewshots()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    # prompt = prompt.format(post_topic=tag, post_length=length_str, post_language=language)

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt

if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))
##########################################   LLM HELPER            ############################################################
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
llm=ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"),model="llama-3.2-90b-vision-preview")

if __name__=="__main__":
    response=llm.invoke("What is difference between GenAI and LLM")
    print(response.content)
