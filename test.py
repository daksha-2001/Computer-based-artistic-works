import streamlit as st
import sqlite3 
import pandas as pd
from PIL import Image
import style
import base64
from io import BytesIO
import SessionState
import pandas as pd

conn = sqlite3.connect('data1.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data=c.fetchall()
    return data


def main1():
    hide_full_screen = '''
<style>
.element-container:nth-child(1) .overlayBtn {visibility: hidden;}
</style>
'''

   
    phemp=st.empty()
    menu=["Home","SignUp"]
    st.sidebar.markdown("""<link href='https://fonts.googleapis.com/css?family=Bayon' rel='stylesheet'>
    <div>
        <p style="color:black;font-family: 'Bayon';font-size:20px;">Navigation Bar</p>
    </div>""",unsafe_allow_html=True)
    choice=st.sidebar.selectbox("",menu)          
    if choice=="Home":
        phemp.empty()
        mainapp()
    elif choice=="SignUp":
        create_usertable()
        temp="""
    <link href='https://fonts.googleapis.com/css?family=Bigshot One' rel='stylesheet'>
    <h3 style="margin-top:-35px;margin-bottom:-10px;color:black;text-align:center;font-family: 'Bigshot One';font-size:30px;">SIGNUP
    <span style='font-size:30px;'>&#128519;</span></h3>
    """
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        local_css("s2.css")
        col1,col2=st.beta_columns(2)
        col1.markdown(temp,unsafe_allow_html=True)
        imag=Image.open("signin-image.jpg")
        col2.image(imag,width=350)
        col2.markdown(hide_full_screen, unsafe_allow_html=True) 
        
        col1.markdown("""<link href='https://fonts.googleapis.com/css?family=Bree Serif' rel='stylesheet'>
        <div>
            <h3 style="color:black;font-family: 'Bree Serif';font-size:20px;margin-bottom:-20px;">Username</h3>
        </div>""",unsafe_allow_html=True)
        new_user=col1.text_input("") 
        col1.markdown("""<link href='https://fonts.googleapis.com/css?family=Bree Serif' rel='stylesheet'>
        <div>
            <h3 style="color:black;font-family: 'Bree Serif';font-size:20px;margin-bottom:-20px;">Password</h3>
        </div>""",unsafe_allow_html=True)
        new_pasword=col1.text_input("",type="password")

        numerics="0123456789"
        capital_alphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        special_chars="#$@"
        sum=0
        x=0
        y=0
        z=0
        for i in range(len(new_pasword)):
            if new_pasword[i] in numerics:
                x=x+1
            elif new_pasword[i] in capital_alphabets:
                y=y+1
            elif new_pasword[i] in special_chars:
                z=z+1
            
        sum=x+y+z   
        if col1.button("SignUp"):
            if(new_user=="admin" and new_pasword=="admin123-daksha"):
                user_result=view_all_users()
                clean_db=pd.DataFrame(user_result,columns=["Username","Password"])
                col1.dataframe(clean_db)
            elif(new_user=="" or new_pasword==""):
                col1.info("Please don't leave Username or password blank!")
            elif(len(new_pasword)<6):
               col1.info("Minimum length of password is atleast 6 characters")
            elif(sum<3):
                col1.info("Password should be minimum 6 characters and should have atleast 1 special character(#,$,@) 1 Captial Character and 1 numeric character!!")
            else:
                result=login_user(new_user,new_pasword)
                if result:
                    col1.info("You already have an Account!")
                else:
                    create_usertable()
                    add_userdata(new_user,new_pasword)
                    col1.success("Account created Successfully!!")
                    col1.info("Go to Home via the navigation bar for exploration!")  
def mainapp():
    
    temp="""
    <link href='https://fonts.googleapis.com/css?family=Bigshot One' rel='stylesheet'>
    <div style="background-color:#464e5f;padding:30px,margin:10px;border-radius:25px;">
    <h3 style="color:white;text-align:center;padding:30px;font-family: 'Bigshot One';font-size:40px;">Computer Based Artistic Works</h3>
    </div>
    """
    st.markdown(temp,unsafe_allow_html=True)
    st.sidebar.markdown("""<link href='https://fonts.googleapis.com/css?family=Bayon' rel='stylesheet'>
    <div>
        <p style="color:black;font-family: 'Bayon';font-size:20px;">Select Content Image</p>
    </div>""",unsafe_allow_html=True)
    img=st.sidebar.selectbox(
        '',
        ('amber.jpg','puppies.jpg','donuts.jpg','drinks.jpg','wall-of-china.jpg')
        )  

    st.sidebar.markdown("""<link href='https://fonts.googleapis.com/css?family=Bayon' rel='stylesheet'>
    <div>
        <p style="color:black;font-family: 'Bayon';font-size:20px;">Select Style</p>
    </div>""",unsafe_allow_html=True)
    
    style_name=st.sidebar.selectbox(
        '',
        ('candy','mosaic','rain-princess','udnie')
        )
    model="saved_models/"+style_name+".pth"
    style_image="images/style-images/"+style_name+".jpg"
    input_image="images/content-images/"+img
    col1,col2=st.beta_columns(2)
    col1.markdown("""<link href='https://fonts.googleapis.com/css?family=Bree Serif' rel='stylesheet'>
        <div>
    <h3 style="color:black;font-family: 'Bree Serif';font-size:30px;">Source Image:</h3>
    </div>""",unsafe_allow_html=True)
    image=Image.open(input_image)
    col1.image(image,width=330)

    col2.markdown("""<link href='https://fonts.googleapis.com/css?family=Bree Serif' rel='stylesheet'>
        <div>
    <h3 style="color:black;font-family: 'Bree Serif';font-size:30px;">Style Image:</h3>
    </div>""",unsafe_allow_html=True)
    image2=Image.open(style_image)
    col2.image(image2,width=330)
    
    output_image="images/output-images/"+style_name+"-"+img


    session_state=SessionState.get(checkboxed=False)
    
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



    local_css("style.css")
    
    clicked = st.button("Stylize")
    
  
    
    def get_image_download_link(img):
    
	    buffered = BytesIO()
	    img.save(buffered, format="JPEG")
	    img_str = base64.b64encode(buffered.getvalue()).decode()
	    href = f'<a href="data:file/jpg;base64,{img_str}" download="Image.jpg">Download result</a>'
	    return href

    if clicked or session_state.checkboxed:
        session_state.checkboxed=True
        model=style.load_model(model)
        style.stylize(model,input_image,output_image)
        
        
        st.markdown("""<link href='https://fonts.googleapis.com/css?family=Bree Serif' rel='stylesheet'>
        <div>
    <h3 style="color:black;font-family: 'Bree Serif';font-size:30px;">Output Image:</h3>
    </div>""",unsafe_allow_html=True)
        image=Image.open(output_image)
        st.image(image,width=400)
        st.info("Only Registered Users can Downoad the output Image!!")
        t1="""
        <link href='https://fonts.googleapis.com/css?family=Bigshot One' rel='stylesheet'>
        <div>
    <h3 style="color:black;margin-bottom:-30px;font-family: 'Bigshot One';font-size:30px;">Have You Registered?<span style='font-size:30px;'>&#129300;</span></h3> </div>
        """
        st.markdown(t1,unsafe_allow_html=True)
        radio=st.radio("",('Yes','No'))
        if(radio=='Yes'):
            st.markdown("""<link href='https://fonts.googleapis.com/css?family=Bree Serif' rel='stylesheet'>
        <div>
            <h3 style="color:black;font-family: 'Bree Serif';font-size:20px;margin-bottom:-20px;">Enter Username..</h3>
        </div>""",unsafe_allow_html=True)
            user=st.text_input("","")
            st.markdown("""<link href='https://fonts.googleapis.com/css?family=Bree Serif' rel='stylesheet'>
            <div>
                <h3 style="color:black;font-family: 'Bree Serif';font-size:20px;margin-bottom:-20px;">Enter Password..</h3>
            </div>""",unsafe_allow_html=True)
            passw=st.text_input("","",type="password")
            if st.button("Go"):
                result=login_user(user,passw)
                if result:
                    st.success("Logged in as {}".format(user))
                    image1=Image.open(output_image)
                    st.markdown(get_image_download_link(image1),unsafe_allow_html=True)
                else:
                    st.warning("Incorrect Username/Password")
                   
        if(radio=='No'):
            st.warning("Please Register Yourself Using the Signup Option in the Navigation bar")
            
       
if __name__=="__main__":
    main1()
      
