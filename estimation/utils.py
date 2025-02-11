from datetime import datetime


class FilterContent:
    """
    Фільтрує контент на відображенях контрактів і таблиці виконнання.
    """

    def __init__(self, request):
        self.MONTH = [
            ("Січень", "Січень"),
            ("Лютий", "Лютий"),
            ("Березень", "Березень"),
            ("Квітень", "Квітень"),
            ("Травень", "Травень"),
            ("Червень", "Червень"),
            ("Липень", "Липень"),
            ("Серпень", "Серпень"),
            ("Вересень", "Вересень"),
            ("Жовтень", "Жовтень"),
            ("Листопад", "Листопад"),
            ("Грудень", "Грудень"),
        ]
        self.current_year = datetime.now().year
        self.years = [
            str(year) for year in range(self.current_year, self.current_year - 5, -1)
        ]
        self.request = request

    def get_selected_month(self):
        return self.request.GET.get("month", "13")

    def get_selected_year(self):
        selected_year = self.request.GET.get("year", self.current_year)
        try:
            return int(selected_year)
        except ValueError:
            return "Всі"
