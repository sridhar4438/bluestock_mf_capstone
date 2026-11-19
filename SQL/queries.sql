-- Q1: Top 5 funds by AUM (Rs. crore)
SELECT scheme_name, fund_house, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- Q2: Average monthly NAV of HDFC Top 100 (last 12 months)
SELECT strftime('%Y-%m', date) AS month, ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
WHERE amfi_code = '125497'
GROUP BY month
ORDER BY month DESC
LIMIT 12;

-- Q3: Yearly SIP inflow and year-on-year growth
WITH yearly AS (
    SELECT substr(month, 1, 4) AS year, SUM(sip_inflow_crore) AS total
    FROM fact_sip_industry
    GROUP BY year
)
SELECT year,
       ROUND(total) AS total_sip_crore,
       ROUND((total - LAG(total) OVER (ORDER BY year)) * 100.0
             / LAG(total) OVER (ORDER BY year), 1) AS yoy_growth_pct
FROM yearly;

-- Q4: Total transaction amount by state
SELECT state, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;

-- Q5: Funds with expense ratio below 1%
SELECT scheme_name, fund_house, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

-- Q6: AUM by fund house on the latest date
SELECT fund_house, aum_lakh_crore
FROM fact_aum
WHERE date = (SELECT MAX(date) FROM fact_aum)
ORDER BY aum_lakh_crore DESC;

-- Q7: SIP vs Lumpsum vs Redemption split
SELECT transaction_type, COUNT(*) AS num_transactions,
       SUM(amount_inr) AS total_amount_inr,
       ROUND(AVG(amount_inr)) AS avg_amount_inr
FROM fact_transactions
GROUP BY transaction_type;

-- Q8: Average SIP amount by age group
SELECT age_group, ROUND(AVG(amount_inr)) AS avg_sip_inr, COUNT(*) AS num_sips
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY age_group
ORDER BY age_group;

-- Q9: Top 5 funds by Sharpe ratio
SELECT f.scheme_name, f.category, p.sharpe_ratio, p.return_3yr_pct
FROM fact_performance p
JOIN dim_fund f ON f.amfi_code = p.amfi_code
ORDER BY p.sharpe_ratio DESC
LIMIT 5;

-- Q10: T30 vs B30 city contribution
SELECT city_tier, COUNT(*) AS num_transactions,
       SUM(amount_inr) AS total_amount_inr,
       ROUND(SUM(amount_inr) * 100.0 / (SELECT SUM(amount_inr) FROM fact_transactions), 1) AS pct_of_total
FROM fact_transactions
GROUP BY city_tier;