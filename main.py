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
