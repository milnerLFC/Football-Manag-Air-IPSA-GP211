# -*- coding: utf-8 -*-
"""
FICHIER CONTENANT LES CLASSES
"""
import tkinter as tk
from tkinter import Label,Button,Entry,ttk

from PIL import Image, ImageTk
import pygame

import time

pygame.mixer.init()


class AutocompleteCombobox(ttk.Combobox):
    
    def __init__ (self,  *args, update_form = None,**kwargs):
        super ().__init__ ( *args, **kwargs)
        self.update_form = update_form


    def set_completion_list(self, completion_list):
            """Use our completion list as our drop down selection menu, arrows move through menu."""
            self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
            self._hits = []
            self._hit_index = 0
            self.position = 0
            self.bind('<KeyRelease>', self.handle_keyrelease)
            self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
            """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
            if delta: # need to delete selection otherwise we would fix the current position
                    self.delete(self.position, tk.END)
            else: # set position to end so selection starts where textentry ended
                    self.position = len(self.get())
            # collect hits
            _hits = []
            for element in self._completion_list:
                    if element.lower().startswith(self.get().lower()): # Match case insensitively
                            _hits.append(element)
            # if we have a new hit list, keep this in mind
            if _hits != self._hits:
                    self._hit_index = 0
                    self._hits=_hits
            # only allow cycling if we are in a known hit list
            if _hits == self._hits and self._hits:
                    self._hit_index = (self._hit_index + delta) % len(self._hits)
            # now finally perform the auto completion
            if self._hits:
                    self.delete(0,tk.END)
                    self.insert(0,self._hits[self._hit_index])
                    self.select_range(self.position,tk.END)
                    
    # def update_form(self, event):
    #     return
                    
    def handle_keyrelease(self, event):
            try:
                self.update_form(event)
            except:pass
            """event handler for the keyrelease event on this widget"""
            if event.keysym == "BackSpace":
                    self.delete(self.index(tk.INSERT), tk.END)
                    self.position = self.index(tk.END)
            if event.keysym == "Left":
                    if self.position < self.index(tk.END): # delete the selection
                            self.delete(self.position, tk.END)
                    else:
                            self.position = self.position-1 # delete one character
                            self.delete(self.position, tk.END)
            if event.keysym == "Right":
                    self.position = self.index(tk.END) # go to end (no selection)
            if len(event.keysym) == 1:
                    self.autocomplete()

                    

class auto_resize(tk.Frame):
    def __init__(self, master, *pargs):
        tk.Frame.__init__(self, master, *pargs)

        self.image = Image.open(r"images/backgrounds/menu.png")
        self.img_copy= self.image.copy()


        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        self.background.bind('<Configure>', self._resize_image)


    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height
        # print(new_width, new_height)

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)
        
class hover_button(Button):
    def __init__(self, master, **kw):
        Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self["background"] = self["activebackground"]
        self["foreground"] = self["activeforeground"]
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("sounds/mouseover.wav"))
    
    def on_leave(self, e):
        self["background"] = self.defaultBackground
        self["foreground"] = self.defaultForeground

        
class cursor_entry_int(Entry):
    def __init__(self, master, default_text = '',minvalue = 0, maxvalue = 0,**kw):
        Entry.__init__(self, master=master, **kw)
        self.default_text = default_text
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.insert(tk.END,self.default_text)
        self.bind("<Button-1>", self.clearEntry)
        self.bind("<Leave>", self.testEntry)
    
    def testEntry(self,e):
        try:
            value = int(self.get())
            if isinstance(value, int) == True:
                if value >= self.minvalue and value <= self.maxvalue:
                    pass
                else:
                    self.delete(0, "end")
                    self.insert(tk.END,self.default_text)                    
        except:
            self.delete(0, "end")
            self.insert(tk.END,self.default_text)
        
    def clearEntry(self, e):
        try:
            value = int(self.get())
            if isinstance(value, int) == True:
                pass
        except:
            self.delete(0, "end")
        
    def deleter(self):
        self.delete(0, "end")
        self.insert(tk.END,self.default_text)        
            
class cursor_entry_str(Entry):
    def __init__(self, master,default_text = '', **kw):
        Entry.__init__(self, master=master, **kw)
        self.default_text = default_text
        self.insert(tk.END,self.default_text)
        self.bind("<Button-1>", self.clearEntry)
        self.bind("<Leave>", self.testEntry)
        
    def clearEntry(self, e):
        value = self.get()
        try:
            if any(char.isdigit() for char in value) or value == 'Nom du Joueur':
                self.delete(0, "end")
        except:
            pass
        
    def testEntry(self,e):
        value = self.get()
        try:
            if any(char.isdigit() for char in value):
                self.delete(0, "end")
                self.insert(tk.END,self.default_text)
        except:
            pass
        if len(value) == 0:
            self.insert(tk.END,self.default_text)
        
    def deleter(self):
        self.delete(0, "end")
        self.insert(tk.END,self.default_text)       

        
class Clock(tk.Label):
    """ Class that contains the clock widget and clock refresh """

    def __init__(self, parent=None, seconds=True, colon=False):
        """
        Create and place the clock widget into the parent element
        It's an ordinary Label element with two additional features.
        """
        tk.Label.__init__(self, parent)

        self.display_seconds = seconds
        if self.display_seconds:
            self.time     = time.strftime('%H:%M:%S')
        else:
            self.time     = time.strftime('%H:%M:%S').lstrip('0')
        self.display_time = self.time
        self.configure(text=self.display_time)

        if colon:
            self.blink_colon()

        self.after(200, self.tick)


    def tick(self):
        """ Updates the display clock every 200 milliseconds """
        if self.display_seconds:
            new_time = time.strftime('%H:%M:%S')
        else:
            new_time = time.strftime('%H:%M:%S').lstrip('0')
        if new_time != self.time:
            self.time = new_time
            self.display_time = self.time
            self.config(text=self.display_time)
        self.after(200, self.tick)


    def blink_colon(self):
        """ Blink the colon every second """
        if ':' in self.display_time:
            self.display_time = self.display_time.replace(':',' ')
        else:
            self.display_time = self.display_time.replace(' ',':',1)
        self.config(text=self.display_time)
        self.after(1000, self.blink_colon)

