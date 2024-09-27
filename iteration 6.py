import tkinter as tk
from tkinter import messagebox

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camp Menu Program")

             #set the window to full screen
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))


        self.bg_image = tk.PhotoImage(file="background_image.png")      #Load the background image

        self.bg_image = self.bg_image.subsample(3, 3)  # Reducing the size of the image

    #Create the startup screen with two sections (left and right)
        
        self.startup_frame = tk.Frame(root, bg="#b6e7fc")
        self.startup_frame.pack(fill="both", expand=True)

          #create a left frame for the background image
        
        self.left_frame = tk.Frame(self.startup_frame, bg="#b6e7fc")
        self.left_frame.place(relwidth=0.5, relheight=1, relx=0, rely=0)

        #Display the background image in the left frame
        
        self.bg_label = tk.Label(self.left_frame, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        #Create a right frame for the text and button
        self.right_frame = tk.Frame(self.startup_frame, bg="white")
        self.right_frame.place(relwidth=0.5, relheight=1, relx=0.5, rely=0)

    #add the Haere Mai message to the right side
        self.haere_mai_label = tk.Label(self.right_frame, text="Haere Mai.", font=("Arial", 60, "bold"), bg="white", fg="#286393")
        self.haere_mai_label.pack(pady=75)

         #Create entry fields for the user's name and class, placed below the Haere Mai message
        self.user_name = tk.StringVar()
        self.user_class = tk.StringVar()

        self.name_label = tk.Label(self.right_frame, text="👤 Enter your name:", font=("Arial", 18), bg="white", fg="#286393")
        self.name_label.pack(pady=10)

          #Validation function for name input
        vcmd = (root.register(self.validate_name), '%P')

        self.name_entry = tk.Entry(self.right_frame, textvariable=self.user_name, font=("Arial", 18), width=30, validate="key", validatecommand=vcmd)
        self.name_entry.pack(pady=10)

        self.class_label = tk.Label(self.right_frame, text="🎒 Enter your class:", font=("Arial", 18), bg="white", fg="#286393")
        self.class_label.pack(pady=10)
        self.class_entry = tk.Entry(self.right_frame, textvariable=self.user_class, font=("Arial", 18), width=30)
        self.class_entry.pack(pady=10)

        #Create the Start Ordering Now button in the right frame
        self.start_button = tk.Button(self.right_frame, text="Start Ordering Now!", font=("Arial", 24), bg="#286393", fg="white", command=self.show_menu_screen)
        self.start_button.pack(pady=75)

          # Load and display the BDSC Logo, adjust its position
        self.original_image = tk.PhotoImage(file="bdsclogo.png")
        width, height = 150, 150
        self.resized_image = self.original_image.subsample(self.original_image.width() // width, self.original_image.height() // height)

        image_label = tk.Label(self.right_frame, image=self.resized_image, bg='white')
        image_label.pack(pady=20)

        # Create the main menu screen
        self.main_frame = tk.Frame(root, bg="#b6e7fc")
        self.main_frame.pack_propagate(0)
        self.main_frame.pack_forget()

        #Welcome message with the user's name
        self.welcome_label_main = tk.Label(self.main_frame, text="", font=("Arial", 30), bg="#b6e7fc")
        self.welcome_label_main.pack(pady=40)

        

        #Ask users for diet restrictions
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

        #Create a Frame for the menu items and buttons
        self.menu_frame = tk.Frame(self.main_frame, bg="#b6e7fc")
        self.menu_frame.pack(pady=20)

          #Cart management
        self.cart = []

    #View Cart button in the top-right corner
        self.view_cart_button = tk.Button(self.main_frame, text="🛒", font=("Arial", 16), bg="#286393", fg="white", command=self.view_cart)
        self.view_cart_button.place(relx=0.9, rely=0.05, anchor=tk.NE)

        # Account button next to the View Cart button
        self.account_button = tk.Button(self.main_frame, text="👤", font=("Arial", 16), bg="#286393", fg="white", command=self.show_account)
        self.account_button.place(relx=0.85, rely=0.05, anchor=tk.NE)

        # Initialize all menu items with prices
        self.full_menu = [("Fried Rice", 8), ("Fish and Chips", 7), ("Cheese Burger", 6), ("Spaghetti Bolognese", 9)]
        self.vegan_menu = [("Vegan Salad", 6),("Vegan Choclate",3),("Sweet Potato", 7)]
        self.vegetarian_menu = [("Vegetarian Burger", 7),("Veggie Chilli", 6),("Veggie Burritos",7)]

    def validate_name(self, input_text):
        if input_text.isalpha() or input_text == "":
            return True
        else:
            messagebox.showerror("Invalid Input", "Please enter only letters for your name.")
            return False

    def show_menu_screen(self):
        if not self.user_name.get() or not self.user_class.get():
            messagebox.showwarning("Input Error", "Please enter both your name and class.")
            return
        self.startup_frame.pack_forget()  # Hide the startup screen
        self.main_frame.pack(fill="both", expand=True)  # Show the main menu screen
        

        # Update the welcome message with the user's name
        self.welcome_label_main.config(text=f"Haere mai, {self.user_name.get()}!", font=("Arial", 28, "bold"), fg="#286393", bg="#b6e7fc")
        
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

            # Button to add the item to the cart
            add_button = tk.Button(item_frame, text="+", font=("Arial", 16), bg="#286393", fg="white", command=lambda i=item, p=price: self.add_to_cart(i, p))
            add_button.pack(side="right", padx=10)

    def add_to_cart(self, item, price):
        #check if the cart already has 3 items
        if len(self.cart) >= 3:
            #show a warning message if the cart exceeds the limit of 3 items
            messagebox.showwarning("Cart Limit", "You can only add 3 items to the cart.")
        else:
            # Add the item to the cart if it's within the limit
            self.cart.append((item, price))
            messagebox.showinfo("Cart", f"{item} added to cart!")


    def view_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("View Cart")
        cart_window.attributes("-fullscreen", True)

        # Back button to return to the main menu
        back_button = tk.Button(cart_window, text="Back", font=("Arial", 18), command=cart_window.destroy)
        back_button.pack(anchor="nw", padx=20, pady=20)

        # Display cart items with "x" buttons
        index = 0
        for item, price in self.cart:
            item_frame = tk.Frame(cart_window)
            item_frame.pack(pady=10)

            item_label = tk.Label(item_frame, text=f"{item} - ${price}", font=("Arial", 18))
            item_label.pack(side="left", padx=10)

            # Add the "x" button for removing the item from the cart
            remove_button = tk.Button(item_frame, text="x", font=("Arial", 18), bg="#286393",fg="white",
                                      command=lambda i=index: self.remove_from_cart(i, cart_window))
            remove_button.pack(side="right", padx=10)

            index += 1

        if not self.cart:
            empty_label = tk.Label(cart_window, text="Your cart is empty.", font=("Arial", 18))
            empty_label.pack(pady=10)

        # Calculate Total and Order buttons at the bottom
        total_button = tk.Button(cart_window, text="Calculate Total", font=("Arial", 18), bg="#286393", fg="white", command=self.calculate_total)
        total_button.pack(pady=20)

        order_button = tk.Button(cart_window, text="Order", font=("Arial", 18), bg="#286393", fg="white", command=self.order)
        order_button.pack(pady=20)

    def remove_from_cart(self, index, cart_window):
        del self.cart[index]  #remove the item at the given index
        cart_window.destroy()    #Close and reopen the cart window to refresh it
        self.view_cart()  #reopen the updated cart window

    def calculate_total(self):
        total = sum(price for item, price in self.cart)
        messagebox.showinfo("Total", f"Your total is: ${total}")

    def order(self):
        if not self.cart:
            messagebox.showwarning("Order Error", "Your cart is empty. Please add items to your cart before ordering.")
            return
        messagebox.showinfo("Order", "Your order has been placed successfully!")

        total = sum(price for item, price in self.cart)
        order_details = f"Name: {self.user_name.get()}\nClass: {self.user_class.get()}\nOrder: {self.cart}\nTotal: ${total:.2f}\n"
                
                #save the order details to an external file
        with open("orders.txt", "a") as file:
                    file.write(order_details + "\n")

    def show_account(self):
        account_window = tk.Toplevel(self.root)
        account_window.title("Account Information")
        account_window.geometry("400x400")

        account_label = tk.Label(account_window, text=f"Name: {self.user_name.get()}\nClass: {self.user_class.get()}", font=("Arial", 18))
        account_label.pack(pady=20)

        close_button = tk.Button(account_window, text="Close", command=account_window.destroy)
        close_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()
