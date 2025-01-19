import pandas as pd

# Load the data
file_path = '/Users/Dhyanam/Downloads/archive/NIFTY 50_minute.csv'
data = pd.read_csv(file_path)

# Ensure correct datetime format and sort by timestamp
data['Datetime'] = pd.to_datetime(data['date'], format='mixed')
data = data.sort_values(by='Datetime')

# Create a column for date to separate each day's data
data['Date'] = data['Datetime'].dt.date

# Filter data between 09:15 and 09:30 for each day
data['Time'] = data['Datetime'].dt.time
data_15min = data[(data['Time'] >= pd.to_datetime("09:15").time()) & (data['Time'] <= pd.to_datetime("09:30").time())]

# Calculate 15-minute high and low between 09:15 and 09:30
high_low_result = data_15min.groupby('Date').agg({
    'high': 'max',
    'low': 'min'
}).reset_index()
high_low_result.rename(columns={'high': '15min_high', 'low': '15min_low'}, inplace=True)

# Merge the 15-minute high-low data back to the original data
data = pd.merge(data, high_low_result, on='Date', how='left')

# Initialize columns for signals and exits
data['Signal'] = None
data['Exit'] = None
data['Trade Price'] = None

def generate_signals_and_exits(data):
    trade_executed = set()  # To track if a trade has been executed for a day

    for idx, row in data.iterrows():
        if row['Time'] > pd.to_datetime("09:30").time() and row['Date'] not in trade_executed:
            if row['high'] > row['15min_high']:
                trade_price = row['high']
                stop_loss = trade_price * (1 - 0.005)  # 0.25% SL
                target_price = trade_price * (1 + 0.005)  # 0.5% TP

                data.at[idx, 'Signal'] = 'Buy'
                data.at[idx, 'Trade Price'] = trade_price
                trade_executed.add(row['Date'])

                # Apply exit conditions for Buy
                exit_triggered = False
                for i in range(idx + 1, len(data)):
                    if data.at[i, 'Date'] != row['Date']:
                        break
                    if data.at[i, 'low'] <= stop_loss:
                        data.at[i, 'Exit'] = f'Stop Loss at {stop_loss:.2f}'
                        exit_triggered = True
                        break
                    if data.at[i, 'high'] >= target_price:
                        data.at[i, 'Exit'] = f'Take Profit at {target_price:.2f}'
                        exit_triggered = True
                        break

                # End-of-day exit
                if not exit_triggered:
                    for j in range(idx + 1, len(data)):
                        if data.at[j, 'Time'] == pd.to_datetime("15:29").time() and data.at[j, 'Date'] == row['Date']:
                            close_price = data.at[j, 'close']
                            exit_type = "Take Profit" if close_price >= trade_price else "Stop Loss"
                            data.at[j, 'Exit'] = f'{exit_type} at {close_price:.2f}'
                            break

            elif row['low'] < row['15min_low']:
                trade_price = row['low']
                stop_loss = trade_price * (1 + 0.005)  # 0.25% SL
                target_price = trade_price * (1 - 0.005)  # 0.5% TP

                data.at[idx, 'Signal'] = 'Sell'
                data.at[idx, 'Trade Price'] = trade_price
                trade_executed.add(row['Date'])

                # Apply exit conditions for Sell
                exit_triggered = False
                for i in range(idx + 1, len(data)):
                    if data.at[i, 'Date'] != row['Date']:
                        break
                    if data.at[i, 'high'] >= stop_loss:
                        data.at[i, 'Exit'] = f'Stop Loss at {stop_loss:.2f}'
                        exit_triggered = True
                        break
                    if data.at[i, 'low'] <= target_price:
                        data.at[i, 'Exit'] = f'Take Profit at {target_price:.2f}'
                        exit_triggered = True
                        break

                # End-of-day exit
                if not exit_triggered:
                    for j in range(idx + 1, len(data)):
                        if data.at[j, 'Time'] == pd.to_datetime("15:29").time() and data.at[j, 'Date'] == row['Date']:
                            close_price = data.at[j, 'close']
                            exit_type = "Take Profit" if close_price < trade_price else "Stop Loss"
                            data.at[j, 'Exit'] = f'{exit_type} at {close_price:.2f}'
                            break

    return data

data = generate_signals_and_exits(data)

# Calculate win/loss metrics
exit_conditions = data.dropna(subset=['Exit'])

# Extract trade outcomes
exit_conditions['Outcome'] = exit_conditions['Exit'].apply(lambda x: 'Win' if 'Take Profit' in x else ('Loss' if 'Stop Loss' in x else 'End of Day'))

# Calculate win and loss counts
win_count = exit_conditions['Outcome'].value_counts().get('Win', 0)
loss_count = exit_conditions['Outcome'].value_counts().get('Loss', 0)
total_trades = win_count + loss_count

# Calculate win and loss percentages
win_percentage = (win_count / total_trades) * 100 if total_trades > 0 else 0
loss_percentage = (loss_count / total_trades) * 100 if total_trades > 0 else 0

print(f"Total Wins: {win_count}")
print(f"Total Losses: {loss_count}")
print(f"Win Percentage: {win_percentage:.2f}%")
print(f"Loss Percentage: {loss_percentage:.2f}%")

# Save the result to a new CSV file
output_file_path = '/Users/Dhyanam/Downloads/archive/15min_signals_with_exits_dynamic_SL_TP.csv'
data.to_csv(output_file_path, index=False)

print(f"Signals, exits, and performance metrics have been saved to {output_file_path}")