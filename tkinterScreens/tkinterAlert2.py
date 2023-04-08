import tkinter as tk

root = tk.Tk()
root.geometry("600x100")
root.configure(bg="#B432B4")
font1 = ("Arial", 30, "bold")
label1 = tk.Label(root, text="ALERT!!!",font=font1, bg="red")
label1.pack()
font2 = ("Arial", 16, "bold")
label2 = tk.Label(root, text="Sorry! You have entered the wrong name or password.",font=font2, bg="#B432B4")
label2.pack()
root.mainloop()