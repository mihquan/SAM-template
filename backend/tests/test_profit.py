from processor.business_logic import calculate_profit_and_margin


def test_profit_calculation():
    tx = {
        "revenue": 500,
        "cost": 300,
        "ad_spend": 100,
        "fees": 20,
    }

    profit, margin = calculate_profit_and_margin(tx)

    assert profit == 80
    assert round(margin, 2) == 0.16
