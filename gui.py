import tkinter as tk
from tkinter import ttk, messagebox


class HarvestApp:
    """
    Графический интерфейс программы.
    """

    def __init__(self, service):
        self.service = service

        self.root = tk.Tk()
        self.root.title("Ферма: учёт урожая")
        self.root.geometry("720x460")

        self._create_ui()


    def run(self):
        """
        Запускает главное окно.
        """

        self.root.mainloop()


    def _create_ui(self):
        """
        Создаёт все элементы интерфейса.
        """

        # Блок ввода данных
        frame_form = ttk.LabelFrame(self.root, text="Данные культуры")
        frame_form.pack(padx=10, pady=10, fill="x")

        ttk.Label(
            frame_form,
            text="Название культуры:"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.entry_name = ttk.Entry(frame_form, width=30)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(
            frame_form,
            text="Площадь посева (га):"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.entry_area = ttk.Entry(frame_form, width=30)
        self.entry_area.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(
            frame_form,
            text="Урожайность (т/га):"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.entry_yield = ttk.Entry(frame_form, width=30)
        self.entry_yield.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(
            frame_form,
            text="Добавить культуру",
            command=self._add_crop
        ).grid(row=3, column=0, columnspan=2, pady=5)

        # Таблица с результатами
        frame_table = ttk.Frame(self.root)
        frame_table.pack(padx=10, pady=5, fill="both", expand=True)

        columns = ("name", "area", "yield", "volume")

        self.tree = ttk.Treeview(
            frame_table,
            columns=columns,
            show="headings",
            height=8
        )

        self.tree.heading("name", text="Культура")
        self.tree.heading("area", text="Площадь, га")
        self.tree.heading("yield", text="Урожайность, т/га")
        self.tree.heading("volume", text="Объём урожая, т")

        self.tree.column("name", width=180, anchor="w")
        self.tree.column("area", width=110, anchor="center")
        self.tree.column("yield", width=140, anchor="center")
        self.tree.column("volume", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(
            frame_table,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления
        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(pady=5)

        ttk.Button(
            frame_buttons,
            text="Рассчитать общий объём",
            command=self._calculate_total
        ).pack(side="left", padx=5)

        ttk.Button(
            frame_buttons,
            text="Очистить всё",
            command=self._clear_all
        ).pack(side="left", padx=5)

        # Итоговая строка
        self.label_total = ttk.Label(
            self.root,
            text="Общий объём урожая за сезон: 0.00"
        )
        self.label_total.pack(pady=10)


    def _add_crop(self):
        """
        Добавляет культуру через интерфейс.
        """

        try:
            area = self._parse_float(self.entry_area)
            yield_per_ha = self._parse_float(self.entry_yield)

            crop = self.service.add_crop(
                self.entry_name.get(),
                area,
                yield_per_ha
            )

        except ValueError as error:
            messagebox.showerror("Ошибка", str(error))
            return

        self.tree.insert(
            "",
            "end",
            values=(
                crop.name,
                f"{crop.area:.2f}",
                f"{crop.yield_per_ha:.2f}",
                f"{crop.volume:.2f}"
            )
        )

        self._clear_entries()


    def _calculate_total(self):
        """
        Показывает общий объём урожая.
        """

        total = self.service.total_volume()

        self.label_total.config(
            text=f"Общий объём урожая за сезон: {total:.2f}"
        )


    def _clear_all(self):
        """
        Очищает таблицу и список культур.
        """

        if not self.service.has_crops():
            return

        if messagebox.askyesno(
            "Очистка",
            "Удалить все введённые культуры?"
        ):
            self.service.clear()
            self.tree.delete(*self.tree.get_children())
            self.label_total.config(
                text="Общий объём урожая за сезон: 0.00"
            )


    def _clear_entries(self):
        """
        Очищает поля ввода.
        """

        self.entry_name.delete(0, tk.END)
        self.entry_area.delete(0, tk.END)
        self.entry_yield.delete(0, tk.END)
        self.entry_name.focus()


    def _parse_float(self, entry):
        """
        Преобразует текст из поля ввода в число.
        """

        text = entry.get().strip().replace(",", ".")

        if not text:
            raise ValueError("Площадь и урожайность нужно ввести числами.")

        try:
            return float(text)
        except ValueError:
            raise ValueError("Площадь и урожайность нужно ввести числами.")