import tkinter as tk
from tkinter import messagebox
from datetime import datetime

appointments = []

# ------------------ Customer Panel ------------------
def open_customer_panel():
    customer = tk.Toplevel(root)
    customer.title("پنل مشتری")
    customer.geometry("400x400")

    tk.Label(customer, text="نام مشتری").pack()
    entry_name = tk.Entry(customer)
    entry_name.pack()

    tk.Label(customer, text="نوع خدمات").pack()
    entry_service = tk.Entry(customer)
    entry_service.pack()

    tk.Label(customer, text="تاریخ (YYYY-MM-DD)").pack()
    entry_date = tk.Entry(customer)
    entry_date.pack()

    tk.Label(customer, text="ساعت (HH:MM)").pack()
    entry_time = tk.Entry(customer)
    entry_time.pack()

    def add_appointment():
        name = entry_name.get()
        service = entry_service.get()
        date = entry_date.get()
        time = entry_time.get()

        if not name or not service or not date or not time:
            messagebox.showwarning("خطا", "همه فیلدها را پر کنید")
            return

        try:
            appointment_time = datetime.strptime(
                f"{date} {time}", "%Y-%m-%d %H:%M"
            )
        except ValueError:
            messagebox.showerror("خطا", "فرمت تاریخ یا ساعت اشتباه است")
            return

        for app in appointments:
            if app["time"] == appointment_time:
                messagebox.showerror("خطا", "این تایم قبلاً رزرو شده")
                return

        appointments.append({
            "name": name,
            "service": service,
            "time": appointment_time
        })

        messagebox.showinfo("موفق", "نوبت شما ثبت شد ✅")
        customer.destroy()

    tk.Button(customer, text="ثبت نوبت", bg="green", fg="white",
              command=add_appointment).pack(pady=15)


# ------------------ Admin Panel ------------------
def open_admin_panel():
    admin = tk.Toplevel(root)
    admin.title("پنل مدیریت")
    admin.geometry("550x400")

    listbox = tk.Listbox(admin, width=70)
    listbox.pack(pady=10)

    def refresh_list():
        listbox.delete(0, tk.END)
        for i, app in enumerate(appointments):
            listbox.insert(
                tk.END,
                f"{i+1}. {app['name']} | {app['service']} | {app['time'].strftime('%Y-%m-%d %H:%M')}"
            )

    def delete_appointment():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("خطا", "یک نوبت انتخاب کنید")
            return
        index = selected[0]
        appointments.pop(index)
        refresh_list()

    tk.Button(admin, text="حذف نوبت انتخاب‌شده", bg="red", fg="white",
              command=delete_appointment).pack(pady=5)

    refresh_list()


# ------------------ Main Panel ------------------
root = tk.Tk()
root.title("سیستم نوبت‌دهی آرایشگاه")
root.geometry("300x250")

tk.Label(root, text="ورود به سیستم", font=("Arial", 14)).pack(pady=20)

tk.Button(root, text="پنل مشتری", width=20,
          command=open_customer_panel).pack(pady=10)

tk.Button(root, text="پنل مدیریت", width=20,
          command=open_admin_panel).pack(pady=10)

root.mainloop()
