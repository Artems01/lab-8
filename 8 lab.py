import tkinter as tk
from tkinter import filedialog, messagebox
import math
import csv
import os


class Circle:
    def __init__(self, x, y, radius, color=""):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def area(self):
        return math.pi * (self.radius ** 2)

    def circumference(self):
        return 2 * math.pi * self.radius

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius,
                           outline="black", fill=self.color)


class CircleManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер Кругов")

        self.circles = []

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.load_button = tk.Button(root, text="Загрузить Круги", command=self.load_circles)
        self.load_button.pack()

        self.draw_button = tk.Button(root, text="Нарисовать Круги", command=self.draw_circles)
        self.draw_button.pack()

        self.move_button = tk.Button(root, text="Переместить Круг", command=self.move_circle)
        self.move_button.pack()

        self.dx_entry = tk.Entry(root)
        self.dx_entry.pack()
        self.dx_entry.insert(0, "")

        self.dy_entry = tk.Entry(root)
        self.dy_entry.pack()
        self.dy_entry.insert(0, "")

        # Кнопка для сегментации по площади
        self.segment_by_area_button = tk.Button(root, text="Сегментировать по Площади", command=self.segment_by_area)
        self.segment_by_area_button.pack()

        # Кнопка для сегментации по длине окружности
        self.segment_by_circumference_button = tk.Button(root, text="Сегментировать по Длине Окружности",
                                                         command=self.segment_by_circumference)
        self.segment_by_circumference_button.pack()

    def load_circles(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV файлы", "*.csv")])

        if not file_path or not os.path.exists(file_path):
            messagebox.showwarning("Предупреждение", "Файл не существует или не выбран.")
            return

        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 4:  # Ожидаем 4 значения: x, y, radius, color
                    messagebox.showerror("Ошибка",
                                         "Неверный формат данных в CSV. В каждой строке должно быть 4 значения.")
                    return

                try:
                    x = float(row[0])
                    y = float(row[1])
                    radius = float(row[2])
                    color = row[3]

                    if radius <= 0:
                        messagebox.showerror("Ошибка", "Радиус должен быть положительным числом.")
                        return

                    circle = Circle(x, y, radius, color)
                    self.circles.append(circle)
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат числа в CSV.")
                    return

        messagebox.showinfo("Успех", "Круги загружены успешно!")

    def move_circle(self):
        if not self.circles:
            messagebox.showwarning("Предупреждение", "Нет кругов для перемещения.")
            return

        try:
            dx = float(self.dx_entry.get())
            dy = float(self.dy_entry.get())
            for circle in self.circles:
                circle.move(dx, dy)
            messagebox.showinfo("Успех", "Круги перемещены успешно!")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные значения для dx и dy.")

    def draw_circles(self):
        self.canvas.delete("all")
        for circle in self.circles:
            circle.draw(self.canvas)

    def segment_by_area(self):
        area_info = "\n".join(f"Круг с площадью: {circle.area():.2f}" for circle in self.circles)
        if not area_info:
            messagebox.showinfo("Результат", "Нет кругов для отображения.")
        else:
            messagebox.showinfo("Информация о Площадях", area_info)

    def segment_by_circumference(self):
        circumference_info = "\n".join(
            f"Круг с длиной окружности: {circle.circumference():.2f}" for circle in self.circles)
        if not circumference_info:
            messagebox.showinfo("Результат", "Нет кругов для отображения.")
        else:
            messagebox.showinfo("Информация о Длинах Окружностей", circumference_info)


if __name__ == "__main__":
    root = tk.Tk()
    app = CircleManagerApp(root)
    root.mainloop()
