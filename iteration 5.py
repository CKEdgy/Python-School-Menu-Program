import tkinter as tk
from tkinter import messagebox

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camp Menu Program")


        self.root.attributes("-fullscreen", True) 
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))#Set the window to full screen
 
    #Create the startup screen
        
        self.startup_frame = tk.Frame(root, bg="#b6e7fc") #background colour is used universally
        self.startup_frame.pack(fill="both", expand=True)


         # making a button for the startup screen - round
        
        self.canvas = tk.Canvas(self.startup_frame, width=400, height=150, bg="#b6e7fc", highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        self.rounded_rect = self.canvas.create_oval(10, 10, 390, 140, fill="#286393", outline="")
        self.text = self.canvas.create_text(200, 75, text="Start Ordering Now!", font=("Arial", 24), fill="white") #font should be changed in later iterations

        self.canvas.tag_bind(self.rounded_rect, "<Button-1>", lambda event: self.show_login_screen())#binding the click to the entire round canvas
        self.canvas.tag_bind(self.text, "<Button-1>", lambda event: self.show_login_screen())

        #Loading the BDSC Logo and adjusting position
        self.original_image = tk.PhotoImage(file="bdsclogo.png")
        width, height = 275, 275
        self.resized_image = self.original_image.subsample(self.original_image.width() // width, self.original_image.height() // height)

        image_label = tk.Label(self.startup_frame, image=self.resized_image, bg='#b6e7fc')
        image_label.place(relx=0.5, rely=0.38, anchor=tk.CENTER)

    # create the user login screen
        
        self.login_frame = tk.Frame(root, bg="#b6e7fc")
        self.login_frame.pack_propagate(0)
        self.login_frame.pack_forget()

        # Collect user information also for later display
        self.user_name = tk.StringVar()
        self.user_class = tk.StringVar()

        self.name_label = tk.Label(self.login_frame, text="Enter your name:", font=("Arial", 18), bg="#b6e7fc")
        self.name_label.pack(pady=20)
        self.name_entry = tk.Entry(self.login_frame, textvariable=self.user_name, font=("Arial", 18), width=30)
        self.name_entry.pack(pady=10)

        self.class_label = tk.Label(self.login_frame, text="Enter your class:", font=("Arial", 18), bg="#b6e7fc")
        self.class_label.pack(pady=20)
        self.class_entry = tk.Entry(self.login_frame, textvariable=self.user_class, font=("Arial", 18), width=30)
        self.class_entry.pack(pady=10)

        self.next_button = tk.Button(self.login_frame, text="Next", font=("Arial", 16), bg="#286393", fg="white", command=self.show_menu_screen)
        self.next_button.pack(pady=30)

        # create the main menu screen
        self.main_frame = tk.Frame(root, bg="#b6e7fc")
        self.main_frame.pack_propagate(0)
        self.main_frame.pack_forget()

        # Welcome message with the users name pulled from the collection
        
        self.welcome_label = tk.Label(self.main_frame, text="", font=("Arial", 30), bg="#b6e7fc")
        self.welcome_label.pack(pady=40)

        # Ask users for diet restrictions
        
        self.diet_label = tk.Label(self.main_frame, text="Select your diet restriction:", font=("Arial", 18), bg="#b6e7fc")
        self.diet_label.pack(pady=20)
        self.diet_var = tk.StringVar(value="None")

        self.vegan_radio = tk.Radiobutton(self.main_frame, text="Vegan", variable=self.diet_var, value="Vegan", font=("Arial", 16), bg="#b6e7fc", command=self.update_menu)
        self.vegan_radio.pack(pady=10)
        self.vegetarian_radio = tk.Radiobutton(self.main_frame, text="Vegetarian", variable=self.diet_var, value="Vegetarian", font=("Arial", 16), bg="#b6e7fc", command=self.update_menu)
        self.vegetarian_radio.pack(pady=10)
        self.none_radio = tk.Radiobutton(self.main_frame, text="None", variable=self.diet_var, value="None", font=("Arial", 16), bg="#b6e7fc", command=self.update_menu)
        self.none_radio.pack(pady=10)

        self.label = tk.Label(self.main_frame, text="Select a meal option:", font=("Arial", 18), bg="#b6e7fc")
        self.label.pack(pady=20)

    
        #create a Frame for the menu items and buttons
        
        self.menu_frame = tk.Frame(self.main_frame, bg="#b6e7fc")
        self.menu_frame.pack(pady=20)

        #Buttons for cart management
        self.cart = []

    # View Cart button in the top-right corner
        self.view_cart_button = tk.Button(self.main_frame, text="🛒", font=("Arial", 16), bg="#286393", fg="white", command=self.view_cart)
        self.view_cart_button.place(relx=0.9, rely=0.05, anchor=tk.NE)

         #Account button next to the View Cart button
        self.account_button = tk.Button(self.main_frame, text="👤", font=("Arial", 16), bg="#286393", fg="white", command=self.show_account)
        self.account_button.place(relx=0.85, rely=0.05, anchor=tk.NE)

        # Initialize all menu items with prices
        self.full_menu = [("Fried Rice", 8), ("Fish and Chips", 7), ("Cheese Burger", 6), ("Spaghetti Bolognese", 9)]
        self.vegan_menu = [("Vegan Salad", 6)]
        self.vegetarian_menu = [("Vegetarian Burger", 7)]

    def show_login_screen(self):
        self.startup_frame.pack_forget()  # Hide the startup screen
        self.login_frame.pack(fill="both", expand=True)  # Show the login screen

    def show_menu_screen(self):
        if not self.user_name.get() or not self.user_class.get():
            messagebox.showwarning("Input Error", "Please enter both your name and class.")
            return
        self.login_frame.pack_forget()  # Hide the login screen
        self.main_frame.pack(fill="both", expand=True)  # Show the main menu screen

        # Update the welcome message with the user's name in blue, all in the same label
        self.welcome_label.config(text=f"Haere mai, {self.user_name.get()}!", font=("Arial", 28, "bold"), fg="#286393", bg="#b6e7fc")
        
        self.update_menu()

    def update_menu(self):
        # Clear the current menu frame content
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        diet_restriction = self.diet_var.get()
        if diet_restriction == "Vegan":
            menu_items = self.vegan_menu
        elif diet_restriction == "Vegetarian":
            menu_items = self.vegetarian_menu
        else:
            menu_items = self.full_menu

        for item, price in menu_items:
            item_frame = tk.Frame(self.menu_frame, bg="#b6e7fc")
            item_frame.pack(fill="x", pady=5)

            # Item label
            item_label = tk.Label(item_frame, text=f"{item} - ${price}", font=("Arial", 16), bg="#b6e7fc")
            item_label.pack(side="left", padx=10)

        # button to add the item to the cart
            add_button = tk.Button(item_frame, text="+", font=("Arial", 16), bg="#286393", fg="white", command=lambda i=item, p=price: self.add_to_cart(i, p))
            add_button.pack(side="right", padx=10)

    def add_to_cart(self, item_name, item_price):
        self.cart.append((item_name, item_price))
        messagebox.showinfo("Cart", f"{item_name} added to cart")

    def view_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("View Cart")
        cart_window.attributes("-fullscreen", True)

        # Back button to return to the main menu
        back_button = tk.Button(cart_window, text="Back", font=("Arial", 18), command=cart_window.destroy)
        back_button.pack(anchor="nw", padx=20, pady=20)

        for item, price in self.cart:
            item_label = tk.Label(cart_window, text=f"{item} - ${price}", font=("Arial", 18))
            item_label.pack(pady=10)

        if not self.cart:
            empty_label = tk.Label(cart_window, text="Your cart is empty.", font=("Arial", 18))
            empty_label.pack(pady=20)

    def show_account(self):
        account_window = tk.Toplevel(self.root)
        account_window.title("Account")
        account_window.attributes("-fullscreen", True)

        back_button = tk.Button(account_window, text="Back", font=("Arial", 18), command=account_window.destroy)
        back_button.pack(anchor="nw", padx=20, pady=20)

     # Display user's name and class in the account window
        user_info = f"Name: {self.user_name.get()}\nClass: {self.user_class.get()}"
        user_label = tk.Label(account_window, text=user_info, font=("Arial", 18))
        user_label.pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()
