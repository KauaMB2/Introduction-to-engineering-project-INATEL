import tkinter as tk

root = tk.Tk()
root.geometry("600x150")
root.configure(bg="#B432B4")
font1 = ("Arial", 30, "bold")
label1 = tk.Label(root, text="ALERT!!!",font=font1, bg="red")
label1.pack()
font2 = ("Arial", 16, "bold")
label2 = tk.Label(root, text="Sorry! You cannot register null values in database.\nPlease, certify you entered the name and\nthe password to be registered!",font=font2, bg="#B432B4")
label2.pack()
root.mainloop()