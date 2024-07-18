from pathlib import Path
from tkinter import Tk, Canvas, Button, StringVar, IntVar, Spinbox, Label

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\HP\Downloads\FivemProjects\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class ProductCalculator:
    def __init__(self, root):
        self.root = root
        self.root.geometry("740x432")
        self.root.configure(bg="#D3D1C8")
        self.root.resizable(False, False)

        # Define the products and their prices
        self.products = {
            "Skunk": 5,
            "Amnesia": 10,
            "White Widow": 20,
            "Blue Dream": 35,
            "Girl Scout Cookie": 45,
        }

        # Define the real values for the products
        self.real_values = {
            "Skunk": 15,
            "Amnesia": 23,
            "White Widow": 33,
            "Blue Dream": 55,
            "Girl Scout Cookie": 60,
        }

        self.canvas = Canvas(
            root,
            bg="#D3D1C8",
            height=432,
            width=740,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Define common width for dropdowns and calculate x position
        dropdown_width = 674.0
        dropdown_x = (740 - dropdown_width) / 2  # Centered x position

        # Sell value button
        self.sell_value_button = Button(
            root,
            text="$0.00",
            command=self.calculate_sell_value,
            bg="#33A259",
            fg="#FFFFFF",
            font=("Roboto", 16, "bold"),
            relief="flat"
        )
        self.sell_value_button.place(
            x=36.0,
            y=322.0,
            width=300.0,  # Original width
            height=64.0
        )

        # Street value button
        self.street_value_button = Button(
            root,
            text="$0.00",
            command=self.calculate_street_value,
            bg="#D65353",
            fg="#FFFFFF",
            font=("Roboto", 16, "bold"),
            relief="flat"
        )
        self.street_value_button.place(
            x=410.0,
            y=322.0,
            width=300.0,  # Original width
            height=64.0
        )

        # Title text
        self.canvas.create_text(
            15.0,
            16.0,
            anchor="nw",
            text="TREY WAREHOUSE CALCULATOR",
            fill="#FFFFFF",
            font=("Roboto", 16, "bold")
        )

        # Variables for product and quantity
        self.product_var = StringVar()
        self.quantity_var = IntVar()

        # Product button
        self.product_button = Button(
            root,
            text="Select Product",
            command=self.toggle_product_spinbox,
            bg="#BEC0A8",
            fg="#FFFFFF",
            font=("Roboto", 16, "bold"),
            relief="flat"
        )
        self.product_button.place(
            x=dropdown_x,
            y=85.0,
            width=dropdown_width,
            height=64.0
        )

        # Quantity button
        self.quantity_button = Button(
            root,
            text="Select Quantity",
            command=self.toggle_quantity_spinbox,
            bg="#BEC0A8",
            fg="#FFFFFF",
            font=("Roboto", 16, "bold"),
            relief="flat"
        )
        self.quantity_button.place(
            x=dropdown_x,
            y=196.0,
            width=dropdown_width,
            height=64.0
        )

        # Product Spinbox
        self.spinbox_product = Spinbox(
            root,
            values=list(self.products.keys()),
            textvariable=self.product_var,
            font=("Roboto", 14, "bold"),
            state="readonly",
            width=24  # Adjust based on desired width
        )
        self.spinbox_product.place(
            x=dropdown_x,
            y=150.0,
            width=dropdown_width,
            height=25.0
        )
        self.spinbox_product.place_forget()  # Initially hidden

        # Quantity Spinbox
        self.spinbox_quantity = Spinbox(
            root,
            values=[50, 100, 250, 500, 1000, 2000, 5000, 10000],
            textvariable=self.quantity_var,
            font=("Roboto", 14, "bold"),
            state="readonly",
            width=24  # Adjust based on desired width
        )
        self.spinbox_quantity.place(
            x=dropdown_x,
            y=261.0,
            width=dropdown_width,
            height=25.0
        )
        self.spinbox_quantity.place_forget()  # Initially hidden

        # Add labels below the buttons
        self.sell_value_label = Label(
            root,
            text="SELL VALUE",
            bg="#D3D1C8",
            fg="#33A259",
            font=("Roboto", 16, "bold")
        )
        self.sell_value_label.place(
            x=36.0,
            y=392.0
        )

        self.street_value_label = Label(
            root,
            text="STREET VALUE",
            bg="#D3D1C8",
            fg="#D65353",
            font=("Roboto", 16, "bold")
        )
        self.street_value_label.place(
            x=410.0,
            y=392.0
        )

    def toggle_product_spinbox(self):
        if self.spinbox_product.winfo_ismapped():
            self.spinbox_product.place_forget()
        else:
            self.spinbox_product.place(
                x=(740 - 674.0) / 2,  # Centered x position
                y=150.0,
                width=674.0
            )
            self.update_product_selection(self.product_var.get())

    def toggle_quantity_spinbox(self):
        if self.spinbox_quantity.winfo_ismapped():
            self.spinbox_quantity.place_forget()
        else:
            self.spinbox_quantity.place(
                x=(740 - 674.0) / 2,  # Centered x position
                y=261.0,
                width=674.0
            )
            self.update_quantity_selection(self.quantity_var.get())

    def update_product_selection(self, value):
        selected_product = value
        self.product_var.set(selected_product)
        self.calculate_sell_value()  # Recalculate values whenever a new product is selected

    def update_quantity_selection(self, value):
        selected_quantity = int(value)
        self.quantity_var.set(selected_quantity)
        self.calculate_sell_value()  # Recalculate values whenever a new quantity is selected

    def calculate_sell_value(self):
        product = self.product_var.get()
        quantity = self.quantity_var.get()

        if product not in self.products or quantity not in [50, 100, 250, 500, 1000, 2000, 5000, 10000]:
            self.sell_value_button.config(text="$0.00")
            return

        price = self.products[product]
        total_value = quantity * price
        readable_total_value = self.format_value(total_value)

        self.sell_value_button.config(text=f"${readable_total_value}")

    def calculate_street_value(self):
        product = self.product_var.get()
        quantity = self.quantity_var.get()

        if product not in self.real_values or quantity not in [50, 100, 250, 500, 1000, 2000, 5000, 10000]:
            self.street_value_button.config(text="$0.00")
            return

        real_value = self.real_values[product]
        total_real_value = quantity * real_value
        readable_total_real_value = self.format_value(total_real_value)

        self.street_value_button.config(text=f"${readable_total_real_value}")

    def format_value(self, value):
        if value >= 1_000_000:
            return f"{value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"{value/1_000:.1f}k"
        else:
            return f"{value:.2f}"

if __name__ == "__main__":
    window = Tk()
    app = ProductCalculator(window)
    window.mainloop()
