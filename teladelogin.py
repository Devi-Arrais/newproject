# -*- encoding:utf-8 -*-
import sqlite3 
import bcrypt
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label


kv = Builder.load_file("login.kv")

conn = sqlite3.connect('user.db')

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS membros(
    nome TEXT NOT NULL,
    passw TEXT NOT NULL    
);
""")

def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))


class CriacaoDeConta(Screen):
    usuario = ObjectProperty(None)
    senha = ObjectProperty(None)
    def submit(self):
        hash_senha = bcrypt.hashpw(self.senha.text, bcrypt.gensalt())
        cur.execute(f"""
            INSERT INTO membros(nome, passw)
            VALUES ('{self.usuario.text}','{hash_senha}');
            """)
        sm.current = "login"  
        conn.commit()

def valida_senha(senha, hash_senha):
    sm.current = "main"
    return bcrypt.hashpw(senha, hash_senha) == hash_senha

    
    
 
class LoginWindow(Screen):
    usuario = ObjectProperty(None)
    senha = ObjectProperty()
    
    def loginBtn(self):
        usuario = cur.execute("""
             SELECT passw FROM membros WHERE nome='%s';
    
            """%(self.usuario.text))
        users = cur.fetchone()
        hash_senha = str(users[0])
        return valida_senha(self.senha.text, hash_senha)
        
    def createBtn(self):
        self.reset()
        sm.current = "crie" 

    def reset(self):
        self.usuario.text = ""
        self.senha.text = ""
    conn.commit()

class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

conn.commit()

class WindowManager(ScreenManager):
    pass

sm = WindowManager()

screen = [LoginWindow(name="login"), CriacaoDeConta(name="crie"),MainWindow(name="main")]
for screen in screen:
    sm.add_widget(screen)
sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()

conn.close()