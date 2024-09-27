import tkinter as tk
from tkinter import messagebox

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camp Menu Program")


        self.root.attributes("-fullscreen", True) #set the window to full screen
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))

    #create the startup screen
        
        self.startup_frame = tk.Frame(root, bg="#b6e7fc")  #background colour used universally
        self.startup_frame.pack(fill="both", expand=True)
        
        #creating shape used for button
        
        self.canvas = tk.Canvas(self.startup_frame, width=400, height=150, bg="#b6e7fc", highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.65, anchor=tk.CENTER) #Centering the shape allowing for centered button canvas

        self.rounded_rect = self.canvas.create_oval(10, 10, 390, 140, fill="#286393", outline="")
        self.text = self.canvas.create_text(200, 75, text="Start Ordering Now!", font=("Arial", 24), fill="white") #font should be changed in future iteration

        #Binding the click to the whole shape
        self.canvas.tag_bind(self.rounded_rect, "<Button-1>", lambda event: self.show_menu_screen())
        self.canvas.tag_bind(self.text, "<Button-1>", lambda event: self.show_menu_screen())

    # create the main menu screen
        
        self.main_frame = tk.Frame(root, bg="#b6e7fc")
        self.main_frame.pack_propagate(0)  
        self.main_frame.pack_forget()  # Hide the main frame initially, display it later in the program.
        

         #initialize all menu items with prices
        
        self.full_menu = [("Gluten-Free Pizza", 8), ("Vegetarian Burger", 7), ("Vegan Salad", 6)]
        self.vegan_menu = [("Vegan Salad", 6)]
        self.vegetarian_menu = [("Vegetarian Burger", 7)]

          # Collect user information, will be used later in the program
        self.user_name = tk.StringVar()
        self.user_class = tk.StringVar()

        # Center and enlarge elements and widgets
        
        self.name_label = tk.Label(self.main_frame, text="Enter your name:", font=("Arial", 18), bg="#b6e7fc") # Font should be changed in later it
        self.name_label.pack(pady=20)
        self.name_entry = tk.Entry(self.main_frame, textvariable=self.user_name, font=("Arial", 18), width=30)
        self.name_entry.pack(pady=10)

        self.class_label = tk.Label(self.main_frame, text="Enter your class:", font=("Arial", 18), bg="#b6e7fc")
        self.class_label.pack(pady=20)
        self.class_entry = tk.Entry(self.main_frame, textvariable=self.user_class, font=("Arial", 18), width=30)
        self.class_entry.pack(pady=10)

        # Ask for diet restrictions
        
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
        self.listbox = tk.Listbox(self.main_frame, font=("Arial", 16), height=6, width=40)
        self.listbox.pack(pady=20)

    #Buttons for cart management
        self.cart = []
        self.cart_button = tk.Button(self.main_frame, text="Add to Cart", font=("Arial", 16), bg="#286393", fg="white", command=self.add_to_cart)
        self.cart_button.pack(pady=10)
        self.view_cart_button = tk.Button(self.main_frame, text="View Cart", font=("Arial", 16), bg="#286393", fg="white", command=self.view_cart)
        self.view_cart_button.pack(pady=10)

        # Load the image and adjust its size
        self.original_image = tk.PhotoImage(file="bdsclogo.png")
        width, height = 275, 275
        self.resized_image = self.original_image.subsample(self.original_image.width() // width, self.original_image.height() // height)
        
        image_label = tk.Label(self.startup_frame, image=self.resized_image, bg='#b6e7fc')
        image_label.place(relx=0.5, rely=0.38, anchor=tk.CENTER)  # Center the image on the startup screen

    def show_menu_screen(self):
        self.startup_frame.pack_forget()  # Hide the startup screen
        self.main_frame.pack(fill="both", expand=True)  # Show the main menu screen
        self.update_menu()

    def update_menu(self):
        self.listbox.delete(0, tk.END)
        diet_restriction = self.diet_var.get()
        if diet_restriction == "Vegan":
            menu_items = self.vegan_menu
        elif diet_restriction == "Vegetarian":
            menu_items = self.vegetarian_menu
        else:
            menu_items = self.full_menu
        
        for item, price in menu_items:
            self.listbox.insert(tk.END, f"{item} - ${price}")

    def add_to_cart(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select an item to add to the cart.")
            return
        
        selected_item = self.listbox.get(selected_index)
        item_name, item_price = selected_item.split(" - $")
        self.cart.append((item_name, float(item_price)))
        messagebox.showinfo("Cart", f"{item_name} added to cart")

    def view_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("View Cart")
        cart_window.attributes("-fullscreen", True)

        # Back button to return to the main menu
        back_button = tk.Button(cart_window, text="Back", font=("Arial", 18), command=cart_window.destroy)
        back_button.pack(anchor="nw", padx=20, pady=20)

        index = 0
        for item, price in self.cart:
            item_label = tk.Label(cart_window, text=f"{item} - ${price}", font=("Arial", 18))
            item_label.pack(pady=10)

            index += 1

        if not self.cart:
            empty_label = tk.Label(cart_window, text="Your cart is empty.", font=("Arial", 18))
            empty_label.pack(pady=10)

        #calculate Total and Order buttons at the bottom

            
        total_button = tk.Button(cart_window, text="Calculate Total", font=("Arial", 18), bg="#286393", fg="white", command=self.calculate_total)
        total_button.pack(pady=20)

        order_button = tk.Button(cart_window, text="Order", font=("Arial", 18), bg="#286393", fg="white", command=self.order)
        order_button.pack(pady=20)

    def calculate_total(self):
        total = sum(price for item, price in self.cart)
        messagebox.showinfo("Total", f"Total amount: ${total:.2f}")

    def order(self):
        if not self.user_name.get() or not self.user_class.get():
            messagebox.showwarning("Input Error", "Please enter both your name and class.")
            return

        total = sum(price for item, price in self.cart)
        order_details = f"Name: {self.user_name.get()}\nClass: {self.user_class.get()}\nOrder: {self.cart}\nTotal: ${total:.2f}\n"
        
        with open("orders.txt", "a") as file:
            file.write(order_details + "\n")
        
        messagebox.showinfo("Order", "Your order has been placed successfully!")

root = tk.Tk()
app = MenuApp(root)
root.mainloop()
