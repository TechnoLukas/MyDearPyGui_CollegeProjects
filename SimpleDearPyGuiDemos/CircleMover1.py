import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Circle Mover No1',width=500, height=800)

cirPar={'radius':10,'x':0,'y':0} #Main dictionary which hold all settings of the circle (radius, pos(x,y))

def updateCirPar(sender, app_data, user_data): #function (dearpygui callback) that updates main dictionary and inserts new values 
    user_data[sender]=app_data #app_data - it is slider value
    updateCir(user_data)

def updateCir(user_data): #function that redraws circle (deletes old, and draws new)
    dpg.delete_item('circle')
    dpg.draw_circle([user_data['x']+220,210-(user_data['y'])],user_data['radius'],tag='circle',parent="viewport")

def resetCirPar(): #reset function (dearpygui callback) that reset everything to default value (dictionary, circle, sliders)
    parameters={'radius':10,'x':0,'y':0}
    dpg.set_value('x',0);dpg.set_value('y',0),dpg.set_value('radius',10)
    updateCirPar('radius',10,cirPar);updateCirPar('x',0,cirPar);updateCirPar('y',0,cirPar) #force callback
    updateCir(parameters)

with dpg.window(label="Viewport",tag="viewport",pos=[10,10],width=465,height=465): #main viewport window where circle is displayed.
    dpg.draw_circle([cirPar['x'],cirPar['y']],cirPar['radius'],tag='circle')
    updateCir(cirPar)

with dpg.window(label="Settings",pos=[10,485],width=465,height=265): #settings window where parameters sliders and reset button positioned
    with dpg.group(horizontal=True):
        dpg.add_text('radius:')
        dpg.add_slider_int(label='',tag='radius',default_value=0,min_value=2,max_value=100,callback=updateCirPar,user_data=cirPar)
    with dpg.group(horizontal=True):
        dpg.add_text('x:     ')
        dpg.add_slider_int(label='',tag='x',default_value=0,min_value=-200,max_value=200,callback=updateCirPar,user_data=cirPar)
    with dpg.group(horizontal=True):
        dpg.add_text('y:     ')
        dpg.add_slider_int(label='',tag='y',default_value=0,min_value=-200,max_value=200,callback=updateCirPar,user_data=cirPar)

    dpg.add_button(label='Reset',tag='reset',callback=resetCirPar)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()