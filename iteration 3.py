import tkinter as tk
from tkinter import messagebox

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camp Menu Program")

          #Set the window to full screen
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))

     #Create the startup screen
        self.startup_frame = tk.Frame(root, bg="#b6e7fc")
        self.startup_frame.pack(fill="both", expand=True)
    

        

         #create a Canvas for the rounded button
        self.canvas = tk.Canvas(self.startup_frame, width=400, height=150, bg="#b6e7fc", highlightthickness=0)

        self.canvas.place(relx=0.5, rely=0.65, anchor=tk.CENTER)  #Place the image in the center of the frame


    #creating an oval
        self.rounded_rect = self.canvas.create_oval(10, 10, 390, 140, fill="#286393", outline="")
        self.text = self.canvas.create_text(200, 75, text="Start Ordering Now!", font=("Arial", 24), fill="white")

        #bind the click event to the entire canvas 
        self.canvas.tag_bind(self.rounded_rect, "<Button-1>", lambda event: self.show_menu_screen())
        self.canvas.tag_bind(self.text, "<Button-1>", lambda event: self.show_menu_screen())

        #create the main menu screen but don't display it yet
        self.main_frame = tk.Frame(root, bg="#b6e7fc")

        # initialize all menu items with prices
        self.full_menu = [("Gluten-Free Pizza", 8), ("Vegetarian Burger", 7), ("Vegan Salad", 6)]
        self.vegan_menu = [("Vegan Salad", 6)]
        self.vegetarian_menu = [("Vegetarian Burger", 7)]

    # Collect user information
        self.user_name = tk.StringVar()
        self.user_class = tk.StringVar()
        
        # Add space from the top
        self.main_frame.pack_propagate(0)
        self.main_frame.pack_forget()  # Hide the main frame initially

        self.name_label = tk.Label(self.main_frame, text="Enter your name:", bg="#b6e7fc")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.main_frame, textvariable=self.user_name , bg="#b6e7fc")
        self.name_entry.pack(pady=5)
        self.class_label = tk.Label(self.main_frame, text="Enter your class:", bg="#b6e7fc")
        self.class_label.pack(pady=5)
        self.class_entry = tk.Entry(self.main_frame, textvariable=self.user_class , bg="#b6e7fc")
        self.class_entry.pack(pady=5)
        
        # Ask for diet restrictions
        self.diet_label = tk.Label(self.main_frame, text="Select your diet restriction:" , bg="#b6e7fc")
        self.diet_label.pack(pady=5)
        self.diet_var = tk.StringVar(value="None")
        self.vegan_radio = tk.Radiobutton(self.main_frame, text="Vegan", variable=self.diet_var, value="Vegan", bg="#b6e7fc", command=self.update_menu)
        self.vegan_radio.pack(pady=5)
        self.vegetarian_radio = tk.Radiobutton(self.main_frame, text="Vegetarian", variable=self.diet_var, value="Vegetarian", bg="#b6e7fc", command=self.update_menu)
        self.vegetarian_radio.pack(pady=5)
        self.none_radio = tk.Radiobutton(self.main_frame, text="None", variable=self.diet_var, value="None", bg="#b6e7fc", command=self.update_menu)
        self.none_radio.pack(pady=5)

        self.label = tk.Label(self.main_frame, text="Select a meal option:", bg="#b6e7fc")
        self.label.pack(pady=5)
        self.listbox = tk.Listbox(self.main_frame)
        self.listbox.pack(pady=5)

        #Buttons for cart management
        self.cart = []
        self.cart_button = tk.Button(self.main_frame, text="Add to Cart", bg="#b6e7fc", command=self.add_to_cart)
        self.cart_button.pack(pady=5)
        self.view_cart_button = tk.Button(self.main_frame, text="View Cart", bg="#b6e7fc", command=self.view_cart)
        self.view_cart_button.pack(pady=5)
        self.total_button = tk.Button(self.main_frame, text="Calculate Total", bg="#b6e7fc", command=self.calculate_total)
        self.total_button.pack(pady=5)
        self.order_button = tk.Button(self.main_frame, text="Order", bg="#b6e7fc", command=self.order)
        self.order_button.pack(pady=5)

        # Load the image
        self.original_image = tk.PhotoImage(file="bdsclogo.png")

        # Resize the image
        width = 275
        height = 275
        self.resized_image = self.original_image.subsample(self.original_image.width() // width, self.original_image.height() // height)

        # Create a label to display the image
        image_label = tk.Label(self.startup_frame, image=self.resized_image, bg='#b6e7fc')
        image_label.place(relx=0.5, rely=0.38, anchor=tk.CENTER)  # Place the image in the center of the frame

    def show_menu_screen(self):
        self.startup_frame.pack_forget()  # Hide the startup screen
        self.main_frame.pack(fill="both", expand=True)  #Show the main menu screen
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

    def remove_item(self, index, window):
        self.cart.pop(index)  # Remove the item at the specified index
        window.destroy()  # Close the current view cart window
        self.view_cart()  # Reopen it to reflect the changes

    def view_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("View Cart")

    # Manual index tracking
        index = 0
        for item, price in self.cart:
            item_label = tk.Label(cart_window, text=f"{item} - ${price}")
            item_label.grid(row=index, column=0, padx=10, pady=5)
            
            remove_button = tk.Button(cart_window, text="X", command=lambda idx=index: self.remove_item(idx, cart_window))
            remove_button.grid(row=index, column=1, padx=10, pady=5)

            index += 1  #Increment the index manually

        if not self.cart:
            empty_label = tk.Label(cart_window, text="Your cart is empty.")
            empty_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

    def calculate_total(self):
        total = sum(price for item, price in self.cart)
        messagebox.showinfo("Total", f"Total amount: ${total:.2f}")

    def order(self):
    #check if the user name and class are provided
        if not self.user_name.get() or not self.user_class.get():
            messagebox.showwarning("Input Error", "Please enter both your name and class.")
            return

        total = sum(price for item, price in self.cart)
        order_details = f"Name: {self.user_name.get()}\nClass: {self.user_class.get()}\nOrder: {self.cart}\nTotal: ${total:.2f}\n"
        
        #Save the order details to an external file
        with open("orders.txt", "a") as file:
            file.write(order_details + "\n")
        
        messagebox.showinfo("Order", "Your order has been placed successfully!")

root = tk.Tk()
app = MenuApp(root)
root.mainloop()
