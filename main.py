
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from pathlib import Path

sns.set_style("whitegrid")

DATA_PATH = r"data\WA_Fn-UseC_-HR-Employee-Attrition.xlsx.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

print("\nInitial Shape:", df.shape)

print("\nChecking Missing Values:")
print(df.isnull().sum())

df.drop_duplicates(inplace=True)

print("\nShape After Cleaning:", df.shape)

attrition_counts = df['Attrition'].value_counts()

plt.figure(figsize=(6,6))
plt.pie(attrition_counts.values,
        labels=attrition_counts.index,
        autopct='%1.1f%%')
plt.title("Employee Attrition Distribution")
Path("output").mkdir(parents=True, exist_ok=True)
plt.savefig("output/attrition_distribution.png")
print("attrition_distribution.png saved successfully")
plt.close()

plt.figure(figsize=(8,6))
sns.boxplot(x='Attrition', y='MonthlyIncome', data=df)
plt.title("Monthly Income vs Attrition")
plt.savefig("output/monthly_income_vs_attrition.png")
print("monthly_income_vs_attrition.png saved successfully")
plt.close()

overtime_attrition = pd.crosstab(df['OverTime'], df['Attrition'])

overtime_attrition.plot(kind='bar', figsize=(8,6))
plt.title("Overtime vs Attrition")
plt.ylabel("Employee Count")
plt.tight_layout()
plt.savefig("output/overtime_vs_attrition.png")
print("overtime_vs_attrition.png saved successfully")
plt.close()

numeric_df = df.select_dtypes(include=np.number)

plt.figure(figsize=(14,10))
sns.heatmap(numeric_df.corr(), cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("output/correlation_heatmap.png")
print("correlation_heatmap.png saved successfully")
plt.close()

dept_attrition = pd.crosstab(df['Department'], df['Attrition'])

dept_attrition.plot(kind='bar', figsize=(10,6))
plt.title("Department-wise Attrition")
plt.ylabel("Employee Count")
plt.tight_layout()
plt.savefig("output/department_attrition.png")
print("department_attrition.png saved successfully")
plt.close()

conn = sqlite3.connect(':memory:')

df.to_sql(
    'employees',
    conn,
    index=False,
    if_exists='replace'
)

query = '''
SELECT Department,
       COUNT(*) AS TotalEmployees
FROM employees
GROUP BY Department
ORDER BY TotalEmployees DESC;
'''

result = pd.read_sql_query(query, conn)

print("\nDepartment-wise Employee Count (SQL):")
print(result)

print("\nProject Execution Completed Successfully!")
