from turtle import up
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Line Mover No1',width=500, height=530,resizable=False)

linePar={'x1':0,'y1':0,'x2':1,'y2':1} #Main dictionary which hold all settings of the circle (radius, pos(x,y))

def updateLinePar(sender, app_data, user_data): #function (dearpygui callback) that updates main dictionary and inserts new values 
    user_data[sender]=app_data #app_data - it is slider value
    updateLine()

def updateLine(): #function that redraws circle (deletes old, and draws new)
    dpg.delete_item('line')
    dpg.delete_item('secondLine1')
    dpg.delete_item('secondLine2')
    dpg.delete_item('secondLine3')
    dpg.delete_item('secondLine4')
    print(linePar)
    dpg.draw_line([linePar['x1']+220,210-linePar['y1']],[linePar['x2']+220,210-linePar['y2']],color=(255,255,255,255),tag='line',parent="viewport")
    dpg.draw_line([5,210-linePar['y2']],[linePar['x2']+220,210-linePar['y2']],tag='secondLine1',color=(255,0,0,255),parent="viewport") #1
    dpg.draw_line([linePar['x2']+220,430],[linePar['x2']+220,210-linePar['y2']],tag='secondLine2',color=(255,0,0,255),parent="viewport") #2
    dpg.draw_line([linePar['x1']+220,210-linePar['y1']],[435,210-linePar['y1']],tag='secondLine3',color=(0,0,255,255),parent="viewport") #3
    dpg.draw_line([linePar['x1']+220,210-linePar['y1']],[linePar['x1']+220,15],tag='secondLine4',color=(0,0,255,255),parent="viewport") #4

with dpg.window(label="Viewport",tag="viewport",pos=[10,10],width=465,height=465,no_resize=True): #main viewport window where circle is displayed.
    dpg.draw_line([linePar['x1'],linePar['y1']],[linePar['x2'],linePar['y2']],color=(255,255,255,255),tag='line')
    dpg.draw_line([linePar['x1'],linePar['y1']],[linePar['x2'],linePar['y2']],tag='secondLine1',color=(255,0,0,100)) #1
    dpg.draw_line([linePar['x1'],linePar['y1']],[linePar['x2'],linePar['y2']],tag='secondLine2',color=(255,0,0,100)) #2
    dpg.draw_line([linePar['x1'],linePar['y1']],[linePar['x2'],linePar['y2']],tag='secondLine3',color=(0,0,255,100)) #3
    dpg.draw_line([linePar['x1'],linePar['y1']],[linePar['x2'],linePar['y2']],tag='secondLine4',color=(0,0,255,100)) #4
    updateLine()
    
    dpg.add_slider_int(label='x1',tag='x1',default_value=0,min_value=-200,max_value=200,callback=updateLinePar,user_data=linePar,pos=[30 ,25],width=400)
    with dpg.group(horizontal=True):
        dpg.add_slider_int(label='y2',tag='y2',default_value=0,min_value=-200,max_value=200,callback=updateLinePar,user_data=linePar,vertical=True,pos=[5 ,40],height=400) #1
        dpg.add_slider_int(label='y1',tag='y1',default_value=0,min_value=-200,max_value=200,callback=updateLinePar,user_data=linePar,vertical=True,pos=[440,40],height=400)#2
    dpg.add_slider_int(label='x2',tag='x2',default_value=0,min_value=-200,max_value=200,callback=updateLinePar,user_data=linePar,pos=[25 ,438],width=400)
        
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()