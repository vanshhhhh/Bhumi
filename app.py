import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
from sqlalchemy import create_engine, MetaData, Table, Column, String
st.set_page_config(
    page_title="Bhumi",
    page_icon = ":leaves:"
)
@st.cache(allow_output_mutation=True)
def load_model():
    model=tf.keras.models.load_model('assets/models/potato_model.h5')
    return model
with st.spinner('Model is being loaded..'):
    model=load_model()
engine = create_engine('sqlite:///bhumi.db', echo = True)
meta = MetaData()
users = Table(
    'users', meta, 
    Column('emailid', String, primary_key = True), 
    Column('firstname', String), 
    Column('lastname', String),
    Column('password', String)
)
def createDatabase():
    meta.create_all(engine)
def addUser(emailid, firstname, lastname, password):
    ins = users.insert()
    ins = users.insert().values(emailid = emailid, firstname = firstname, lastname = lastname, password = password)
    conn = engine.connect()
    result = conn.execute(ins)
try:
    createDatabase()
    addUser('testuser@gmail.com', 'test', 'user', 'testuser')
except:
    print("Database already exists")
def userLogin(emailid, password):
    query = users.select().where(users.c.emailid == emailid)
    conn = engine.connect()
    result = conn.execute(query)
    if result.rowcount == 0:
        print("User does not exist")
    else:
        for row in result:
            if row[3] == password:
                return True
            else:
                return False
def home():
    features = st.radio("Features", ("Disease Detection", "Crop Recommender"), horizontal = True)
    if features == "Disease Detection":
        col1, col2 = st.columns(2)
        with col1:
            selectCrop = st.selectbox("Select Crop", ("Potato", "Other Crop"))
        if selectCrop == "Potato":
            col1, col2 = st.columns(2) 
            with col1:
                file = st.file_uploader("", type=["jpg", "png"])
                def import_and_predict(image_data, model):
                    size = (256,256)    
                    image = ImageOps.fit(image_data, size, Image.ANTIALIAS)
                    img = np.asarray(image)
                    img_reshape = img[np.newaxis,...]
                    prediction = model.predict(img_reshape)
                    return prediction
            with col2:
                if file is None:
                    st.write('\n\n')
                    st.write('\n\n')
                    st.write('\n\n')
                    st.info('Please upload an image file')
                else:
                    image = Image.open(file)
                    st.image(image, use_column_width=True)
                    predictions = import_and_predict(image, model)
                    class_names = ['Early blight', 'Late blight', 'Healthy']
                    string = "Prediction : " + class_names[np.argmax(predictions)]
            if class_names[np.argmax(predictions)] == 'Healthy':
                st.success(string)
            else:
                st.error(string)
                if string == 'Prediction : Late blight':
                    st.write("Late blight is a fungal disease that affects potato plants. It is caused by the fungus Phytophthora infestans. The disease is most common in warm, wet weather. Late blight is a serious disease that can cause significant yield losses. It is most common in the Pacific Northwest, but can occur anywhere potatoes are grown.")
                    st.video('https://www.youtube.com/watch?v=PSXXoGrOyDg') 
        if selectCrop == "Other Crop":
            st.info("Coming Soon")
    if features == "Crop Recommender":
        st.info("Coming Soon")
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: white;
            color: black;
            text-align: center;
            z-index:1;
            }
            </style>
            <div class="footer">
            <p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://vanshhhhh.github.io/" target="_blank">Vansh Sharma</a></p>
            </div>
            </style>
            """
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
st.sidebar.image("./assets/images/logo.png", use_column_width=True)
st.title("Bhumi")
choice = st.sidebar.radio('', ['About Us', 'Login', 'Sign up'], horizontal = True)
if choice != 'About Us':
    email = st.sidebar.text_input('Please Enter Your Email',key = 'login')
    password = st.sidebar.text_input('Please Enter Your Password',type = 'password')
if choice == 'Sign up':
    info = st.info('Please Login to continue')
    firstname = st.sidebar.text_input('Please Enter First Name')
    lastname = st.sidebar.text_input('Please Enter Last Name')
    submit = st.sidebar.button('Sign Up')
    if submit:
        try:
            addUser(email, firstname, lastname, password)
            info.empty()
            st.title('Welcome ' + firstname)
            st.success('Your account is created suceesfully! Please login to continue')
        except:
            info.empty()
            st.error('Registeration Failed')
# User Login Block
if choice == 'Login':
    info = st.info('Please Login to continue')
    login = st.sidebar.checkbox('Login')
    if login:
        try:
            if userLogin(email, password):
                info.empty()
                st.subheader('Welcome')
                home()
            else:
                info.empty()
                st.error('Login Failed')
        except Exception as e:
            info.empty()
            print(e)
if choice == 'About Us':
    st.info('''
    This project is developed by [Vansh Sharma](https://www.linkedin.com/in/vanshsharma10). Make sure to give it a star on [Github](https://github.com/vanshhhhh/Bhumi).
    ''')