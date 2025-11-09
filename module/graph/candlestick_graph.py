import yfinance as yf
import requests
import numpy as np

def adjust_width_height(data_points):
    if data_points <= 50:
        return 80, 20
    elif data_points <= 100:
        return 100, 25
    elif data_points <= 200:
        return 120, 30
    else:
        # For large datasets, use sampling
        return 150, 35

def get_real_data(symbol, period="5d"):
    """Get real stock data"""
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    width, height = adjust_width_height(len(hist));
    data = []
    for _, row in hist.iterrows():
        data.append([row['Open'], row['High'], row['Low'], row['Close']]);
    return data, width, height


def create_candlestick_chart(data, width=100, height=40):
    """Create ASCII candlestick chart"""
    
    # Extract values
    opens = [d[0] for d in data]
    highs = [d[1] for d in data]
    lows = [d[2] for d in data]
    closes = [d[3] for d in data]
    
    # Calculate chart dimensions
    min_price = min(min(lows), min(opens), min(closes))
    max_price = max(max(highs), max(opens), max(closes))
    price_range = max_price - min_price
    
    # Scale factors
    x_scale = width / len(data)
    y_scale = height / price_range if price_range > 0 else 1
    
    # Initialize chart matrix
    chart = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Draw each candlestick
    for i, (o, h, l, c) in enumerate(zip(opens, highs, lows, closes)):
        x_pos = int(i * x_scale + x_scale / 2)
        
        # Scale prices to chart coordinates
        high_y = int((h - min_price) * y_scale)
        low_y = int((l - min_price) * y_scale)
        open_y = int((o - min_price) * y_scale)
        close_y = int((c - min_price) * y_scale)
        
        # Ensure valid coordinates
        high_y = min(max(high_y, 0), height - 1)
        low_y = min(max(low_y, 0), height - 1)
        open_y = min(max(open_y, 0), height - 1)
        close_y = min(max(close_y, 0), height - 1)
        
        # Draw high-low line
        for y in range(low_y, high_y + 1):
            if 0 <= y < height:
                chart[height - 1 - y][x_pos] = '│'
        
        # Draw body (rectangle between open and close)
        body_top = min(open_y, close_y)
        body_bottom = max(open_y, close_y)
        body_char = '█' if c >= o else '░'  # Filled for up, pattern for down
        
        for y in range(body_top, body_bottom + 1):
            if 0 <= y < height:
                # Draw body with some width
                for dx in [-1, 0, 1]:
                    pos = x_pos + dx
                    if 0 <= pos < width:
                        chart[height - 1 - y][pos] = body_char
    
    return chart, min_price, max_price
    
def print_chart(chart, min_price, max_price, data):
    """Print the chart with labels"""
    
    # Print Y-axis labels
    for i, row in enumerate(chart):
        price = max_price - (i / len(chart) * (max_price - min_price))
        print(f"{price:8.1f} ", end="")
        print(''.join(row))
    
    # Print X-axis
    print(" " * 8 + "─" * len(chart[0]))
    
    # Print some stats
    print(f"\nPrice Range: {min_price:.1f} - {max_price:.1f}")
    print(f"Latest: {data[-1][3]:.1f} " + 
          ("▲" if data[-1][3] >= data[-1][0] else "▼"))

def GRAPH_CANDLESTICK(stock, period):
    data, width, height = get_real_data(stock, period);
    chart, min_price, max_price = create_candlestick_chart(data, width, height);
    print_chart(chart, min_price, max_price, data);
"""
# Main execution
if __name__ == "__main__":
    data, width, height = get_real_data('AAPL', '1mo');#fetch_sample_data()
    chart, min_price, max_price = create_candlestick_chart(data, width, height)
    print("Candlestick Chart:\n")
    print_chart(chart, min_price, max_price, data)
"""
