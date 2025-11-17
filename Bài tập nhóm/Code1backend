# shop_backend.py
import pandas as pd
import hashlib

# ======== Lớp Người dùng ========
class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

class UserManager:
    def __init__(self, users=None):
        self.users = users if users else []

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        if any(u.username == username for u in self.users):
            return None  # user tồn tại
        new_user = User(username, self.hash_password(password))
        self.users.append(new_user)
        return new_user

    def login(self, username, password):
        pw_hash = self.hash_password(password)
        for u in self.users:
            if u.username == username and u.password_hash == pw_hash:
                return u
        return None

# ======== Lớp Sản phẩm ========
class Product:
    def __init__(self, pid, name, category, price, stock, sizes, colors, sold_count=0):
        self.id = pid
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.sizes = sizes
        self.colors = colors
        self.sold_count = sold_count

# ======== DataAccess ========
USER_FILE = "users.xlsx"
PRODUCT_FILE = "shop_products.xlsx"

class DataAccess:
    def load_users(self):
        try:
            df = pd.read_excel(USER_FILE)
            return [User(row['username'], row['password_hash']) for idx, row in df.iterrows()]
        except FileNotFoundError:
            return []

    def save_users(self, users):
        data = [{'username': u.username, 'password_hash': u.password_hash} for u in users]
        df = pd.DataFrame(data)
        df.to_excel(USER_FILE, index=False)

    def load_products(self):
        try:
            df = pd.read_excel(PRODUCT_FILE)
            products = []
            for idx, row in df.iterrows():
                products.append(Product(
                    pid=row['id'],
                    name=row['name'],
                    category=row['category'],
                    price=int(row['price']),
                    stock=int(row['stock']),
                    sizes=row['sizes'],
                    colors=row['colors'],
                    sold_count=int(row['sold_count'])
                ))
            return products
        except FileNotFoundError:
            return []

    def save_products(self, products):
        data = []
        for p in products:
            data.append({
                'id': p.id,
                'name': p.name,
                'category': p.category,
                'price': p.price,
                'stock': p.stock,
                'sizes': p.sizes,
                'colors': p.colors,
                'sold_count': p.sold_count
            })
        df = pd.DataFrame(data)
        df.to_excel(PRODUCT_FILE, index=False)

# ======== Quản lý sản phẩm ========
class ProductManager:
    def __init__(self, products=None):
        self.products = products if products else []

    def search_products(self, keyword):
        keyword = keyword.lower()
        return [p for p in self.products if keyword in p.name.lower()]

    def get_top_selling(self, n=10):
        return sorted(self.products, key=lambda p: p.sold_count, reverse=True)[:n]

    def get_product_by_id(self, pid):
        for p in self.products:
            if p.id == pid:
                return p
        return None

# ======== Chương trình chính ========
def main():
    print("===== Shop Thời Trang =====")

    data_access = DataAccess()
    users = data_access.load_users()
    products = data_access.load_products()

    user_manager = UserManager(users)
    product_manager = ProductManager(products)
    current_user = None
    cart = []

    # Đăng nhập/Đăng ký
    while current_user is None:
        print("\n1. Đăng nhập")
        print("2. Đăng ký")
        choice = input("Chọn: ")
        if choice == "1":
            username = input("Tên đăng nhập: ")
            password = input("Mật khẩu: ")
            current_user = user_manager.login(username, password)
            if current_user:
                print(f"✔ Đăng nhập thành công! Xin chào {current_user.username}")
            else:
                print("❌ Sai tên đăng nhập hoặc mật khẩu")
        elif choice == "2":
            username = input("Tên đăng nhập: ")
            password = input("Mật khẩu: ")
            current_user = user_manager.register(username, password)
            if current_user:
                print(f"✔ Đăng ký thành công! Bạn đã đăng nhập với tài khoản {current_user.username}")
                data_access.save_users(users)
            else:
                print("❌ Tên đăng nhập đã tồn tại")
        else:
            print("❌ Lựa chọn không hợp lệ")

    # Menu chính
    while True:
        print("\n===== Menu =====")
        print("1. Top 10 sản phẩm bán chạy")
        print("2. Tìm kiếm sản phẩm")
        print("3. Xem giỏ hàng")
        print("4. Thanh toán")
        print("5. Đăng xuất/Thoát")
        choice = input("Chọn: ")

        if choice == "1":
            top_products = product_manager.get_top_selling()
            print("==== Top 10 sản phẩm bán chạy ====")
            for p in top_products:
                print(f"{p.id} | {p.name} | {p.category} | Giá: {p.price} | Đã bán: {p.sold_count}")

        elif choice == "2":
            keyword = input("Nhập từ khóa tìm kiếm: ")
            results = product_manager.search_products(keyword)
            if results:
                print(f"==== Kết quả tìm kiếm ({len(results)}) ====")
                for idx, p in enumerate(results, 1):
                    print(f"{idx}. {p.id} | {p.name} | {p.category} | Giá: {p.price} | Size: {p.sizes} | Màu: {p.colors}")
                add_choice = input("Thêm sản phẩm vào giỏ hàng? (y/n): ")
                if add_choice.lower() == 'y':
                    ids = input("Nhập ID sản phẩm (cách nhau bằng dấu ,): ").split(",")
                    for pid in ids:
                        prod = product_manager.get_product_by_id(pid.strip())
                        if prod:
                            cart.append(prod)
                            print(f"✔ Đã thêm {prod.name} vào giỏ hàng")
                        else:
                            print(f"❌ Không tìm thấy sản phẩm {pid.strip()}")
            else:
                print("❌ Không tìm thấy sản phẩm phù hợp")

        elif choice == "3":
            if not cart:
                print("Giỏ hàng trống")
            else:
                print("==== Giỏ hàng của bạn ====")
                total = 0
                for p in cart:
                    print(f"{p.id} | {p.name} | Giá: {p.price}")
                    total += p.price
                print(f"Tổng cộng: {total}")

        elif choice == "4":
            if not cart:
                print("❌ Giỏ hàng trống")
            else:
                total = sum(p.price for p in cart)
                print(f"💰 Tổng thanh toán: {total}")
                confirm = input("Xác nhận thanh toán? (y/n): ")
                if confirm.lower() == 'y':
                    for p in cart:
                        p.sold_count += 1
                        p.stock = max(0, p.stock - 1)
                    data_access.save_products(products)
                    cart.clear()
                    print("✔ Thanh toán thành công!")
                else:
                    print("❌ Thanh toán hủy")

        elif choice == "5":
            print("👋 Đăng xuất, tạm biệt!")
            data_access.save_users(users)
            break
        else:
            print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()
