Description:

Developed a fully automated trading strategy that processes minute-level stock market data for NIFTY 50, identifies breakout trades based on the first 15-minute high and low levels, and applies dynamic stop-loss (0.5%) and take-profit (1%) to manage risk and reward. The strategy evaluates monthly and yearly PnL performance to determine profitability.

Technologies:

Python, Pandas, NumPy, CSV, Data Analysis, Algorithmic Trading.

Key Contributions:

  •	Data Processing: Cleaned, structured, and sorted minute-level stock market data to extract key trading windows.
	•	Signal Generation: Implemented a rule-based breakout strategy to trigger buy/sell signals after the first 15-minute range.
	•	Risk Management: Integrated dynamic stop-loss (0.25%) and take-profit (0.5%) levels for automated exits.
	•	Performance Evaluation: Computed PnL metrics on a daily, monthly, and yearly basis to assess strategy profitability.
	•	Optimized Execution: Leveraged Pandas vectorized operations for efficient data processing.
	•	Data Export & Reporting: Automated CSV generation for trade logs, signals, and performance metrics.
