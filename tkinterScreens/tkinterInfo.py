import tkinter as tk

root = tk.Tk()
root.geometry("600x400")
root.configure(bg="#B432B4")
font1 = ("Arial", 30, "bold")
label1 = tk.Label(root, text="What is MoveVision?",font=font1, bg="#B432B4")
label1.pack()
font2 = ("Arial", 12, "bold")
label2 = tk.Label(root, text="MoveVision is a fun game made with A.I., Tkinter, OpenCV, Pygame, Mediapipe,\n MongoDB and many other programming tools! The goal of the game is to\n make people move their bodies to live a healthier life in a fun and friendly\n way interactive! The game was developed by Kauã Moreira Batista!\n I'm glad to see you interested here in the game! To enjoy! CARPE DIEM!!!",font=font2, bg="#B432B4")
label2.pack()
root.mainloop()