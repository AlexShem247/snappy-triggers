import tkinter as tk
from tkinter import messagebox
import time
import sys
import pygame
import threading
import imageio

from random import randint
from tkinter import ttk
from PIL import ImageTk, Image

sys.path.append("Modules") # Import modules from Modules directory

import singlePlayer

video = imageio.get_reader("images/intro_video.mp4")

def showVideo(label):

    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        label.config(image=frame_image)
        label.image = frame_image
        time.sleep(0.01)
    time.sleep(5)
    showVideo(label)


class MainScreen:
    """GUI for the Main Screen"""

    def __init__(self, root):
        # Config Window
        self.root = root
        self.root.title("Snappy Triggers - Main Screen")
        self.root.iconbitmap("images/logo.ico")
        self.root.geometry("1280x720+60+25")
        self.root["bg"] = "gray10"

        self.root.state("zoomed")  # Maximises root window

        # Sets game settings to default
        self.gameFPS = 60
        self.gameVolume = 0.8
        self.gameColor = "blue"

        self.homeMenu()


    def homeMenu(self):
        """Home Menu for if there is no saved users"""
        # Create Objects in Window
        videoLabel = tk.Label(self.root)
        videoLabel.pack(pady=(20, 5))
        thread = threading.Thread(target=showVideo, args=(videoLabel,))
        thread.daemon = 1
        thread.start()

        d = {}
        for c in (65, 97):
            for i in range(26):
                d[chr(i+c)] = chr((i+13) % 26 + c)

        tk.Label(self.root,
                 text="".join([d.get(c, c) for c in "Tnzr znqr ol Nyrknaqre Furznyl"]),
                 font="Arial 14", bg="gray10", fg="gray80").pack(pady=(5, 15))

        tk.Button(self.root, text="Play", font="Arial 28 bold", bg="gray40", fg="white",
                  command=self.playSingleplayer).pack(pady=13, ipadx=130)
        tk.Button(self.root, text="View Rules", font="Arial 28 bold", bg="gray40",
                  fg="white", command=self.viewRules).pack(pady=13, ipadx=70)
        tk.Button(self.root, text="Quit", font="Arial 28 bold", bg="gray40", fg="white",
                  command=self.root.destroy).pack(pady=13, ipadx=130)


    def close_window(self, window):
        """Maximises root window before destroying child window"""
        self.root.state("zoomed")  # Maximises root window
        window.destroy()
        
        
    def pauseGame(self, fps, volume, crosshairColor):
        """ Pauses game and opens up tkinter window """ 
        endGame = False
        
        def getValues(*args):
            """ Gets values from widgets"""
            nonlocal fps, volume, crosshairColor
            fps = int(entry_fps.get())
            volume = entry_volume.get()/100
            crosshairColor = entry_Color.get().lower()
            pauseWin.wm_state("iconic")
            pauseWin.quit()
            
        def quitGame():
            """ Shows pop-up box before closing game """
            nonlocal endGame
            response = messagebox.askyesno("Quit Game", "Are you sure you want to quit the game?\
                                              \n\nAll progress will be lost.", icon="warning")
            if response:
                pauseWin.wm_state("iconic")
                pauseWin.quit()
                pygame.quit()
                
        def updateText(*args):
            """ Upates text color label """
            textColor.config(text=entry_Color.get().title())
        
        pauseWin = tk.Tk()
        pauseWin.title("Snappy Triggers - Paused")
        pauseWin.iconbitmap("images/logo.ico")
        pauseWin.geometry("440x240+400+200")
        pauseWin["bg"] = "gray10"
        pauseWin.protocol("WM_DELETE_WINDOW", getValues)
        
        # Create text
        tk.Label(pauseWin, text="Frames per Second:", font="Arial 14 bold",
                 bg="gray10", fg="white").grid(row=1, column=0, pady=(20, 10), padx=(20, 0), sticky="e")
        tk.Label(pauseWin, text="Main volume:", font="Arial 14 bold",
                 bg="gray10", fg="white").grid(row=2, column=0, pady=10, padx=(20, 0), sticky="e")
        tk.Label(pauseWin, text="Crosshair Colour:", font="Arial 14 bold",
                 bg="gray10", fg="white").grid(row=3, column=0, pady=10, padx=(20, 0), sticky="e")
    
        # Create Spinbox
        entry_fps = tk.Spinbox(pauseWin, from_=5, to=100, increment=5, font="Arial 14", width=5)
        entry_fps.grid(row=1, column=1, sticky="w", padx=20, pady=(20, 10))
        entry_fps.delete(0, "end")
        entry_fps.insert(0, fps)
    
        # Create Slider
        entry_volume = tk.Scale(pauseWin, from_=0, to=100, orient="horizontal",
                                     length=150, font="Arial 14", fg="white", bg="gray10", highlightthickness=0)
        entry_volume.grid(row=2, column=1, sticky="w", padx=20)
        entry_volume.set(volume * 100)
    
        # Create Dropbox
        entry_Color = tk.StringVar()
        entry_Color.set(crosshairColor.title())
        
        colorFrame = tk.LabelFrame(pauseWin, bg="gray10", relief="flat")
        colorFrame.grid(row=3, column=1)
        
        textColor = tk.Label(colorFrame, text=entry_Color.get().title(),
                             bg="gray40", fg="white", font="Arial 14 bold")
        textColor.grid(row=0, column=0, pady=10, sticky="w", ipady=3, ipadx=10)
    
        dropColors = tk.OptionMenu(colorFrame, entry_Color, "Blue", "Red", "Green", "Yellow", command=updateText)
        dropColors.config(bg="gray40", fg="white", font="Arial 12 bold", highlightthickness=0)
        dropColors.grid(row=0, column=1, sticky="e", padx=20)
    
        # Create Button
        tk.Button(pauseWin, text="Resume", font="Arial 16 bold", bg="gray40", fg="white",
                  command=getValues).grid(row=4, column=0, pady=20, ipadx=30, padx=20)
        
        tk.Button(pauseWin, text="Quit Game", font="Arial 16 bold", bg="gray40", fg="white",
                  command=quitGame).grid(row=4, column=1, pady=20, ipadx=30, padx=20)
        
        fps = int(entry_fps.get())
        volume = entry_volume.get()/100
        crosshairColor = entry_Color.get().lower()
        
        pauseWin.bind("<Escape>", getValues)
        pauseWin.mainloop()
        pauseWin.destroy()
        
        return fps, volume, crosshairColor, endGame
        
    
    def playSingleplayer(self):
        """Starts singleplayer gamemode"""
        self.score, self.bossDefeated, self.gameFPS, self.gameVolume, self.gameColor = \
            singlePlayer.startGame(self.gameFPS, self.gameVolume, self.gameColor, self.pauseGame)

        self.root.state("zoomed")  # Maximises root window            

    def viewRules(self):
        """Opens window containing Game Rules"""
        self.rulesWin = tk.Toplevel()
        self.rulesWin.title("Snappy Triggers - Rules")
        self.rulesWin.iconbitmap("images/logo.ico")
        self.rulesWin.geometry("800x750+100+25")
        self.rulesWin["bg"] = "gray10"
        self.rulesWin.protocol("WM_DELETE_WINDOW", lambda: self.close_window(self.rulesWin))

        self.root.wm_state("iconic")  # Minimises root window

        # Create text
        tk.Label(self.rulesWin, text="Game Rules", font="Arial 30 bold underline",
                 bg="gray10", fg="white").pack(padx=5, pady=10)

        tk.Label(self.rulesWin, text="In every round, multiple targets will appear on-screen. The objective",
                 font="Arial 16", bg="gray10", fg="white").pack(padx=20, pady=(10, 0))
        tk.Label(self.rulesWin, text="of the game is to shoot as many targets within the time limit as possible.",
                 font="Arial 16", bg="gray10", fg="white").pack(padx=20, pady=0)

        tk.Label(self.rulesWin, text="There are three different levels, each with it's own unique enemies",
                 font="Arial 16", bg="gray10", fg="white").pack(padx=20, pady=(20, 0))
        tk.Label(self.rulesWin, text="and themes. Shooting enemies give you points. Some enemies will give",
                 font="Arial 16", bg="gray10", fg="white").pack(padx=20, pady=0)
        tk.Label(self.rulesWin, text="you more points and some will give you minus points, depending on its type.",
                 font="Arial 16", bg="gray10", fg="white").pack(padx=20, pady=0)

        # Create image
        self.gameShot = ImageTk.PhotoImage(Image.open("Images/gameplay.png"))
        tk.Label(self.rulesWin, image=self.gameShot).pack(pady=20)

        # Create text
        tk.Label(self.rulesWin, text="Controls",
                 font="Arial 18 bold underline", bg="gray10", fg="white").pack(padx=20, pady=0)
        tk.Label(self.rulesWin, text="Move the crosshair around the screen using the mouse, using",
                 font="Arial 16", bg="gray10", fg="white").pack(padx=20, pady=(10, 0))
        tk.Label(self.rulesWin, text="the left mouse button to shoot and shake the mouse to reload.",
                 font="Arial 16", bg="gray10", fg="white").pack(padx=20, pady=0)

    


if __name__ == "__main__":
    homePage = tk.Tk()
    window = MainScreen(homePage)
    homePage.mainloop()
