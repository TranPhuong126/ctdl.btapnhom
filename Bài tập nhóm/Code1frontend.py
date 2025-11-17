import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pandas as pd

# ---------------- Load sản phẩm ----------------
PRODUCT_FILE = "shop_products.xlsx"
try:
    products_df = pd.read_excel(PRODUCT_FILE)
except:
    products_df = pd.DataFrame(columns=["id","name","category","price","stock","sizes","colors","sold_count"])

# ---------------- Quản lý người dùng ----------------
users = {}
current_user = None
cart = []

# ---------------- Chức năng người dùng ----------------
def register():
    global users
    username = simpledialog.askstring("Đăng ký", "Tên người dùng:")
    if not username: return
    if username in users:
        messagebox.showerror("Lỗi", "Tên đã tồn tại!")
        return
    password = simpledialog.askstring("Đăng ký", "Mật khẩu:", show="*")
    users[username] = password
    messagebox.showinfo("Thành công", "Đăng ký thành công!")

def login():
    global current_user
    username = simpledialog.askstring("Đăng nhập", "Tên người dùng:")
    if username not in users:
        messagebox.showerror("Lỗi", "Người dùng không tồn tại!")
        return
    password = simpledialog.askstring("Đăng nhập", "Mật khẩu:", show="*")
    if users[username] != password:
        messagebox.showerror("Lỗi", "Sai mật khẩu!")
        return
    current_user = username
    messagebox.showinfo("Thành công", f"Xin chào {username}")
    update_user_label()

def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Đăng xuất", "Bạn đã đăng xuất")
    update_user_label()

def update_user_label():
    user_label.config(text=f"Xin chào: {current_user}" if current_user else "Chưa đăng nhập")

# ---------------- Giỏ hàng ----------------
def add_to_cart(product_id):
    cart.append(product_id)
    messagebox.showinfo("Thành công", f"Đã thêm sản phẩm vào giỏ hàng")

def view_cart():
    if not cart:
        messagebox.showinfo("Giỏ hàng", "Giỏ hàng trống!")
        return
    cart_items = products_df[products_df['id'].isin(cart)]
    cart_text = ""
    total = 0
    for _, row in cart_items.iterrows():
        cart_text += f"{row['name']} - {row['price']} VNĐ\n"
        total += row['price']
    cart_text += f"\nTổng cộng: {total} VNĐ"
    messagebox.showinfo("Giỏ hàng", cart_text)

def checkout():
    global cart
    if not cart:
        messagebox.showinfo("Thanh toán", "Giỏ hàng trống!")
        return
    cart_items = products_df[products_df['id'].isin(cart)]
    total = cart_items['price'].sum()
    confirm = messagebox.askyesno("Thanh toán", f"Tổng tiền: {total} VNĐ. Xác nhận thanh toán?")
    if confirm:
        for pid in cart:
            idx = products_df.index[products_df['id']==pid][0]
            products_df.at[idx,'stock'] -= 1
            products_df.at[idx,'sold_count'] += 1
        cart = []
        messagebox.showinfo("Thanh toán", "Thanh toán thành công!")

# ---------------- Hiển thị sản phẩm ----------------
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def show_product_detail(prod):
    detail = tk.Toplevel(root)
    detail.title(prod['name'])
    detail.geometry("300x250")
    tk.Label(detail, text=prod['name'], font=("Arial",14,"bold")).pack(pady=5)
    tk.Label(detail, text=f"Giá: {prod['price']} VNĐ", fg="green").pack(pady=5)
    tk.Label(detail, text=f"Đã bán: {prod['sold_count']} sản phẩm").pack(pady=5)
    tk.Label(detail, text=f"Kích thước: {prod['sizes']}").pack(pady=5)
    tk.Label(detail, text=f"Màu sắc: {prod['colors']}").pack(pady=5)
    tk.Button(detail, text="Thêm vào giỏ", command=lambda pid=prod['id']: add_to_cart(pid)).pack(pady=10)

def display_products(df):
    clear_frame(product_frame)
    row = 0
    col = 0
    for _, prod in df.iterrows():
        frame = tk.Frame(product_frame, bd=1, relief="raised", padx=10, pady=10, bg="white")
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        tk.Label(frame, text=prod['name'], font=("Arial", 12, "bold"), bg="white").pack()
        tk.Label(frame, text=f"Giá: {prod['price']} VNĐ", fg="green", bg="white").pack()
        tk.Label(frame, text=f"Đã bán: {prod['sold_count']}", bg="white").pack()
        frame.bind("<Button-1>", lambda e, p=prod: show_product_detail(p))
        for widget in frame.winfo_children():
            widget.bind("<Button-1>", lambda e, p=prod: show_product_detail(p))
        col +=1
        if col>=4:
            col=0
            row+=1

# ---------------- Tìm kiếm & Gợi ý ----------------
def update_suggestions(event=None):
    keyword = search_entry.get().lower()
    clear_frame(suggestion_frame)
    # Nếu chưa nhập gì, hiển thị top 7 bán chạy
    if not keyword:
        top7 = products_df.sort_values('sold_count', ascending=False).head(7)
    else:
        top7 = products_df[products_df['name'].str.lower().str.contains(keyword)]
        top7 = top7.sort_values('sold_count', ascending=False).head(7)
    for prod in top7.itertuples():
        btn = tk.Button(suggestion_frame, text=f"{prod.name} (Đã bán: {prod.sold_count})",
                        anchor="w", relief="flat", bg="#FFFFEE",
                        command=lambda p=prod: show_product_detail(p))
        btn.pack(fill="x")

# ---------------- Filter theo danh mục ----------------
def filter_category(cat):
    df = products_df[products_df['category']==cat]
    display_products(df)

# ---------------- GUI Tkinter ----------------
root = tk.Tk()
root.title("ShopSensei")
root.geometry("1000x700")
root.configure(bg="#FFF8F0")

# Header
header = tk.Frame(root, bg="#FFDD99")
header.pack(fill="x")
tk.Label(header, text="ShopSensei", font=("Arial", 24), bg="#FFDD99").pack(side="left", padx=20)
user_label = tk.Label(header, text="Chưa đăng nhập", font=("Arial", 12), bg="#FFDD99")
user_label.pack(side="left", padx=10)
tk.Button(header, text="Đăng ký", command=register).pack(side="left", padx=5)
tk.Button(header, text="Đăng nhập", command=login).pack(side="left", padx=5)
tk.Button(header, text="Đăng xuất", command=logout).pack(side="left", padx=5)

# Search bar
search_frame = tk.Frame(root, bg="#FFF0DD")
search_frame.pack(fill="x", pady=5)
search_entry = tk.Entry(search_frame, width=50, font=("Arial",12))
search_entry.pack(side="left", padx=10, pady=5)
search_entry.bind("<KeyRelease>", update_suggestions)

suggestion_frame = tk.Frame(root, bg="#FFFFEE")
suggestion_frame.pack(fill="x")

tk.Button(search_frame, text="Xem giỏ", command=view_cart).pack(side="left", padx=5)
tk.Button(search_frame, text="Thanh toán", command=checkout).pack(side="left", padx=5)

# Main frame chứa sidebar + products
main_frame = tk.Frame(root, bg="#FFF8F0")
main_frame.pack(fill="both", expand=True)

# Sidebar danh mục
sidebar = tk.Frame(main_frame, width=200, bg="#FFDDAA")
sidebar.pack(side="left", fill="y")
tk.Label(sidebar, text="Danh mục", font=("Arial", 14, "bold"), bg="#FFDDAA").pack(pady=10)
categories = products_df['category'].unique() if not products_df.empty else []
for cat in categories:
    tk.Button(sidebar, text=cat, width=20, command=lambda c=cat: filter_category(c)).pack(pady=2)

# Frame sản phẩm
canvas = tk.Canvas(main_frame, bg="#FFF8F0")
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#FFF8F0")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

product_frame = scrollable_frame

# Hiển thị tất cả sản phẩm ban đầu
display_products(products_df)
update_suggestions()  # Hiển thị top 7 ban đầu

root.mainloop()
