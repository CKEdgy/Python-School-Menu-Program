import tkinter as tk
from tkinter import messagebox

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camp Menu Program")

         #initialize all menu items with prices
        self.full_menu = [("Gluten-Free Pizza", 8), ("Vegetarian Burger", 7), ("Vegan Salad", 6)]
        self.vegan_menu = [("Vegan Salad", 6)]
        self.vegetarian_menu = [("Vegetarian Burger", 7)]

        #collect user information
        self.user_name = tk.StringVar()
        self.user_class = tk.StringVar()
        self.name_label = tk.Label(root, text="Enter your name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root, textvariable=self.user_name)
        self.name_entry.pack()
        self.class_label = tk.Label(root, text="Enter your class:")
        self.class_label.pack()
        self.class_entry = tk.Entry(root, textvariable=self.user_class)
        self.class_entry.pack()
        
    #ask for diet restrictions
        self.diet_label = tk.Label(root, text="Select your diet restriction:")
        self.diet_label.pack()
        self.diet_var = tk.StringVar(value="None")
        self.vegan_radio = tk.Radiobutton(root, text="Vegan", variable=self.diet_var, value="Vegan", command=self.update_menu)
        self.vegan_radio.pack()
        self.vegetarian_radio = tk.Radiobutton(root, text="Vegetarian", variable=self.diet_var, value="Vegetarian", command=self.update_menu)
        self.vegetarian_radio.pack()
        self.none_radio = tk.Radiobutton(root, text="None", variable=self.diet_var, value="None", command=self.update_menu)
        self.none_radio.pack()

        self.label = tk.Label(root, text="Select a meal option:")
        self.label.pack()
        self.listbox = tk.Listbox(root)
        self.listbox.pack()

          #Buttons for cart management
        self.cart = []
        self.cart_button = tk.Button(root, text="Add to Cart", command=self.add_to_cart)
        self.cart_button.pack()
        self.view_cart_button = tk.Button(root, text="View Cart", command=self.view_cart)
        self.view_cart_button.pack()
        self.total_button = tk.Button(root, text="Calculate Total", command=self.calculate_total)
        self.total_button.pack()
        self.order_button = tk.Button(root, text="Order", command=self.order)
        self.order_button.pack()

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
        selected_item = self.listbox.get(tk.ACTIVE)
        item_name, item_price = selected_item.split(" - $")
        self.cart.append((item_name, float(item_price)))
        messagebox.showinfo("Cart", f"{item_name} added to cart")

    def remove_item(self, index, window):
        self.cart.pop(index)  # remove the item at the specified index
        window.destroy()  # close the current view cart window
        self.view_cart()  #Reopen it to reflect the changes

    def view_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("View Cart")

        #manual index tracking
        index = 0
        for item, price in self.cart:
            item_label = tk.Label(cart_window, text=f"{item} - ${price}")
            item_label.grid(row=index, column=0, padx=10, pady=5)
            
            remove_button = tk.Button(cart_window, text="X", command=lambda idx=index: self.remove_item(idx, cart_window))
            remove_button.grid(row=index, column=1, padx=10, pady=5)

            index += 1  # Increment the index manually

        if not self.cart:
            empty_label = tk.Label(cart_window, text="Your cart is empty.")
            empty_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

    def calculate_total(self):
        total = sum(price for item, price in self.cart)
        messagebox.showinfo("Total", f"Total amount: ${total:.2f}")

    def order(self):
        # Check if the user name and class are provided
        if not self.user_name.get() or not self.user_class.get():
            messagebox.showwarning("Input Error", "Please enter both your name and class.")
            return

        total = sum(price for item, price in self.cart)
        order_details = f"Name: {self.user_name.get()}\nClass: {self.user_class.get()}\nOrder: {self.cart}\nTotal: ${total:.2f}\n"
        
        # Save the order details to an external file
        with open("orders.txt", "a") as file:
            file.write(order_details + "\n")
        
        messagebox.showinfo("Order", "Your order has been placed successfully!")

root = tk.Tk()
app = MenuApp(root)
root.mainloop()
