##########################################################
# User Singup Page (College project; 9th Grade)
#   ~ Version: master
#
#   Resources:
#     * Homepage:    https://github.com/TechnoLukas
#     * DearPyGui:   https://github.com/hoffstadt/DearPyGui
##########################################################

import dearpygui.dearpygui as dpg
import time
import json

#---Variables---
nickname="" #Nickname of current user
password='' #Password of current user
confirmpassword='' #Confirm password of current user
textdoc='' #Text document of the current user
logedIn=False #Varibale which block content and popup Login wondow or close the Login window and show the content

dpg.create_context()

#---Fonts---
with dpg.font_registry(): #Creates font varibales 
    # first argument ids the path to the .ttf or .otf file
    font_Title=dpg.add_font("C:\Windows\Fonts\Arial.ttf", 30)
    font_Normal=dpg.add_font("C:\Windows\Fonts\Arial.ttf", 14)

#---Functions---
#--Buttons--
def SingupButton(text):
    t = dpg.add_button(label=text, callback=Signup)
    dpg.bind_item_theme(t, "__demo_hyperlinkTheme")

def LoginButton(text):
    t = dpg.add_button(label=text, callback=Login)
    dpg.bind_item_theme(t, "__demo_hyperlinkTheme")

#--Callbacks--
def NicknameCallback(sender,app_data,user_data):
    global nickname
    nickname = app_data

def PasswordCallback(sender,app_data,user_data):
    global password,confirmpassword
    pitem=user_data[0] #previews item
    ptype=user_data[1] #password type normal/confirm
    if len(pitem)>4: #Makes that max lenth of password is 4
        dpg.disable_item(pitem)
        dpg.focus_item(pitem)
        dpg.enable_item(pitem)
        dpg.set_value(sender, app_data[0:4])
        dpg.disable_item(sender)
        dpg.focus_item(sender)
        time.sleep(0.05)
        dpg.enable_item(sender)
    if ptype=="normal":
        password=app_data[0:4]
    else:
        confirmpassword=app_data[0:4]

def LoginCallback():
    global logedIn
    if nickname=='' or password=='':
        dpg.configure_item("popup_EF", show=True)
    else:
        if(nickname in UsersDatabase_getfull()):
            if(len(password) < 4):
                dpg.configure_item("popup_SP", show=True)
            elif(UsersDatabase_getval(nickname,"password")!=int(password)):
                dpg.configure_item("popup_IP", show=True)
            else:
                dpg.configure_item("popup_SL", show=True)
                logedIn=True
                ToggleStatus()
                MainContentWindow()
        else:
            dpg.configure_item("popup_IN", show=True)

def SingupCallback():
    global logedIn
    if nickname=='' or password=='' or confirmpassword=='':
        dpg.configure_item("popup_EF", show=True)
    else:
        if(nickname not in UsersDatabase_getfull()):
            if(len(password) < 4):
                dpg.configure_item("popup_SP", show=True)
            elif(len(confirmpassword) < 4):
                dpg.configure_item("popup_SCP", show=True)
            elif(confirmpassword!=password):
                dpg.configure_item("popup_MP", show=True)
            else:
                dpg.configure_item("popup_SL", show=True)
                logedIn=True
                UsersDatabase_newuser(nickname)
                UsersDatabase_setval(nickname,"password",int(password))
                ToggleStatus()
                MainContentWindow()
        else:
            dpg.configure_item("popup_DN", show=True)

def TextdocCallback(sender,app_data,user_data):
    UsersDatabase_setval(nickname,"textdoc",app_data)


#--Window funcions--
def MenuButton():
    if logedIn==True:
        LogOut()
    else:
        LoginOrSingup()

def LoginOrSingup():
    DelAll()
    w_width=400
    w_height=200
    with dpg.window(label="Login Or Singup", width=w_width,height=w_height, pos=(600/2-w_width/2,800/2-w_height/2),no_move=True,no_collapse=True,no_resize=True,tag="LoginOrSingup"):
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        
        with dpg.group(tag="slt"): #Singup or Login Title so we can position it.
            posm=dpg.get_item_pos("slt") #Gets position of this group
            dpg.add_text("Login Or Singup",pos=(posm[0]+400/2-100,posm[1]+20)) #Changes our position
            dpg.bind_item_font(dpg.last_item(), font_Title) #Aplly font
        dpg.add_text("To access the content you need to Login or Singup")
        with dpg.group(horizontal=True):
            dpg.add_button(label="Login",width=200,height=40,callback=Login) #Changes our position
            dpg.add_button(label="Singup",width=200,height=40,callback=Signup) #Changes our position

def Signup():
    DelAll()
    w_width=400
    w_height=400
    with dpg.window(label="Singup", width=400,height=400, pos=(600/2-w_width/2,800/2-w_height/2),no_move=True,no_collapse=True,no_resize=True,tag="Singup"):
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        
        with dpg.group(tag="st"): #Singup Title so we can position it.
            posm=dpg.get_item_pos("st") #Gets position of this group
            dpg.add_text("Create new account",pos=(posm[0]+400/2-120,posm[1]+20)) #Changes our position
            dpg.bind_item_font(dpg.last_item(), font_Title) #Aplly font

        dpg.add_text("Nickname: ")
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        dpg.add_input_text(tag="nicknameinputs",no_spaces=True,callback=NicknameCallback) #Nickname Input (SingUp)
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        dpg.add_text("Password: ")
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        dpg.add_input_text(no_spaces=True,decimal=True,callback=PasswordCallback,user_data=["nicknameinputs","normal"])
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        dpg.add_text("Confirm Password: ")
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        dpg.add_input_text(no_spaces=True,decimal=True,callback=PasswordCallback,user_data=["nicknameinputs","confirm"])
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        
        with dpg.group(horizontal=True):
            dpg.add_text("If you already have an account you can")
            dpg.bind_item_font(dpg.last_item(), font_Normal)
            LoginButton("Login")
            dpg.bind_item_font(dpg.last_item(), font_Normal)

        with dpg.group(tag="sb"): #Login Button so we can position it.
            posm=dpg.get_item_pos("sb") #Gets position of this group
            dpg.add_button(label="Singup",pos=(posm[0]+400/2-60,posm[1]+230),width=100,height=40,callback=SingupCallback) #Changes our position
            dpg.bind_item_font(dpg.last_item(), font_Title) #Aplly font

def Login(): 
    DelAll()
    w_width=400
    w_height=250
    with dpg.window(label="Login", width=w_width,height=w_height, pos=(600/2-w_width/2,800/2-w_height/2),no_move=True,no_collapse=True,no_resize=True,tag="Login"):
        dpg.bind_item_font(dpg.last_item(), font_Normal)

        with dpg.group(tag="lt"): #Login Title so we can position it.
            posm=dpg.get_item_pos("lt") #Gets position of this group
            dpg.add_text("Login with existing account",pos=(posm[0]+400/2-170,posm[1]+20)) #Changes our position
            dpg.bind_item_font(dpg.last_item(), font_Title) #Aplly font

        dpg.add_text("Nickname: ")
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        dpg.add_input_text(tag="nicknameinputl",no_spaces=True,callback=NicknameCallback) #Nickname Input (Login)
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        dpg.add_text("Password: ")
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        dpg.add_input_text(no_spaces=True,decimal=True,callback=PasswordCallback,user_data=["nicknameinputl","normal"])
        dpg.bind_item_font(dpg.last_item(), font_Normal)

        with dpg.group(horizontal=True):
            dpg.add_text("If you don't have an account you can ")
            dpg.bind_item_font(dpg.last_item(), font_Normal)
            SingupButton("Singup")
            dpg.bind_item_font(dpg.last_item(), font_Normal)
        
        with dpg.group(tag="lb"): #Login Button so we can position it.
            posm=dpg.get_item_pos("lb") #Gets position of this group
            dpg.add_button(label="Login",pos=(posm[0]+400/2-60,posm[1]+190),width=100,height=40,callback=LoginCallback) #Changes our position
            dpg.bind_item_font(dpg.last_item(), font_Title) #Aplly font

def LogOut():
    global logedIn
    logedIn=False
    DelAll()
    dpg.configure_item("popup_SLO", show=True)
    ToggleStatus()

def MainContentWindow():
    DelAll()
    with dpg.window(label="Main Content", width=500,height=500, tag="MainContentWindow"):
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        dpg.add_input_text(default_value=UsersDatabase_getval(nickname,"textdoc"), multiline=True,callback=TextdocCallback)
        dpg.bind_item_font(dpg.last_item(), font_Normal)

def ToggleStatus():
    l=["Login/Singup","Logout"]
    currentlabel = dpg.get_item_configuration("losb")["label"]
    l.pop(l.index(currentlabel))
    dpg.configure_item("losb", label=l[0])
    

#--Deleting functions--
def DelLogin():
    dpg.delete_item("Login")

def DelSingup():
    dpg.delete_item("Singup")

def DelLoginOrSingup():
    dpg.delete_item("LoginOrSingup")

def DelMainContentWindow():
    dpg.delete_item("MainContentWindow")

def DelAll():
    if(dpg.does_item_exist("Login")) or (dpg.does_item_exist("Singup") or dpg.does_item_exist("LoginOrSingup") or dpg.does_item_exist("MainContentWindow")):
        DelLogin()
        DelSingup()
        DelLoginOrSingup()
        DelMainContentWindow()

#--Database functions--
def UsersDatabase_getfull():
    with open("usersdatabase.json", "r") as fp:
        udbj = json.load(fp)
    return udbj

def UsersDatabase_getval(user,key):
    with open("usersdatabase.json", "r") as fp:
        udbj = json.load(fp)
    return udbj[user][key]

def UsersDatabase_setval(user,key,val):
    with open("usersdatabase.json", "r") as fp:
        udbj = json.load(fp)
    udbj[user][key]=val
    with open("usersdatabase.json", "w") as fp:
        json.dump(udbj,fp, indent = 4)

def UsersDatabase_newuser(user):
    udbj=UsersDatabase_getfull()
    udbj[user]={"password":'',"textdoc":''}
    with open("usersdatabase.json", "w") as fp:
        json.dump(udbj,fp, indent = 4)

#---Popups---
def CreatePopup(name,text):
    with dpg.window(label=name,pos=(600/2-300/2,800/2-100/2), modal=True, show=False, tag=name, no_title_bar=True,width=300,height=30,no_move=True,no_resize=True):
        dpg.add_text(text)
        dpg.bind_item_font(dpg.last_item(), font_Normal)
        dpg.add_button(label="OK", width=280,height=25, callback=lambda: dpg.configure_item(name, show=False))
        dpg.bind_item_font(dpg.last_item(), font_Normal)

CreatePopup("popup_SL","You have successfully loged in.") #Successful Login
CreatePopup("popup_SS","You have successfully signed up.") #Successful Singup
CreatePopup("popup_SLO","You have successfully loged out.") #Successful Log out
CreatePopup("popup_IN","There is no such nickname.") #Incorrect Nickname
CreatePopup("popup_DN","There is already such nickname.") #Duplicate Nickname
CreatePopup("popup_SP","Password should be 4 numbers long.") #Small Password
CreatePopup("popup_SCP","Confrim Password should be 4 numbers long.") #Small Confirm Password
CreatePopup("popup_IP","Incorrect password.") #Incorrect Password
CreatePopup("popup_MP","Confirm password should match password.") #Match Password (confirm password should password)
CreatePopup("popup_EF","You need to fill all fields.") #Empty Fields
        
viewport=dpg.create_viewport(title="04_06_SchoolProject",width=600,height=800,resizable=False) #Setting of the viewport
dpg.setup_dearpygui()

with dpg.viewport_menu_bar(): #Creating viewport buttons
    dpg.add_menu_item(label="Login/Singup",callback=MenuButton,tag="losb") #Login Or SingUp button
    dpg.bind_item_font(dpg.last_item(), font_Normal)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()