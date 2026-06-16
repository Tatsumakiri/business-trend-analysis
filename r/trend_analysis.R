library(tidyverse)
library(openxlsx)
library(zoo)

base_dir <- getwd()
data_path <- file.path(base_dir, "data", "sample_sales_data.csv")
output_dir <- file.path(base_dir, "output")
report_path <- file.path(output_dir, "trend_analysis_report_r.xlsx")
chart_path <- file.path(output_dir, "monthly_sales_trend_r.png")

if (!dir.exists(output_dir)) {
  dir.create(output_dir)
}

# 1. Load data
df <- read.csv(data_path)

# 2. Data preprocessing
df$Order.Date <- as.Date(df$Order.Date)
df$Order.Month <- format(df$Order.Date, "%Y-%m")
df$Amount <- as.numeric(df$Amount)

# 3. Monthly sales trend
monthly_sales <- df %>%
  group_by(Order.Month) %>%
  summarise(Monthly.Sales = sum(Amount, na.rm = TRUE), .groups = "drop") %>%
  arrange(Order.Month)

# 4. Month-over-month growth rate
monthly_sales <- monthly_sales %>%
  mutate(
    Growth.Rate = (Monthly.Sales / lag(Monthly.Sales)) - 1,
    Growth.Rate.Percent = round(Growth.Rate * 100, 2)
  )

# 5. 3-month moving average
monthly_sales <- monthly_sales %>%
  mutate(
    Moving.Average.3M = rollmean(Monthly.Sales, k = 3, fill = NA, align = "right")
  )

# 6. Outlier detection
mean_sales <- mean(monthly_sales$Monthly.Sales, na.rm = TRUE)
std_sales <- sd(monthly_sales$Monthly.Sales, na.rm = TRUE)

monthly_sales <- monthly_sales %>%
  mutate(
    Outlier.Flag = ifelse(
      abs(Monthly.Sales - mean_sales) > 1.5 * std_sales,
      "Outlier",
      "Normal"
    )
  )

# 7. Category sales summary
category_sales <- df %>%
  group_by(Category) %>%
  summarise(Total.Sales = sum(Amount, na.rm = TRUE), .groups = "drop") %>%
  arrange(desc(Total.Sales))

# 8. Monthly x Category trend
monthly_category_trend <- df %>%
  group_by(Order.Month, Category) %>%
  summarise(Total.Sales = sum(Amount, na.rm = TRUE), .groups = "drop") %>%
  pivot_wider(
    names_from = Category,
    values_from = Total.Sales,
    values_fill = 0
  )

# 9. Create chart
png(chart_path, width = 1000, height = 600)
plot(
  monthly_sales$Monthly.Sales,
  type = "o",
  xaxt = "n",
  main = "Monthly Sales Trend - R Version",
  xlab = "Order Month",
  ylab = "Monthly Sales"
)
axis(1, at = 1:nrow(monthly_sales), labels = monthly_sales$Order.Month, las = 2)
dev.off()

# 10. Export Excel report
wb <- createWorkbook()

addWorksheet(wb, "Cleaned Data")
writeData(wb, "Cleaned Data", df)

addWorksheet(wb, "Monthly Trend")
writeData(wb, "Monthly Trend", monthly_sales)

addWorksheet(wb, "Category Sales")
writeData(wb, "Category Sales", category_sales)

addWorksheet(wb, "Monthly Category")
writeData(wb, "Monthly Category", monthly_category_trend)

saveWorkbook(wb, report_path, overwrite = TRUE)

cat("R Excel report created:", report_path, "\n")
cat("R chart created:", chart_path, "\n")
