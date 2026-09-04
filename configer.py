HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive'
}

URLS = {
    "products":  "https://oracleapex.com/ords/ifs315_4476838/4476838_API/GET_top_products_by_total_revenue",
    "customers": "https://oracleapex.com/ords/ifs315_4476838/4476838_API/GET_top_customers_by_spend",
    "orders":    "https://oracleapex.com/ords/ifs315_4476838/4476838_API/GET_order_status_breakdown_by_year",
    "inventory": "https://oracleapex.com/ords/ifs315_4476838/4476838_API/GET_inventory_distribution_across_warehouses",
    "sales":     "https://oracleapex.com/ords/ifs315_4476838/4476838_API/GETsalesmonthly"
}

OUTPUT_FILENAME = "combined_dashboard.html"