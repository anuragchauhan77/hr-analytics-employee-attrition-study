
SELECT Department,
       COUNT(*) AS TotalEmployees
FROM employees
GROUP BY Department
ORDER BY TotalEmployees DESC;
