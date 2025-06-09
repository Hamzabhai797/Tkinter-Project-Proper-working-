import tkinter as tk
from tkinter import messagebox
import cv2
import PIL.Image, PIL.ImageTk
import threading

users_db = {}

# === Load background video ===
def load_background_video():
    try:
        cap = cv2.VideoCapture("airo.mp4")
        return cap
    except FileNotFoundError:
        messagebox.showerror("Error", "Background video 'background_video.mp4' not found.")
        root.destroy()
        exit()

# === Update video background frame ===
def update_video_background():
    ret, frame = cap.read()
    if ret:
        # Convert the frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to Image
        img = PIL.Image.fromarray(frame)

        # Resize image to fit the window
        img = img.resize((1200, 850), PIL.Image.LANCZOS)

        # Convert to PhotoImage
        bg_img = PIL.ImageTk.PhotoImage(img)

        # Update the background label
        bg_label.config(image=bg_img)
        bg_label.image = bg_img

    # Continuously update the frame
    bg_label.after(20, update_video_background)

# === Initialize App ===
root = tk.Tk()
root.title("Airport Management System")
root.geometry("1000x650")
root.resizable(False, False)

cap = load_background_video()

def set_background():
    global bg_label
    bg_label = tk.Label(root)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    update_video_background()

def set_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg="gray")

    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, text)
            entry.config(fg="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

def show_home():
    clear_frame()
    set_background()
    tk.Label(root, text="Airport Management System", font=("Arial", 16, "bold"), bg="white").place(x=350, y=40)
    tk.Button(root, text="Register", command=show_register, width=20, bg="navy", fg="white").place(x=420, y=85)
    tk.Button(root, text="Login", command=show_login, width=20, bg="green", fg="white").place(x=420, y=120)

def show_register():
    clear_frame()
    set_background()
    tk.Label(root, text="Registration", font=("Arial", 16, "bold"), bg="white").place(x=300, y=20)

    fields = ["Full Name", "User Name", "Email", "Password"]
    variables = {}
    y = 80
    for field in fields:
        tk.Label(root, text=field + ":", font=("Arial", 10, "bold"), bg="white").place(x=180, y=y)
        ent = tk.Entry(root, width=30, show="*" if field == "Password" else "")
        ent.place(x=300, y=y)
        set_placeholder(ent, f"Enter your {field.lower()}")
        variables[field] = ent
        y += 40

    def register():
        name = variables["Full Name"].get()
        email = variables["Email"].get()
        password = variables["Password"].get()
        username = variables["User Name"].get()

        if any(x.startswith("Enter") or not x.strip() for x in [name, email, password, username]):
            messagebox.showerror("Error", "Please fill in all fields correctly.")
            return

        if email in users_db:
            messagebox.showwarning("Warning", "User already registered. Please login.")
        else:
            users_db[email] = {"name": name, "username": username, "password": password}
            messagebox.showinfo("Success", "Registration complete.")
            show_login()

    tk.Button(root, text="Submit", command=register, bg="black", fg="white", width=20).place(x=260, y=250)
    tk.Button(root, text="Back", command=show_home, bg="gray", fg="white", width=10).place(x=10, y=10)

def show_login():
    clear_frame()
    set_background()
    tk.Label(root, text="Login", font=("Arial", 16, "bold"), bg="white").place(x=300, y=30)

    tk.Label(root, text="Email:", font=("Arial", 10), bg="white").place(x=200, y=100)
    email_entry = tk.Entry(root, width=30)
    email_entry.place(x=300, y=100)
    set_placeholder(email_entry, "Enter your email")

    tk.Label(root, text="Password:", font=("Arial", 10), bg="white").place(x=200, y=140)
    pass_entry = tk.Entry(root, width=30, show="*")
    pass_entry.place(x=300, y=140)
    set_placeholder(pass_entry, "Enter your password")

    def login():
        email = email_entry.get()
        password = pass_entry.get()

        if email in users_db and users_db[email]["password"] == password:
            messagebox.showinfo("Welcome", f"Welcome {users_db[email]['name']}")
            show_flight_form()
        else:
            messagebox.showerror("Error", "User not found or incorrect password.")

    tk.Button(root, text="Login", command=login, bg="green", fg="white", width=20).place(x=270, y=200)
    tk.Button(root, text="Back", command=show_home, bg="gray", fg="white", width=10).place(x=10, y=10)

def show_flight_form():
    clear_frame()
    set_background()
    tk.Label(root, text="Flight Form", font=("Arial", 16, "bold"), bg="white").place(x=280, y=20)

    fields = ["Name", "Passport Number", "City OR Country (From)", "City OR Country (To)", "Flight Number"]
    variables = {}
    y = 80
    for field in fields:
        tk.Label(root, text=field + ":", font=("Arial", 10), bg="white").place(x=180, y=y)
        ent = tk.Entry(root, width=30)
        ent.place(x=320, y=y)
        set_placeholder(ent, f"Enter your {field.lower()}")
        variables[field] = ent
        y += 40

    def submit_flight():
        details = {k: v.get() for k, v in variables.items()}
        if any(x.startswith("Enter") or not x.strip() for x in details.values()):
            messagebox.showerror("Error", "All fields must be filled!")
            return
        show_flight_result(details)

    tk.Button(root, text="Submit", command=submit_flight, bg="blue", fg="white", width=20).place(x=260, y=280)
    tk.Button(root, text="Logout", command=show_home, bg="red", fg="white", width=10).place(x=10, y=10)

def show_flight_result(data):
    clear_frame()
    set_background()
    tk.Label(root, text="Your Flight Details", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    summary = f"""
Name: {data['Name']}
Passport: {data['Passport Number']}
Route: {data['City OR Country (From)']} ➜ {data['City OR Country (To)']}
Flight No: {data['Flight Number']}

🛫 Flight from {data['City OR Country (From)']} to {data['City OR Country (To)']} is scheduled to depart in 30 minutes.
🛬 Estimated arrival: In 2 hours.
    """
    tk.Label(root, text=summary.strip(), justify="left", font=("Arial", 11), bg="white").pack(pady=20)
    tk.Button(root, text="Back to Home", command=show_home, bg="gray", fg="white", width=20).pack(pady=10)

# === Start the App ===
show_home()
root.mainloop()

