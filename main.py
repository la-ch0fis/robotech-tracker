import yfinance as yf
import pandas as pd


def find_peaks_and_troughs(data, window=60):
    data['rolling_max'] = data['High'].rolling(window, center=True).max()
    data['peak'] = data['High'] == data['rolling_max']

    data['rolling_min'] = data['Low'].rolling(window, center=True).min()
    data['trough'] = data['Low'] == data['rolling_min']

    return data


def measure_trend_durations(data):
    peak_dates = data[data['peak']].index.tolist()
    trough_dates = data[data['trough']].index.tolist()

    events = [(d, 'peak') for d in peak_dates] + [(d, 'trough') for d in trough_dates]
    events.sort()

    uptrends, downtrends = [], []
    for i in range(1, len(events)):
        prev_date, prev_type = events[i - 1]
        curr_date, curr_type = events[i]
        duration = (curr_date - prev_date).days

        if prev_type == 'trough' and curr_type == 'peak':
            uptrends.append(duration)
        elif prev_type == 'peak' and curr_type == 'trough':
            downtrends.append(duration)

    if uptrends:
        print(f"Uptrends: {uptrends}, avg: {sum(uptrends)/len(uptrends):.1f} days")
    else:
        print("No clear uptrends detected in this period.")

    if downtrends:
        print(f"Downtrends: {downtrends}, avg: {sum(downtrends)/len(downtrends):.1f} days")
    else:
        print("No clear downtrends detected in this period.")
    
    last_date, last_type = events[-1]
    
    if last_type == 'peak':
        current_state = "downtrend"
        relevant = downtrends
    else:
        current_state = "uptrend"
        relevant = uptrends
    
    print(f"Currently in: {current_state} (since {last_date.date()})")

    if relevant:
        avg = sum(relevant) / len(relevant)
        lo, hi = min(relevant), max(relevant)
        earliest = last_date + pd.Timedelta(days=lo)
        typical = last_date + pd.Timedelta(days=avg)
        latest = last_date + pd.Timedelta(days=hi)
        print(f"Projected reversal window: {earliest.date()} (earliest seen) "
              f"--> {typical.date()} (typical) --> {latest.date()} (latest seen)")
    else:
        print("Not enough history to project a reversal window for this state.")


def analyze_ticker(symbol):
    symbol = symbol.strip().upper()

    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="180d", interval="4h")
        
    except Exception as e:
        print(f"Couldn't fetch data for {symbol}: {e}")
        return

    if data.empty:
        print(f"No data returned for {symbol} — check the ticker symbol is correct.")
        return
    
    data = find_peaks_and_troughs(data)
    print(f"\n--- Results for {symbol} ---")
    print(f"Price is: ${data['Close'].iloc[-1]:.2f} as of {data.index[-1]}")
    measure_trend_durations(data)


# =============================Entry point ============================= #
if __name__ == "__main__":
    while True:
        symbols = input("What are we analyzing today huh? Give me the ticker symbols and I'll give you some insights!! Or you can press 'q' to quit. Let's go: ")
        if symbols.lower().strip() == 'q':
            break

        if len(symbols) > 0:
            symbol = symbols.split(",")
            for s in symbol:
                s = s.strip()
                if not s:
                    continue
                analyze_ticker(s)
        else:
            print("What are you tring to pull here, MOFO? Give me something, come on!")
    # for symbol in ["TSLA", "URNJ", "SNOW"]:
    #     analyze_ticker(symbol)

