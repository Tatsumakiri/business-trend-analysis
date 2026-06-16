import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sample_sales_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
REPORT_PATH = OUTPUT_DIR / "trend_analysis_report.xlsx"
CHART_PATH = OUTPUT_DIR / "monthly_sales_trend.png"

OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    # 1. Load data
    df = pd.read_csv(DATA_PATH)

    # 2. Data preprocessing
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # 3. Monthly sales trend
    monthly_sales = (
        df.groupby("Order Month")["Amount"]
        .sum()
        .reset_index()
        .rename(columns={"Amount": "Monthly Sales"})
    )

    # 4. Month-over-month growth rate
    monthly_sales["Growth Rate"] = monthly_sales["Monthly Sales"].pct_change()
    monthly_sales["Growth Rate (%)"] = (monthly_sales["Growth Rate"] * 100).round(2)

    # 5. Moving average
    monthly_sales["3-Month Moving Average"] = (
        monthly_sales["Monthly Sales"]
        .rolling(window=3)
        .mean()
        .round(2)
    )

    # 6. Outlier detection using mean and standard deviation
    mean_sales = monthly_sales["Monthly Sales"].mean()
    std_sales = monthly_sales["Monthly Sales"].std()

    monthly_sales["Outlier Flag"] = monthly_sales["Monthly Sales"].apply(
        lambda x: "Outlier" if abs(x - mean_sales) > 1.5 * std_sales else "Normal"
    )

    # 7. Category sales summary
    category_sales = (
        df.groupby("Category")["Amount"]
        .sum()
        .reset_index()
        .rename(columns={"Amount": "Total Sales"})
        .sort_values("Total Sales", ascending=False)
    )

    # 8. Monthly x Category trend
    monthly_category_trend = pd.pivot_table(
        df,
        index="Order Month",
        columns="Category",
        values="Amount",
        aggfunc="sum",
        fill_value=0
    )

    # 9. Create chart
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_sales["Order Month"], monthly_sales["Monthly Sales"], marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Order Month")
    plt.ylabel("Monthly Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_PATH)
    plt.close()

    # 10. Export Excel report
    with pd.ExcelWriter(REPORT_PATH, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)
        monthly_sales.to_excel(writer, sheet_name="Monthly Trend", index=False)
        category_sales.to_excel(writer, sheet_name="Category Sales", index=False)
        monthly_category_trend.to_excel(writer, sheet_name="Monthly Category")

        # Adjust column widths
        for sheet_name, worksheet in writer.sheets.items():
            for column_cells in worksheet.columns:
                max_length = 0
                column_letter = column_cells[0].column_letter

                for cell in column_cells:
                    if cell.value is not None:
                        max_length = max(max_length, len(str(cell.value)))

                worksheet.column_dimensions[column_letter].width = max_length + 3

    print(f"Excel report created: {REPORT_PATH}")
    print(f"Chart created: {CHART_PATH}")

if __name__ == "__main__":
    main()
