import xlsxwriter
import random

# Tạo file Excel
workbook = xlsxwriter.Workbook('shop_products.xlsx')
worksheet = workbook.add_worksheet()

# Header
headers = ["id","name","category","price","stock","sizes","colors","sold_count"]
for col, header in enumerate(headers):
    worksheet.write(0, col, header)

categories = {
    "Áo": ["Áo thun hoạt hình", "Áo sơ mi", "Áo dài tay", "Áo khoác gió", "Áo hoodie", "Áo ba lỗ"],
    "Quần": ["Quần jean", "Quần short", "Quần kaki", "Quần thể thao", "Quần baggy"],
    "Giày": ["Giày thể thao", "Giày sneaker", "Giày búp bê", "Giày cao gót", "Giày sandal"],
    "Mũ": ["Mũ lưỡi trai", "Mũ len", "Mũ bucket", "Mũ nón rộng vành"],
    "Phụ kiện": ["Thắt lưng", "Khăn quàng", "Túi xách", "Ví", "Vòng tay"]
}

sizes_options = ["S", "M", "L", "XL"]
colors_options = ["Đỏ", "Đen", "Trắng", "Xanh", "Vàng", "Xám"]

for i in range(1, 201):
    pid = f"P{i:04d}"
    category = random.choice(list(categories.keys()))
    name = random.choice(categories[category])
    price = random.randint(2,40) * 50000  # làm tròn 50.000
    stock = random.randint(10,100)
    sizes = ",".join(random.sample(sizes_options, random.randint(1,len(sizes_options))))
    colors = ",".join(random.sample(colors_options, random.randint(1,len(colors_options))))
    sold_count = random.randint(0,500)

    row = [pid,name,category,price,stock,sizes,colors,sold_count]
    for col, value in enumerate(row):
        worksheet.write(i, col, value)

workbook.close()
print("✔ File shop_products.xlsx đã được tạo thành công!")
