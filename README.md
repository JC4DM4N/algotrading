# smartSS

smart Stocks & Shares. Gives a detailed and customisable breakdown of trading history and investment performance.

Includes python module smartSS:

    import smartSS

    # plot trade history with historical stock value.
    smartSS.plot.plot_activity_on_history('GOOGL')

    # get returns on first buy into Google.
    smartSS.get_asset_returns_since_buy('GOOGL',ibuy=0)

    # get current portfolio value.
    smartSS.useful_tools..get_portfolio_value()

Amongst other useful tools.

Requires user to tailor their ticker_map in config.py
