import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from PIL import Image
ps = PorterStemmer()
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

image = Image.open('icon.png')
col1, col2, col3 = st.columns(3)
col2.image(image,width=250)
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text: 
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('hybridTunedModel.pkl','rb'))


html_temp = """
    <div style="background-color:#662d91;padding:10px">
    <h2 style="color:white;text-align:center;"> Phishing Email Detector/Classifier </h2>
    </div>
    """
st.markdown(html_temp,unsafe_allow_html=True)

    
input = st.text_area("Enter the message" , height =250)


if st.button('Predict'):

    # 1. preprocess
    transformed = transform_text(input)
    # 2. vectorize
    vector_input = tfidf.transform([transformed])
    # 3. predict
    result = model.predict(vector_input.toarray())[0]
    # 4. Display
    if result == 1:
        st.header("Phishing Email")
        speak("This is Phishing Email")
    else:
        st.header("Legitimate Email")
        speak("This is Legitimate Email")