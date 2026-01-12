def calculate_profit_and_margin(tx: dict) -> tuple[float, float]:
    revenue = tx["revenue"]
    cost = tx["cost"]
    ad_spend = tx["ad_spend"]
    fees = tx["fees"]

    profit = revenue - cost - ad_spend - fees
    margin = profit / revenue if revenue > 0 else 0.0

    return profit, margin
