# Crypto Transaction Analyzer 🔍

A Python-based tool for analyzing cryptocurrency transactions and detecting potentially suspicious patterns. 

## 🚀 Features

- Transaction pattern analysis across wallets
- Risk indicator detection:
  - Interaction with mixing services
  - Structuring patterns
  - Round-amount transactions
  - High-velocity trading
- Counterparty analysis and relationship mapping
- Detailed report generation
- Support for custom risk thresholds

## 💻 Tech Stack

- Python 3.8+
- Pandas for data processing
- JSON for data storage

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto-transaction-analyzer.git
cd crypto-transaction-analyzer
```

2. Install dependencies:
```bash
pip install pandas
```

## 📊 Usage

1. Prepare your transaction data in JSON format:
```json
[
    {
        "timestamp": "2024-01-01T10:00:00",
        "from_address": "0x123...",
        "to_address": "0x456...",
        "amount": 1.5,
        "transaction_hash": "0xabc..."
    }
]
```

2. Run the analyzer:
```python
from crypto_analyzer import CryptoTransactionAnalyzer

analyzer = CryptoTransactionAnalyzer()
transactions = analyzer.load_transactions('your_transactions.json')
analysis = analyzer.analyze_wallet("target_address", transactions)
report = analyzer.generate_report(analysis)
print(report)
```

## 📈 Example Output

```
Wallet Analysis Report
=====================
Address: 0x123...

Transaction Summary
------------------
Total Transactions: 50
Total Volume: 125.5 ETH

Risk Indicators
--------------
- Interaction with mixing service: tornado.cash
- Multiple round-number transactions

[...]
```



## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Feel free to submit issues and pull requests.

