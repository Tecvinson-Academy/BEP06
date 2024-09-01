import tkinter as tk
from tkinter import messagebox, simpledialog
#import uuid
import random
from datetime import datetime, timedelta

class Company:
    def __init__(self, name, delivery_cost_per_km):
        self.company_id = "{:06d}".format(random.randint(0, 999999))
        self.name = name
        self.delivery_cost_per_km = delivery_cost_per_km
        self.subscription_end_date = datetime.now() + timedelta(days=365)
        self.profit = 0.0

    def subscribe(self):
        self.subscription_end_date = datetime.now() + timedelta(days=365)

    def is_subscription_active(self):
        return datetime.now() < self.subscription_end_date

    def add_profit(self, amount):
        self.profit += amount

class Waybill:
    def __init__(self, sender, sender_location, receiver, receiver_location, items, weight, is_fragile):
        self.waybill_id = "{:06d}".format(random.randint(0, 999999))
        self.sender = sender
        self.sender_location = sender_location
        self.receiver = receiver
        self.receiver_location = receiver_location
        self.items = items
        self.weight = weight
        self.is_fragile = is_fragile
        self.tracking_data = []
        self.associated_company = None
        self.estimated_cost = 0.0

    def associate_company(self, company):
        self.associated_company = company
        self.estimated_cost = self.calculate_delivery_cost(company.delivery_cost_per_km)
        company.add_profit(self.estimated_cost)

    def calculate_delivery_cost(self, cost_per_km):
        distance = 100  # in kilometers
        return cost_per_km * distance

    def add_tracking(self, location):
        self.tracking_data.append(location)

    def display_tracking(self):
        tracking_info = "\n".join(self.tracking_data)
        messagebox.showinfo("Tracking Data", f"Tracking Data for Waybill ID {self.waybill_id}:\n{tracking_info}")

    def display_receipt(self):
        receipt = (
            f"Waybill ID: {self.waybill_id}\n"
            f"Sender: {self.sender}\n"
            f"Sender Location: {self.sender_location}\n"
            f"Receiver: {self.receiver}\n"
            f"Receiver Location: {self.receiver_location}\n"
            f"Items: {self.items}\n"
            f"Weight: {self.weight} kg\n"
            f"Fragile: {'Yes' if self.is_fragile else 'No'}\n"
            f"Estimated Cost: ${self.estimated_cost:.2f}\n"
        )
        messagebox.showinfo("Receipt", receipt)

class LogisticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logistics Management Interface")
        self.companies = []
        self.waybills = []
        self.current_company = None
        self.welcome_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def welcome_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to Waybill 365").pack()
            
        write_up = (
                "This application allows logistics companies to manage waybills, invoices and subscriptions.\n "
                "As a registered company, you can subscribe to our service for $10,000 per year,  "
                "allowing you to access our features. \nYou can generate waybills, track shipments "
                "and manage your company's logistics all in one place.\n\n"
                "For users, the interface provides tools to create waybills, add tracking data, "
                "and generate PDFs for waybills\n. Companies can also view their invoices and waybills, "
                "ensuring that all transactions are transparent and well-documented.\n\n"
                "Please choose an option below to get started."
        )
        tk.Label(self.root, text=write_up).pack()
        tk.Button(self.root, text="Company Menu", command=self.company_menu).pack()
        tk.Button(self.root, text="User Menu", command=self.User_menu).pack()
       

    def company_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Company Menu").pack()
        tk.Button(self.root, text="Subscribe", command=self.register_company).pack()
        tk.Button(self.root, text="View Invoices", command=self.view_invoices).pack()
        tk.Button(self.root, text="Logout", command=self.welcome_menu).pack()

    def register_company(self):
        self.clear_window()
        willing_to_pay = messagebox.askyesno("Subscription", "Are you willing to pay the $10,000 subscription fee?")
        if not willing_to_pay:
            messagebox.showinfo("Subscription Required", "You need to subscribe to use our service. Goodbye!")
            self.root.quit()
            return

        while True:
            try:
                subscription_amount = simpledialog.askfloat("Subscription Fee", "Enter the subscription fee: $")
                if subscription_amount < 10000:
                    response = messagebox.askyesno("Insufficient Amount", "Insufficient amount. Please pay the full $10,000 subscription fee.\nDo you want to go back to the previous menu?")
                    if response:
                        self.welcome_menu()
                        return
                else:
                    break
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            messagebox.showinfo("Subscription Required", "You need to subscribe to use our service. Goodbye!")
            self.root.quit()
            return

        name = simpledialog.askstring("Company Name", "Enter company name:")
        delivery_cost_per_km = simpledialog.askfloat("Delivery Cost per km", "Enter delivery cost per km: $")
        company = Company(name, delivery_cost_per_km)
        self.subscribe_company(company)
        self.companies.append(company)
        self.company_id = "{:06d}".format(random.randint(0, 999999))
        self.company_id =  "{:06d}".format(random.randint(0, 999999))
        messagebox.showinfo("Success", f"Company {name} registered and subscribed successfully." f" company_id: {self.company_id}")
        self.company_menu()
        
    def subscribe_company(self, company):
        messagebox.showinfo("Subscribing", f"Subscribing {company.name} for $10,000 yearly fee...")
        company.subscribe()
        messagebox.showinfo("Subscription Successful", f"Subscription successful. {company.name} is now active until {company.subscription_end_date}.")

    def User_menu(self):
        self.clear_window()
        tk.Label(self.root, text="User Menu").pack()
        tk.Button(self.root, text="List Subscribed Companies", command=self.list_subscribed_companies).pack()
        tk.Button(self.root, text="Create Waybill", command=self.create_waybill).pack()
        tk.Button(self.root, text="Add Tracking Data", command=self.add_tracking_data).pack()
        tk.Button(self.root, text="Display Tracking Data", command=self.display_tracking_data).pack()
        tk.Button(self.root, text="Generate PDF Waybill", command=self.generate_pdf_waybill).pack()
        tk.Button(self.root, text="Logout", command=self.welcome_menu).pack()

    def list_subscribed_companies(self):
        self.clear_window()
        tk.Label(self.root, text="List of Subscribed Companies").pack()
        active_companies = [c for c in self.companies if c.is_subscription_active()]
        if not active_companies:
            tk.Label(self.root, text="No companies currently subscribed.").pack()
        else:
            for company in active_companies:
                tk.Label(self.root, text=f"{company.name} (ID: {company.company_id} (rate per distance{company.delivery_cost_per_km}))").pack()
        tk.Button(self.root, text="Back to User Menu", command=self.User_menu).pack()

    def create_waybill(self):
        self.clear_window()
        tk.Label(self.root, text="Create Waybill").pack()
        sender = simpledialog.askstring("Sender Name", "Enter sender's name:")
        sender_location = simpledialog.askstring("Sender Location", "Enter sender's location:")
        receiver = simpledialog.askstring("Receiver Name", "Enter receiver's name:")
        receiver_location = simpledialog.askstring("Receiver Location", "Enter receiver's location:")
        items = simpledialog.askstring("Items", "Enter items to be delivered:")
        weight = simpledialog.askfloat("Weight", "Enter total weight (in kg):")
        is_fragile = messagebox.askyesno("Fragile Item", "Is the item fragile?")
        waybill = Waybill(sender, sender_location, receiver, receiver_location, items, weight, is_fragile)
        tk.Label(self.root, text="Select a company for delivery:").pack()
        active_companies = [c for c in self.companies if c.is_subscription_active()]
        company_var = tk.StringVar(self.root)
        company_var.set(active_companies[0].name)
        tk.OptionMenu(self.root, company_var, *[company.name for company in active_companies]).pack()
        def select_company():
            selected_company_name = company_var.get()
            selected_company = next(c for c in active_companies if c.name == selected_company_name)
            waybill.associate_company(selected_company)
            self.waybills.append(waybill)
            waybill.display_receipt()
            self.User_menu()
        tk.Button(self.root, text="Create Waybill", command=select_company).pack()

    def add_tracking_data(self):
        self.clear_window()
        waybill_id = simpledialog.askstring("Waybill ID", "Enter the Waybill ID:")
        waybill = next((w for w in self.waybills if w.waybill_id == waybill_id), None)
        if waybill:
            location = simpledialog.askstring("Current Location", "Enter current location:")
            waybill.add_tracking(location)
            messagebox.showinfo("Success", "Tracking data added successfully.")
        else:
            messagebox.showerror("Error", f"Waybill ID {waybill_id} not found.")
        self.User_menu()

    def display_tracking_data(self):
        self.clear_window()
        waybill_id = simpledialog.askstring("Waybill ID", "Enter the Waybill ID:")
        waybill = next((w for w in self.waybills if w.waybill_id == waybill_id), None)
        if waybill:
            waybill.display_tracking()
        else:
            messagebox.showerror("Error", f"Waybill ID {waybill_id} not found.")
        self.User_menu()
    def view_invoices(self):
        self.clear_window()
        tk.Label(self.root, text="Select a company to view invoices").pack()
        company_ids = [str(c.company_id) for c in self.companies]
        company_id_var = tk.StringVar(self.root)
        company_id_var.set(company_ids[0])
        tk.OptionMenu(self.root, company_id_var, *company_ids).pack()
        def view_invoices_for_company():
            company_id = company_id_var.get()
            company = next((c for c in self.companies if str(c.company_id) == company_id), None)
            if company:
                self.clear_window()
                tk.Label(self.root, text=f"Invoices for {company.name}").pack()
                company_waybills = [w for w in self.waybills if w.associated_company == company]
                if not company_waybills:
                    tk.Label(self.root, text="No waybills found for this company.").pack()
                else:
                    for waybill in company_waybills:
                        tk.Label(self.root, text=f"Waybill ID: {waybill.waybill_id} | Sender: {waybill.sender} | Receiver: {waybill.receiver} | Items: {waybill.items} | Profit: ${waybill.estimated_cost:.2f}").pack()
                tk.Button(self.root, text="Back to Company Menu", command=self.company_menu).pack()
            else:
                 messagebox.showerror("Error", "Invalid company ID.")
                 self.company_menu()
        tk.Button(self.root, text="View Invoices", command=view_invoices_for_company).pack()

    def generate_pdf_waybill(self):
        waybill_id = simpledialog.askstring("Waybill ID", "Enter the Waybill ID:")
        waybill = next((w for w in self.waybills if w.waybill_id == waybill_id), None)
        if waybill:
            generate_pdf(waybill)
        else:
            messagebox.showerror("Error", f"Waybill ID {waybill_id} not found.")
        self.User_menu()

   

def generate_pdf(waybill):
    # Placeholder function for generating a PDF
    messagebox.showinfo("Generate PDF", f"Generating PDF for Waybill ID: {waybill.waybill_id}")

if __name__ == "__main__":
   
    root =tk.Tk()
    app = LogisticsApp(root)
    root.mainloop()



            