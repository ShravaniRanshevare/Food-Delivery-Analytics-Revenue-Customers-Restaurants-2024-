# ============================
# 1. Load Libraries & Data
# ============================

import pandas as pd
import duckdb
import seaborn as sns
import matplotlib.pyplot as plt


customers = pd.DataFrame({
    "customer_id": list(range(1,16)),
    "signup_date": [
        "2024-01-02","2024-01-05","2024-01-10","2024-01-12","2024-01-15",
        "2024-01-18","2024-01-20","2024-01-22","2024-01-25","2024-01-28",
        "2024-02-01","2024-02-03","2024-02-05","2024-02-07","2024-02-10"
    ],
    "city": [
        "London","London","Manchester","London","Manchester",
        "London","Manchester","London","Manchester","London",
        "London","Manchester","London","Manchester","London"
    ]
})

customers["signup_date"] = pd.to_datetime(customers["signup_date"])


restaurants = pd.DataFrame({
    "restaurant_id": [10,11,12,13,14,15,16,17],
    "name": [
        "Pasta Palace","Curry House","Burger Bros","Sushi Zen",
        "Taco Town","Pizza Planet","Noodle Nook","BBQ Barn"
    ],
    "cuisine": [
        "Italian","Indian","American","Japanese",
        "Mexican","Italian","Chinese","American"
    ],
    "city": [
        "London","London","Manchester","London",
        "Manchester","London","Manchester","London"
    ]
})

orders = pd.DataFrame({
    "order_id": list(range(100,140)),
    "customer_id": [
    1,1,1,
    2,2,
    3,3,3,
    4,4,4,
    5,5,
    6,6,6,6,
    7,7,
    8,8,8,
    9,9,9,
    10,10,
    11,11,11,
    12,12,
    13,13,13,
    14,14,
    15,15,
    15   # ← added one more to make 40
     ],

    "restaurant_id": [
        10,11,10, 12,12, 10,13,13, 14,10,11,
        12,15, 16,16,17,17, 10,10, 11,11,12,
        13,13,14, 15,15, 16,16,17,
        10,11, 12,12,13, 14,14, 15,15,13
    ],
    "order_time": [
    "2024-01-02 12:00","2024-01-05 18:30","2024-01-10 13:00",
    "2024-01-06 13:00","2024-01-15 14:00",
    "2024-01-11 19:00","2024-01-12 20:00","2024-01-20 12:30",
    "2024-01-13 18:00","2024-01-14 19:00","2024-01-18 20:00",
    "2024-01-16 12:30","2024-01-22 13:00",
    "2024-01-18 11:00","2024-01-20 12:00","2024-01-25 13:00","2024-01-28 14:00",
    "2024-01-19 15:00","2024-01-22 16:00",
    "2024-01-23 17:00","2024-01-25 18:00","2024-01-28 19:00",
    "2024-01-26 12:00","2024-01-28 13:00","2024-02-01 14:00",
    "2024-02-02 15:00","2024-02-05 16:00",
    "2024-02-03 17:00","2024-02-06 18:00","2024-02-08 19:00",
    "2024-02-04 12:00","2024-02-07 13:00",
    "2024-02-09 14:00","2024-02-10 15:00","2024-02-12 16:00",
    "2024-02-11 17:00","2024-02-13 18:00",
    "2024-02-14 19:00","2024-02-15 20:00","2024-02-17 16:00"
],

    "status": ["completed"] * 40,
    "total_amount": [
    25.50,18.00,27.00,
    22.00,19.00,
    30.00,15.00,20.00,
    12.00,14.00,18.00,
    15.00,22.00,
    10.00,12.00,14.00,16.00,
    25.00,28.00,
    18.00,20.00,22.00,
    30.00,32.00,35.00,
    40.00,42.00,
    12.00,14.00,16.00,
    20.00,22.00,
    24.00,26.00,28.00,
    30.00,32.00,
    34.00,36.00,
    38.00   # ← added to make 40
]

})

orders["order_time"] = pd.to_datetime(orders["order_time"])

order_items = pd.DataFrame([
    # Orders 100–106 (your original ones)
    [100, "Spaghetti Carbonara", 1, 12.00],
    [100, "Garlic Bread", 1, 4.00],

    [101, "Chicken Tikka", 1, 10.00],
    [101, "Naan Bread", 1, 2.00],

    [102, "Margherita Pizza", 1, 11.00],
    [102, "Tiramisu", 1, 6.00],

    [103, "Cheeseburger", 1, 9.00],
    [103, "Fries", 1, 3.00],

    [104, "Sushi Roll", 1, 12.00],
    [104, "Miso Soup", 1, 3.00],

    [105, "Ramen Bowl", 1, 10.00],
    [105, "Gyoza", 1, 5.00],

    [106, "Cheeseburger", 1, 9.00],
    [106, "Milkshake", 1, 4.00],

    # Orders 107–139 (new rows, same style)
    [107, "Tacos", 2, 4.00],
    [107, "Nachos", 1, 5.00],

    [108, "Pepperoni Pizza", 1, 12.00],
    [108, "Garlic Knots", 1, 4.00],

    [109, "Chow Mein", 1, 9.00],
    [109, "Spring Rolls", 1, 4.00],

    [110, "BBQ Ribs", 1, 14.00],
    [110, "Cornbread", 1, 3.00],

    [111, "Spaghetti Bolognese", 1, 11.00],
    [111, "Bruschetta", 1, 5.00],

    [112, "Butter Chicken", 1, 12.00],
    [112, "Naan Bread", 1, 2.00],

    [113, "Sushi Roll", 1, 12.00],
    [113, "Edamame", 1, 3.00],

    [114, "Tacos", 2, 4.00],
    [114, "Quesadilla", 1, 6.00],

    [115, "Margherita Pizza", 1, 11.00],
    [115, "Tiramisu", 1, 6.00],

    [116, "Chow Mein", 1, 9.00],
    [116, "Fried Rice", 1, 8.00],

    [117, "BBQ Ribs", 1, 14.00],
    [117, "Coleslaw", 1, 3.00],

    [118, "Cheeseburger", 1, 9.00],
    [118, "Fries", 1, 3.00],

    [119, "Sushi Roll", 1, 12.00],
    [119, "Miso Soup", 1, 3.00],

    [120, "Tacos", 2, 4.00],
    [120, "Nachos", 1, 5.00],

    [121, "Pepperoni Pizza", 1, 12.00],
    [121, "Garlic Knots", 1, 4.00],

    [122, "Chow Mein", 1, 9.00],
    [122, "Spring Rolls", 1, 4.00],

    [123, "BBQ Ribs", 1, 14.00],
    [123, "Cornbread", 1, 3.00],

    [124, "Spaghetti Carbonara", 1, 12.00],
    [124, "Garlic Bread", 1, 4.00],

    [125, "Butter Chicken", 1, 12.00],
    [125, "Naan Bread", 1, 2.00],

    [126, "Sushi Roll", 1, 12.00],
    [126, "Green Tea", 1, 2.00],

    [127, "Tacos", 2, 4.00],
    [127, "Quesadilla", 1, 6.00],

    [128, "Margherita Pizza", 1, 11.00],
    [128, "Panna Cotta", 1, 6.00],

    [129, "Chow Mein", 1, 9.00],
    [129, "Fried Rice", 1, 8.00],

    [130, "BBQ Ribs", 1, 14.00],
    [130, "Coleslaw", 1, 3.00],

    [131, "Cheeseburger", 1, 9.00],
    [131, "Fries", 1, 3.00],

    [132, "Sushi Roll", 1, 12.00],
    [132, "Edamame", 1, 3.00],

    [133, "Tacos", 2, 4.00],
    [133, "Nachos", 1, 5.00],

    [134, "Pepperoni Pizza", 1, 12.00],
    [134, "Garlic Knots", 1, 4.00],

    [135, "Chow Mein", 1, 9.00],
    [135, "Spring Rolls", 1, 4.00],

    [136, "BBQ Ribs", 1, 14.00],
    [136, "Cornbread", 1, 3.00],

    [137, "Spaghetti Bolognese", 1, 11.00],
    [137, "Bruschetta", 1, 5.00],

    [138, "Butter Chicken", 1, 12.00],
    [138, "Naan Bread", 1, 2.00],

    [139, "Sushi Roll", 1, 12.00],
    [139, "Green Tea", 1, 2.00],
], columns=["order_id", "item_name", "quantity", "price"])


con=duckdb.connect()

con.register("customers", customers)
con.register("orders", orders)
con.register("restaurants", restaurants)
con.register("order_items", order_items)


# =====================================
# 2. Daily and Monthly Revenue Analysis
# =====================================

"""
Daily and Monthly Revenue Analysis
-----------------------------------

This section examines revenue trends to understand demand patterns over time. Daily revenue
fluctuates throughout January and February, with a noticeable spike on 28 January driven by a cluster
of high‑value orders. Despite this spike, the 7‑day rolling average remains relatively stable,
indicating consistent underlying demand. Monthly order volume also shows a slight decline in February,
suggesting a mild seasonal or behavioural shift.

"""


daily=con.execute("""
SELECT DATE(order_time) as Date,SUM(total_amount) as daily_revenue
FROM orders
WHERE status ='completed'
GROUP BY Date
ORDER BY Date;
""").df()


plt.figure(figsize=(8,4))
sns.lineplot(data=daily,x="Date",y="daily_revenue",marker="o")
plt.title("Daily Revenue")
plt.show()


monthly = con.execute(
"""
SELECT 
    DATE_TRUNC('month', o.order_time) AS month,
    COUNT(*) AS orders
FROM orders o
WHERE status = 'completed'
GROUP BY DATE_TRUNC('month', o.order_time)
ORDER BY month;
""").df()

plt.figure(figsize=(8,4))
sns.lineplot(data=monthly,x="month",y="orders",marker="o")
plt.title("Monthly Active Users")
plt.show()


# ============================
# 3. Customer Behaviour
# ============================

"""
Customer Behaviour Analysis
---------------------------

This section explores customer engagement patterns, including reorder behaviour and loyalty.
Most customers place all their orders within the same month they signed up, resulting in a cohort age of 0
for the majority. A small number of customers show short reorder gaps (typically 2–5 days),
and only three customers qualify as loyal (3+ completed orders). This indicates strong short‑term engagement
but limited long‑term retention, highlighting an opportunity to improve customer loyalty.

"""

order_rate=con.execute("""
WITH first_orders AS (
SELECT c.customer_id , c.signup_date, MIN(DATE(o.order_time)) as first_order_date
FROM customers c LEFT JOIN orders o ON (o.customer_id = c.customer_id)
GROUP BY c.customer_id,c.signup_date)

SELECT SUM(first_order_date==signup_date)::DOUBLE /COUNT(*) as order_rate
FROM first_orders;
""").df()

cust_life=con.execute(
"""
SELECT c.customer_id,c.city,MIN(DATE(o.order_time)) as first_order_date,
MAX(DATE(o.order_time)) as last_order_date, COUNT(*) as total_orders, SUM(o.total_amount) as total_spend,
AVG(o.total_amount) as avg_spend, MAX(DATE(o.order_time))- MIN(DATE(o.order_time)) as days_active
FROM customers c JOIN orders o ON c.customer_id=o.customer_id
WHERE o.status='completed'
GROUP BY c.customer_id,c.city
ORDER BY total_spend DESC;
""").df()

plt.figure(figsize=(10,5))
sns.scatterplot(data=cust_life, x="total_orders",y="total_spend",hue="city",s=100)
plt.title("Total Spend vs Total Orders")
plt.xlabel("Total Orders")
plt.ylabel("Total Spend")
plt.tight_layout()
plt.show()

reorder_rate = con.execute(
"""
WITH counts AS (
    SELECT customer_id, restaurant_id, COUNT(*) AS orders_at_restaurant
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id, restaurant_id
)
SELECT COUNT(DISTINCT customer_id) FILTER (WHERE orders_at_restaurant >= 2)::DOUBLE
       / COUNT(DISTINCT customer_id) AS reorder_rate
FROM counts;
""").df()

time_between=con.execute(
"""
With first_order as (
Select c. customer_id, o.order_time as time, ROW_NUMBER() OVER(PARTITION BY c.customer_id ORDER BY o.order_time) as num
FROM customers c JOIN orders o on (c.customer_id=o.customer_id)
WHERE o.status='completed' )

SELECT f1.customer_id, DATE(f1.time) as Date ,DATE(f1.time) ,DATE(f2.time) ,f2.time - f1.time as time_diff
FROM first_order f1 JOIN first_order f2 ON ( f1.customer_id=f2.customer_id)
AND f1.num=1 AND f2.num=2
ORDER BY f1.customer_id, Date;
""").df()

time_between["time_diff"] = time_between["time_diff"].dt.total_seconds() / 86400


plt.figure(figsize=(10,5))
sns.barplot(data=time_between,x="customer_id",y="time_diff")
plt.title("Number of days between first and second order Per Customer")
plt.show()

loyal_cust=con.execute(
"""
SELECT customer_id , COUNT(*) as order_count
FROM orders
WHERE status='completed'
GROUP BY customer_id
HAVING COUNT(*) >=3
ORDER BY order_count DESC;
""").df()

plt.figure(figsize=(10,5))
sns.barplot(data= loyal_cust ,x="customer_id",y="order_count")
plt.title("Loyal Customers and their order count")
plt.show()

# ============================
# 4. Restaurant Performance
# ============================

"""
Restaurant Performance Analysis

This section evaluates restaurant‑level performance across revenue, cuisine popularity,
and menu contribution. Burger Bros, Pasta Palace, and Taco Town emerge as top performers,
while Noodle Nook generates the lowest revenue. Cuisine‑level analysis shows strong demand for American,
Italian, and Indian dishes. Menu item breakdowns reveal that a small number of items contribute
disproportionately to each restaurant’s revenue, offering opportunities for targeted menu optimisation
and promotional strategy.

"""

top_3_restaurants =con.execute("""
WITH rest_revenue AS(
SELECT r.city,r.restaurant_id,SUM(o.total_amount) as revenue
FROM restaurants r JOIN orders o ON( r.restaurant_id=o.restaurant_id)
WHERE o.status ='completed'
GROUP BY r.city,r.restaurant_id
),

ranked AS (
SELECT city,restaurant_id,revenue,RANK() OVER( PARTITION BY city ORDER BY revenue DESC) as rnk
FROM rest_revenue)

SELECT * from ranked
WHERE rnk <= 3
ORDER BY city,rnk ;
""").df()

g = sns.catplot(
    data=top_3_restaurants ,
    x="restaurant_id",
    y="revenue",
    col="city",
    kind="bar",
    height=4,
    aspect=1
)
g.fig.suptitle("Top 3 Restaurants by Revenue per City", y=1.05)
plt.show()


cancelled_order_rate  = con.execute(
"""
WITH cancelled AS (
SELECT r.city,COUNT(*) as c
FROM restaurants r JOIN orders o ON( r.restaurant_id=o.restaurant_id)
WHERE o.status='cancelled'
GROUP BY r.city),

total AS (
SELECT r.city,COUNT(*) as co
FROM restaurants r JOIN orders o ON( r.restaurant_id=o.restaurant_id)
GROUP BY r.city)

SELECT c.c/co.co AS cancel_rate
FROM cancelled c JOIN total co ON (c.city=co.city)
ORDER BY cancel_rate DESC;
""").df()


day_7_rolling = con.execute("""
WITH completed as (
SELECT DATE(order_time) as date , COUNT(*) as c
FROM orders
WHERE status = 'completed'
GROUP BY date)

SELECT date,c,AVG(c) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as avg
FROM completed
ORDER BY date ;
""").df()

plt.figure(figsize=(10,5))
sns.lineplot(data= day_7_rolling,x="date",y="c",color="steelblue",marker="o",label="Daily Completed orders")
sns.lineplot(data= day_7_rolling,x="date",y="avg",color="orange",marker="o",label="7 Day Rolling Avg")
plt.title("Daily Completed Orders with 7-Day Rolling Average")
plt.xlabel("Date")
plt.ylabel("Orders")
plt.legend()
plt.tight_layout()
plt.show()


revenue_AOV = con.execute(
"""
SELECT r.cuisine as cuisine ,SUM(o.total_amount) as revenue, AVG(o.total_amount) as avg
FROM restaurants r JOIN orders o ON( r.restaurant_id=o.restaurant_id)
WHERE o.status ='completed'
GROUP BY r.cuisine
ORDER BY revenue DESC;
""").df()

plt.figure(figsize=(10,5))
sns.barplot(data= revenue_AOV ,x="cuisine",y="revenue")
sns.barplot(data= revenue_AOV ,x="cuisine",y="avg")
plt.title("Total and Average Revenue Per Cuisine")
plt.legend(title="Colours of the two Measures", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.show()


pct_menu_item = con.execute(
"""
WITH item_revenue as (
SELECT order_id,item_name, quantity*price as revenue
FROM order_items
),

rest_revenue as(
SELECT o.restaurant_id,SUM(i.revenue) as rest_r
FROM item_revenue i JOIN orders o ON(o.order_id=i.order_id)
WHERE o.status='completed'
GROUP BY o.restaurant_id
),

item_breakdown AS (
SELECT o.restaurant_id, ir.item_name, SUM(ir.revenue) AS item_revenue
FROM orders o JOIN item_revenue ir USING (order_id)
WHERE o.status = 'completed'
GROUP BY o.restaurant_id, ir.item_name )

SELECT i.restaurant_id, i.item_name, i.item_revenue, i.item_revenue / r.rest_r AS pct_of_revenue
FROM item_breakdown i JOIN rest_revenue r USING (restaurant_id)
ORDER BY restaurant_id, pct_of_revenue DESC;

""").df()

pivot_pct=pct_menu_item.pivot(
    values="pct_of_revenue",
    index="restaurant_id",
    columns="item_name").fillna(0)

pivot_pct.plot(
    kind="bar",
    stacked=True,
    figsize=(10,5),
    colormap="tab20"
)

plt.title("Percentage of Revenue by Menu Item per Restaurant")
plt.xlabel("Restaurant ID")
plt.ylabel("Percentage of Revenue")
plt.legend(title="Menu Item", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()

popular_cuisine= con.execute(
"""
WITH per_city as (
SELECT r.city,r.cuisine,COUNT(o.order_id) as count
FROM restaurants r JOIN orders o ON( r.restaurant_id=o.restaurant_id)
WHERE o.status='completed'
GROUP BY r.city,r.cuisine),

ranked as (
SELECT city,cuisine,count,RANK() OVER(PARTITION BY city ORDER BY count DESC) as rnk
FROM per_city)

SELECT * from ranked
WHERE rnk=1
ORDER BY city,rnk;
""").df()

plt.figure(figsize=(10,5))
g=sns.catplot(
    data=popular_cuisine,
    x="cuisine",
    y="rnk",
    col="city",
    kind="bar",
    height=4,
    aspect=1)
g.fig.suptitle("Most Popular Cuisine per City",y=1.05)
plt.show()


# ============================
# 5. Cohort Analysis
# ============================

"""
Cohort Analysis
----------------------

This cohort analysis groups customers by their signup month and tracks whether they return to place orders
in subsequent months. Each row represents a signup cohort (e.g., January signups), and each column represents
the month in which customers placed an order after signup.Because most customers place multiple orders within
the same month they joined, retention is high at Cohort Age 0 but drops sharply in later months. Only one
customer returns after a longer gap (9 days), resulting in minimal activity in Cohort Age 1 and beyond.
This pattern indicates short‑cycle repeat behaviour rather than long‑term retention.


"""

cohort_retention= con.execute(
"""
WITH cohort as (
SELECT customer_id,DATE_TRUNC('month',signup_date) as cmonth
FROM customers
),

active as (
SELECT customer_id,DATE_TRUNC('month',order_time) as amonth
FROM orders
WHERE status ='completed'),

joined as (
SELECT cmonth,amonth,COUNT(DISTINCT a.customer_id) as active
FROM cohort c JOIN active a USING (customer_id)
GROUP BY cmonth, amonth)

SELECT * from joined
ORDER BY cmonth,amonth;
""").df()

cohort_pivot = cohort_retention.pivot(
    index="cmonth",
    columns="amonth",
    values="active"
).fillna(0)

plt.figure(figsize=(10,6))
sns.heatmap(
    cohort_pivot,
    annot=True,
    fmt=".0f",
    cmap="Blues"
)

plt.title("Cohort Retention Heatmap")
plt.xlabel("Active Month")
plt.ylabel("Cohort Month")
plt.tight_layout()
plt.show()



###key metrics###
print("Order Rate:", order_rate)
print("Reorder Rate:", reorder_rate)
print("Top Restaurants:", top_3_restaurants)


#===========#
  #THE END
#===========#









