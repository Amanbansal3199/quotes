from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager ,Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
import json,glob
import random
from pathlib import Path
Builder.load_file("designs.kv")

# creating  login screen
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    def forgot(self):
        self.manager.current ="Forgot_Password"
    def next(self,uname,pword):
        with open("users.json") as file:
            users=json.load(file)
        if uname in users and users[uname]["password"]==pword:
            self.manager.transition.direction="up"
            self.manager.current="Login_page"
        else:
            anim=Animation(color=(0.6,0.7,1,1))
            anim.start(self.ids.login_wrong)
            self.ids.login_wrong.text="Wrong username or password!"


# login page
class LoginPage(Screen):
     def log_out(self):
         self.manager.transition.direction="right"
         self.manager.current = "Login_Screen"

     def get_quote(self,feeling):
         feeling=feeling.lower()
         available_feeling=glob.glob(r"C:\Users\HP Pavilion\Desktop\python\quotes/*txt")
         available_feeling=[Path(filename).stem for filename in available_feeling]

         if feeling in available_feeling:
            with open(f"{feeling}.txt",encoding="utf8") as file:
                quotes=file.readlines()
            self.ids.qu.text = random.choice(quotes)
         else:
             self.ids.qu.text="pls try another feeling"
class ImageButton(HoverBehavior,ButtonBehavior,Image):
    pass

class ForgotPassword(Screen):
    def go_to_back(self):
        self.manager.transition.direction="right"
        self.manager.current="Login_Screen"


# creating a sign_up page
class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
        users[uname]={"username":uname,"password":pword,
             "created":datetime.now().strftime("%d-%m-%y %H:%M:%S")}
        with open("users.json",'w') as file:
            json.dump(users,file)
            self.manager.current="sign_up_successfully"

# back to login page
class SignUpScreenSuccess(Screen):
    def go_to(self):
        self.manager.transition.direction= "right"
        self.manager.current ="Login_Screen"
class RootWidget(ScreenManager):
    pass
class MainApp(App):
    def build(self):
        return RootWidget()
if __name__ == "__main__":
    MainApp().run()