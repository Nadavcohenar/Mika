import streamlit as st
import pandas as pd

def nursing_home_comparison(nursing_homes, years):
    results = {}

    for name, deposit, annual_erosion, monthly_payment in nursing_homes:
        data = []

        for year in range(1, years + 1):
            erosion_amount = (annual_erosion / 100) * deposit
            total_monthly_payment = (erosion_amount / 12) + monthly_payment

            data.append([year, deposit, annual_erosion, monthly_payment, total_monthly_payment])
            deposit -= erosion_amount

        # Calculate the sum of "Total Monthly Payment" for each year and add it as a new row
        total_monthly_payment_sum = sum(row[4] for row in data)
        total_monthly_payment_sum= total_monthly_payment_sum*12
        round(total_monthly_payment_sum,2)
        data.append(["", "", "", "", fr"Total {total_monthly_payment_sum}"])

        df = pd.DataFrame(data, columns=["Year", "Deposit (₪)", "Annual Erosion (%)", "Monthly Payment (₪)", "Total Monthly Payment (₪)"])
        results[name] = df

    return results

st.title("Assisted living- Ben Zion")

nursing_homes = []
num_nursing_homes = st.number_input("Enter the number of nursing homes:", min_value=1, step=1)

for i in range(num_nursing_homes):
    name = st.text_input(f"Enter the name of Nursing Home {i + 1}:")

    if not name:
        st.warning("Name cannot be empty. Please provide a name.")
        continue

    deposit = st.number_input(f"Enter the deposit for {name} in shekels:")
    annual_erosion = st.number_input(f"Enter the annual erosion for {name} in percentages:")
    monthly_payment = st.number_input(f"Enter the monthly payment for {name}:")

    nursing_homes.append((name, deposit, annual_erosion, monthly_payment))

years = st.number_input("Enter the number of years to calculate:", min_value=1, step=1)

if st.button("Calculate"):
    results = nursing_home_comparison(nursing_homes, int(years))

    for name, df in results.items():
        st.subheader(f"Results for {name}:")
        st.dataframe(df)
