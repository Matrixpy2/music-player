import customtkinter
from customtkinter import CTkFrame as Frame
from customtkinter import CTkButton as Button
from customtkinter import CTkImage ,CTkLabel , CTkSlider , IntVar
from CTkListbox import CTkListbox
from PIL import Image
from tkinter.filedialog import askopenfilename
import shutil ,os
import pygame
from tkinter.messagebox import showwarning
import music_tag
import time

class Main(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry('850x600')
        self.title('Music Player')
        pygame.mixer.init()
        
        # add play list function
        def add():
            x= askopenfilename(title='choose song' , filetypes=(('Mp3 Songs', '*.mp3'),))
            try:
                shutil.copy(x , 'musics')
            except:
                showwarning('error' , 'the same file')   
        self.mount_list=0
        def show_song():
            self.list_box.delete(0 , 'end')
            musics = os.listdir('musics')
            try:
                for music in musics:
                    self.list_box.insert('end' , music)
                    self.mount_list+=1
                
                    
            except:
                showwarning(title='salam' , message='salam')
            print(self.mount_list)
            
        
        #  Frames
        self.grid_rowconfigure(0 , weight=2)
        self.grid_rowconfigure(1 , weight=2)
        self.grid_columnconfigure(0 , weight=4)
        self.grid_columnconfigure(1, weight=2)
        
        self.main_Frame = Frame(self , fg_color='transparent')
        self.main_Frame.grid(row=0 , column=0, columnspan=2 , pady=25 , padx=25 , sticky='nsew' )
        self.sidebar_Frame = Frame(self , fg_color='transparent')
        self.sidebar_Frame.grid(row =0 , column=2  , padx=15 , pady=15 , sticky='ns')
        self.controler_Frame = Frame(self , fg_color='transparent')
        self.controler_Frame.grid(row=1 , column=0 , columnspan=2 , sticky='nsew' , pady=15 , padx=15)
        self.Button = Button(self , text='add to play list' , command=add)
        self.Button.grid(row=1 , column=2 , )
        
        # function for slider
        self.slider_state = IntVar(value=0)
        def select_item(choose):
            index = self.list_box.curselection()
            name = self.list_box.get(index)
            pygame.mixer_music.load(f'musics/{name}')
            pygame.mixer_music.play()
            pygame.mixer_music.set_pos(choose)
            self.real_time.set(choose)
            # self.slider_state.set(choose)
        
        
        # controler
        self.controler_Frame.grid_rowconfigure(1 , weight=1)
        self.controler_Frame.columnconfigure((0,2) ,weight=1)
        self.controler_Frame.columnconfigure(1 , weight=3)
        self.start_time=CTkLabel(self.controler_Frame , text='00:00')
        self.start_time.grid(row=1 , column=1)
        self.slider_time =customtkinter.CTkSlider(self.controler_Frame , from_=0 , to=100, variable=self.slider_state , command=select_item )
        self.slider_time.grid(row=1 , column=2 ,columnspan=3 , sticky='ew')
        self.end_time =CTkLabel(self.controler_Frame ,text='00:00')
        self.end_time.grid(row=1 ,column=5)
        
        # controler functions
        self.real_time= IntVar(value=0)
        def start():
            if pygame.mixer_music.get_busy():  
                current_time = self.real_time.get()+int((pygame.mixer_music.get_pos() + 1) / 1000)
                formatted_time = time.strftime('%M:%S', time.gmtime(current_time))
                self.start_time.configure(text=formatted_time)
                self.slider_state.set(current_time)
                print((self.slider_state))
            self.start_time.after(1000, start)
        def end():
            music_index=self.list_box.curselection()
            music_name=self.list_box.get(music_index)
            mp3=music_tag.load_file(f'musics/{music_name}')
            len_time =int(mp3['#length'])
            self.slider_time.configure(to=len_time)
            format_time=time.strftime('%M:%S' , time.gmtime(len_time))
            self.end_time.configure(text=format_time)
            
            
            
        
        def volume(choose):
            pygame.mixer_music.set_volume(choose/100)
            self.volume_state.set(choose)
        
        self.volume_state=IntVar(value=50)
        
        self.volume = customtkinter.CTkSlider(self, from_=0 , to=100 ,  orientation='vertical' , variable=self.volume_state ,command=volume ,number_of_steps=100)
        self.volume.grid(row=0 , column=1)
        # List box
        
        self.sidebar_Frame.grid_rowconfigure(0 , weight=1)
        self.sidebar_Frame.grid_columnconfigure(0 , weight=1)
        self.list_box= CTkListbox(self.sidebar_Frame , fg_color='black' )
        self.list_box.grid(row=0 , column=0 , sticky='nsew')
        # album image
        self.main_Frame.grid_rowconfigure(0 , weight=1)
        self.main_Frame.grid_columnconfigure(0 , weight=1)
        self.album_image = customtkinter.CTkLabel(self.main_Frame ,text='', image=CTkImage(Image.open('assets/album.jpg'), size=(350,350) ))
        self.album_image.grid(row =0 ,column= 0 ,sticky='ns'  )
        
        # Button controler
        def play():
            self.slider_state.set(value=0)
            self.real_time.set(value=0)
            try:
                music_index=self.list_box.curselection()
                start()
                end()
                # print(music_index)
                music_name = self.list_box.get(music_index)
                mp3=music_tag.load_file(f'musics/{music_name}')
                album_image=mp3['artwork'].first.data
                with open('assets/image.jpg' ,'wb') as photo:
                    photo.write(album_image)
                self.album_image.configure(image=CTkImage(Image.open('assets/image.jpg'), size=(350,350) ))
                
                pygame.mixer_music.load(f'musics/{music_name}')
                pygame.mixer_music.play()
                album_art =mp3['artwork'].first.data
                self.album_image.configure(album_art)
            except:
                showwarning('error' , 'select a song')
        self.i=0
        def pause():
            if self.i ==0:
                pygame.mixer_music.pause()
                self.i+=1
            elif self.i==1:
                pygame.mixer_music.unpause()
                self.i-=1
            else:
                print(self.i)
                
        def next():
            index=self.list_box.curselection()
            self.slider_state.set(value=0)
            self.real_time.set(value=0)
            try:
                self.list_box.activate(index+1)
                play()
            except:
                self.list_box.activate(0)
                play()

        def previous():
            index=self.list_box.curselection()
            self.slider_state.set(value=0)
            self.real_time.set(value=0)
            try:
                self.list_box.activate(index-1)
                play()
            except:
                self.list_box.activate(len(self.mount_list))
                play()
        def stop():
            pygame.mixer_music.stop()
            self.slider_state.set(value=0)
            self.real_time.set(value=0)
        
        
        
        
        
        # Buttons
        self.controler_Frame.grid_columnconfigure(tuple(i for i in range(7)) , weight=1)
        self.controler_Frame.grid_rowconfigure(0 , weight=1)
        self.previous =Button(self.controler_Frame ,image=CTkImage(Image.open('assets/previous.jpg') , size=(50,50)),text='', fg_color='transparent' , command=previous)
        self.previous.grid(row=0 , column=1)
        self.stop = Button(self.controler_Frame , image=CTkImage(Image.open('assets/stop.jpg') , size=(50,50)),text='', fg_color='transparent' , command=stop)
        self.stop.grid(row =0 , column=2 )
        self.play = Button(self.controler_Frame , image=CTkImage(Image.open('assets/play.jpg') , size=(50,50)),text='', fg_color='transparent' , command=play)
        self.play.grid(row = 0 , column=3)
        self.pause =Button(self.controler_Frame , image=CTkImage(Image.open('assets/pause.png') , size=(50,50)),text='', fg_color='transparent' ,command=pause)
        self.pause.grid(row = 0 , column=4)
        self.next = Button(self.controler_Frame, image=CTkImage(Image.open('assets/next.jpg') , size=(50,50)),text='', fg_color='transparent' , command=next)
        self.next.grid(row =0 , column =5)
        
        show_song()      
        
        