import pandas as pd
import numpy as np


EXPENSES = (
    "Bank Fees",
    "Clothing",
    "Consumables",
    "Entertainment",
    "Hotels",
    "Interest Payments",
    "Meals",
    "Memberships",
    "Pension Plan Contributions" "Rent",
    "Service Fees",
    "Travel Fares",
    "Utilities",
    "Cleaning Supplies",
    "Communication Charges",
    "Energy",
    "Food",
    "Insurance",
    "Maintenance",
    "Medical Costs",
    "Office Supplies",
    "Professional Service Fees",
    "Repair Costs",
    "Taxes",
    "Tuition",
    "Vehicle Lease",
)


class Seeder:
    def generate(self):
        with pd.ExcelWriter("expenses_seed_example.xlsx", engine="xlsxwriter") as writer:
            for sheet_name in EXPENSES:
                dates = pd.date_range(start="2020-01-01", end="2021-01-01")
                data = {
                    "date": dates,
                    "amount": pd.Series(np.random.choice(np.random.randint(100, size=150), size=dates.size)),
                }
                df = pd.DataFrame(data, columns=["date", "amount"])
                df.to_excel(writer, sheet_name=sheet_name)


if __name__ == "__main__":
    s = Seeder()
    s.generate()
