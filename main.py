import numpy as np
import pyautogui
import keyboard
import cv2
import PIL
import sys
from PIL import Image,ImageTk
from tkinter import *

from tkinter import filedialog



#/////////////////////////////////////////////////////////////////////////

window = Tk() 

titlephoto = PhotoImage(file='titlephoto.png')

window.iconphoto(False, titlephoto)

def quit():
       import sys;sys.exit()

# //////////////////////////////////////////////////////////



# Drawer // Warning Script is controlling

def drawer(img):

    max_y, max_x= img.shape

    current_mouse_x, current_mouse_y = pyautogui.position() 

    #Checks
    #print(img.shape)
    #print(max_x, max_y)

    def controller(x, y):
        pyautogui.click(current_mouse_x + x, current_mouse_y + y) #To avoid clicking interface currently hardcoded for ms paint (old one) try to add to start from mouse position
        pyautogui.PAUSE = 0.00000001

    def drawing(img):
        cv2.waitKey(5000)

        x = 0
        y = 0

        while True:
            try:
                if img[y][x] != 0 : #Checking what is the value of pixel
                    #print([x, y])
                    controller(x, y)
            
            except Exception :
                pass
            
            if x < max_x :
                x+=1
            else :
                x = 0 
                y+=1

            if y >= max_y :
                break

            # Script control for User
            
            if keyboard.is_pressed('ctrl+h'):
                cv2.waitKey(5000)

            if keyboard.is_pressed('ctrl+q'):
                break
    
    # Intialising

    drawing(img)


#///////////////////////////////////////////////////////////




# Picture Processing



def processing(img):
    
    window_processing = Tk()
    window_processing.geometry('550x1050')
    window_processing.title('Parameters')

    # Checkbox for color
    col = IntVar(master=window_processing)
    if_col = Checkbutton(master=window_processing, variable=col, text = 'Color Editing (Draw Not Available)')
    if_col.pack()

    

    # Panned Windows

    gussian_blur = PanedWindow(master=window_processing, orient=VERTICAL)
    gussian_blur.pack(pady=10)

    bilateral_filtering = PanedWindow(master=window_processing, orient=VERTICAL)
    bilateral_filtering.pack(pady=10)

    # Bilateral Heading
    
    bilateral_filtering_heading = Label(master=window_processing, text='Bilateral Filtering', font=4)
    bilateral_filtering.add(bilateral_filtering_heading)

    l = Label(master=window_processing)
    l.pack()

    # Guassian Heading

    gussian_blur_heading = Label(master=window_processing, text='Guassian Blur', font=4)
    gussian_blur_heading.pack()

    gussian_blur.add(gussian_blur_heading)


    #check
    cv2.imshow('Original', img)


    
    # Workings
    
    def under_hood_processing_guassian(img, par1, par2, par3):
        
        print(col.get())

        if col.get() == 0 : #Checking the status of checked

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            gray = cv2.GaussianBlur(gray, (par3, par3), 0)

            canny = cv2.Canny(gray, par1, par2)

            name = 'Guassian Par- '+str(par1)+' Par2- '+str(par2)+' Par3- '+str(par3)

            to_show = cv2.bitwise_not(canny)
            
            cv2.imshow(name,to_show)
        
        else :

            to_show = cv2.GaussianBlur(img, (par3, par3), 0)

            name = 'Guassian Color Par3- '+str(par3)
            
            cv2.imshow(name,to_show)

        
    def under_hood_processing_bilateral(img, d, s_color, s_space, par1, par2):

        print(col.get())

        if col.get() == 0 :

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            gray = cv2.bilateralFilter(img, d, s_color, s_space)

            canny = cv2.Canny(gray, par1, par2)

            name = 'Bilateral par1- '+str(par1)+' par2- '+str(par2)+' d- '+str(d)+' sigma color- '+str(s_color)+' sigma space- '+str(s_space)

            to_show = cv2.bitwise_not(canny)

            cv2.imshow(name, to_show)
        
        else :
            gray = cv2.bilateralFilter(img, d, s_color, s_space)
            name = 'Bilateral Color d- '+str(d)+' sigma color- '+str(s_color)+' sigma space- '+str(s_space)

            cv2.imshow(name, gray)
    
    

    # Controls

    def show():
        
        under_hood_processing_guassian(img, int(par_1.get()), int(par_2.get()), int(par_3.get()))

    def show_bilateral():
        
        under_hood_processing_bilateral(img, int(d_bilateral.get()), int(sigma_color.get()), int(sigma_space.get()), int(par_1_b.get()), int(par_2_b.get()))
        
    
    def draw_g():
        par1, par2, par3 = int(par_1.get()), int(par_2.get()), int(par_3.get())

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (par3, par3), 0)

        canny = cv2.Canny(gray, par1, par2)

        drawer(canny)
        
        

    def draw_b():
        d, s_color, s_space, par1, par2 = int(d_bilateral.get()), int(sigma_color.get()), int(sigma_space.get()), int(par_1_b.get()), int(par_2_b.get())

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        gray = cv2.bilateralFilter(img, d, s_color, s_space)

        canny = cv2.Canny(gray, par1, par2)

        drawer(canny)

        

    def save_g():
        par1, par2, par3 = int(par_1.get()), int(par_2.get()), int(par_3.get())
        
        if col.get() == 0 :
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            gray = cv2.GaussianBlur(gray, (par3, par3), 0)

            canny = cv2.Canny(gray, par1, par2)

            name = 'Guassian Par- '+str(par1)+' Par2- '+str(par2)+' Par3- '+str(par3)+'.png'

            to_show = cv2.bitwise_not(canny)

            cv2.imwrite(name, to_show)

        else :
            to_show = cv2.GaussianBlur(img, (par3, par3), 0)

            name = 'Guassian Color Par3- '+str(par3)+'.png'

            cv2.imwrite(name,to_show)
        

    def save_b():
        d, s_color, s_space, par1, par2 = int(d_bilateral.get()), int(sigma_color.get()), int(sigma_space.get()), int(par_1_b.get()), int(par_2_b.get())

        if col.get() == 0 :

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            gray = cv2.bilateralFilter(img, d, s_color, s_space)

            canny = cv2.Canny(gray, par1, par2)

            name = 'Bilateral par1- '+str(par1)+' par2- '+str(par2)+' d- '+str(d)+' sigma color- '+str(s_color)+' sigma space- '+str(s_space)+'.png'

            to_show = cv2.bitwise_not(canny)

            cv2.imwrite(name, to_show)
        
        else :
            gray = cv2.bilateralFilter(img, d, s_color, s_space)
            name = 'Bilateral Color d- '+str(d)+' sigma color- '+str(s_color)+' sigma space- '+str(s_space)+'.png'

            cv2.imwrite(name, gray)

    
    
    
    # Guassian Options

    par_1_label = Label(master=window_processing, text='Canny Parameter 1 (0 to 255) ')
    par_1_label.pack()
    par_1 = Entry(master=window_processing)
    par_1.pack()

    gussian_blur.add(par_1_label)
    gussian_blur.add(par_1)

    par_2_label = Label(master=window_processing, text='Canny Parameter 2 (0 to 255) ')
    par_2_label.pack()
    par_2 = Entry(master=window_processing)
    par_2.pack()

    gussian_blur.add(par_2_label)
    gussian_blur.add(par_2)

    par_3_label = Label(master=window_processing, text='Gaussian Blur (Kernel) ')
    par_3_label.pack()
    par_3 = Entry(master=window_processing)
    par_3.pack()

    gussian_blur.add(par_3_label)
    gussian_blur.add(par_3)

   
    button_show_results = Button(master=window_processing,
                                 text='Show',
                                 command=show)     
    
    button_show_results.pack()
    gussian_blur.add(button_show_results)

    
    button_draw_g = Button(master=window_processing,
                         text = 'Draw',
                         command=draw_g)
    button_draw_g.pack()
    gussian_blur.add(button_draw_g)

    
    button_save_g = Button(master=window_processing,
                         text = 'Save',
                         command=save_g)

    button_save_g.pack()
    gussian_blur.add(button_save_g)

    
   
   
   
    # Bilateral Options
    par_1_label_b = Label(master=window_processing, text='Canny Parameter 1 (0 to 255) ')
    par_1_label_b.pack()
    par_1_b = Entry(master=window_processing)
    par_1_b.pack()

    bilateral_filtering.add(par_1_label_b)
    bilateral_filtering.add(par_1_b)

    
    par_2_label_b = Label(master=window_processing, text='Canny Parameter 2 (0 to 255) ')
    par_2_label_b.pack()
    par_2_b = Entry(master=window_processing)
    par_2_b.pack()

    bilateral_filtering.add(par_2_label_b)
    bilateral_filtering.add(par_2_b)

    d_label = Label(master=window_processing, text='Distance')
    d_label.pack()

    d_bilateral = Entry(master=window_processing)
    d_bilateral.pack()

    bilateral_filtering.add(d_label)
    bilateral_filtering.add(d_bilateral)
    
    sigma_color_label = Label(master=window_processing, text='Sigma Color')
    sigma_color_label.pack()

    sigma_color = Entry(master=window_processing)
    sigma_color.pack()

    bilateral_filtering.add(sigma_color_label)
    bilateral_filtering.add(sigma_color)

    sigma_space_label = Label(master=window_processing, text='Sigma Space')
    sigma_space_label.pack()
    
    sigma_space = Entry(master=window_processing)
    sigma_space.pack()

    bilateral_filtering.add(sigma_space_label)
    bilateral_filtering.add(sigma_space)


    button_show_bilateral = Button(master=window_processing,
                                    text='Show',
                                    command=show_bilateral)
    
    button_show_bilateral.pack()
    bilateral_filtering.add(button_show_bilateral)

    
    
    button_draw_bi = Button(master=window_processing,
                         text = 'Draw',
                         command=draw_b)
    
    button_draw_bi.pack()
    bilateral_filtering.add(button_draw_bi)


    button_save_bi = Button(master=window_processing,
                         text = 'Save',
                         command=save_b)

    button_save_bi.pack()
    bilateral_filtering.add(button_save_bi)
    

    
    # Instruction

    instruction_heading = Label(master=window_processing, text='Instruction for Starting Draw: ', font=3)
    instruction_heading.pack()

    instruction1 = Label(master=window_processing, text='1. Open Desired Software and choose smallest pencil or brush.')
    instruction2 = Label(master=window_processing, text='2. Click on draw and switch to the software and place mouse on draw location.\n(wait time is 5 sec)')
    instruction3 = Label(master=window_processing, text='3. Do not disturb when mouse is in control of script')
    instruction4 = Label(master=window_processing, text='4. You can use following keyboard commands')
    instruction5 = Label(master=window_processing, text='Halt for 5 sec -- CTRL + H \nQuit Script -- CTRL + Q\nThis Function is tested in Microsoft Paint only.')

    instruction1.pack()
    instruction2.pack()
    instruction3.pack()
    instruction4.pack()
    instruction5.pack()
    


    window_processing.mainloop()




# ////////////////////////////////////////////////////////////






# Browse Next 

def nextt():
    window_browse_process = Tk()
    window_browse_process.title("Adjust Photo")
    window_browse_process.geometry("800x300")

    l = Label(master=window_browse_process)
    l.pack()

    def forward():
        height.configure(state=DISABLED)
        width.configure(state=DISABLED)

        browse_forward_img = cv2.resize(img, (int(width.get()), int(height.get())))
        l.browse_forward_img = browse_forward_img

        processing(browse_forward_img)
        
        window_browse_process.configure(state = DISABLED)

    button_next = Button(master=window_browse_process,
                         text='Next', 
                         font=3,
                         width=15,
                         height=5,
                         command=forward)
    button_next.pack()

    height_label = Label(master=window_browse_process, text="Height")
    height_label.pack()
    height = Entry(master=window_browse_process)
    height.pack()


    width_label = Label(master=window_browse_process, text="Width")
    width_label.pack()
    width = Entry(master=window_browse_process)
    width.pack()


    # //// Add resize ability
    img = cv2.imread(file_path)
    
    

    window_browse_process.mainloop()



# //////////////////////////////////////////////////////////////





# Camera Option

def cam():
    window_camera = Tk()
    window_camera.title('Take Photo')
    window_camera.geometry("700x700")

    snapped = False

    l= Label(master=window_camera)
    l.pack()
    
    height = 500
    width = 800
    
    camm=cv2.VideoCapture(0)
    camm.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camm.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def snap():
        camm.release()
        video_feed.configure(state=DISABLED)
        
        global captured_photo
        captured_photo = frame
        l.captured_photo = captured_photo
        processing(captured_photo)
        global snapped
        snapped = True
       

        
    
    
    def show_frame():
        #print(snapped)
        if snapped == False :
            global frame
            
            _, frame = camm.read()
            
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            
            img = PIL.Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img, master=window_camera)
            
            video_feed.imgtk = imgtk
            video_feed.configure(image=imgtk)
            video_feed.after(10, show_frame)
        

    video_feed = Label(window_camera)
    video_feed.pack()


    button_snap = Button(window_camera,
                         text='Snap!!!',
                         font=5,
                         height=5,
                         width=20,
                         command=snap)
    button_snap.pack()
    
    show_frame()
    
    window_camera.mainloop()





# ///////////////////////////////////////////////////////    

    



# Browse Option

def browse():

    # Function for opening the  browser 
    def browseFiles(): 
        filename = filedialog.askopenfilename(initialdir = "/", 
                                            title = "Select a Photo", 
                                            filetypes = (("jpg files",
                                                            "*.jpg*")
                                                            ,("jpeg files", 
                                                            "*.jpeg*"),
                                                            ("png files",
                                                            "*.png*"), 
                                                        ("All files", 
                                                            "*.*"))) 
        
        # Change label contents to show photo path 
        label_file_explorer.configure(text="Selected File : "+filename)
        
        
        # for using in other module
        global file_path
        file_path = filename 

    window_browse = Tk()

    # window title 
    window_browse.title('Autodraw') 
    
    # window size 
    window_browse.geometry("800x300") 
        
    window_browse.config(background = "white") 
        
    label_file_explorer = Label(window_browse,  
                                text = "Open Photo", 
                                width = 100, height = 4,  
                                fg = "blue") 
    
        
    button_explore = Button(window_browse,  
                            text = "Browse Files", 
                            command = browseFiles)  
    
    button_exit = Button(window_browse,  
                        text = "Exit",
                        fg="red", 
                        command = quit)  

    button_next = Button(window_browse, 
                        text = "Next",
                        fg="green",
                        command= nextt)
    

    # Layout   
    label_file_explorer.grid(column = 1, row = 1, pady=5) 
    
    button_explore.grid(column = 1, row = 2, pady=5) 
    
    button_exit.grid(column = 1,row = 6, pady=5) 

    button_next.grid(column=1, row=4, pady=5)


    
    window_browse.mainloop()





# /////////////////////////////////////////////////////


#Starting GUI
window.title('Autodraw')
window.geometry('400x100')

button_camera = Button(window,
                       text='Camera',
                       height=4,
                       width=11,
                       font=5,
                       command=cam)

button_browse = Button(window,
                       text='Browse',
                       height=4,
                       width=11,
                       font=5,
                       command = browse)

button_exit = Button(window,
                     text='Exit',
                     fg='red',
                     height=4,
                     width=11,
                     font=5,
                     command=quit)


button_camera.grid(row=1, column=1, pady=10)
button_browse.grid(row=1, column=2, pady=10)
button_exit.grid(row=1, column=3, pady=10)

window.mainloop() 


# Feels Section : 

# Never forget who is whose master and if possible mention it, in future it will safe you a ass lot of time.
# Garbage collector is the real villain here
# Always release camera when you are done using it
# Live stuff is not transferred well, you can but you gonna get a lot of errors.