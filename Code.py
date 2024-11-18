import pandas as pd
import datetime
from typing import List, Dict
import json

class CryptoTransactionAnalyzer:
    def __init__(self):
        self.risk_indicators = {
            'mixing_service': ['tornado.cash', 'wasabi', 'samourai'],
            'high_risk_jurisdictions': ['sanctioned-country-1', 'sanctioned-country-2'],
            'suspicious_patterns': {
                'structuring': 9999,  # Just below 10k threshold
                'velocity': 5,  # Transactions per hour threshold
                'round_amounts': True
            }
        }
    
    def load_transactions(self, filepath: str) -> pd.DataFrame:
        """Load transaction data from JSON file."""
        with open(filepath, 'r') as file:
            data = json.load(file)
        return pd.DataFrame(data)
    
    def analyze_wallet(self, address: str, transactions: pd.DataFrame) -> Dict:
        """Analyze a wallet's transaction patterns."""
        wallet_txs = transactions[
            (transactions['from_address'] == address) | 
            (transactions['to_address'] == address)
        ]
        
        analysis = {
            'address': address,
            'total_transactions': len(wallet_txs),
            'total_volume': wallet_txs['amount'].sum(),
            'risk_indicators': self.check_risk_indicators(wallet_txs),
            'transaction_velocity': self.calculate_velocity(wallet_txs),
            'counterparties': self.analyze_counterparties(address, wallet_txs)
        }
        
        return analysis
    
    def check_risk_indicators(self, transactions: pd.DataFrame) -> List[str]:
        """Check for presence of risk indicators in transactions."""
        risks = []
        
        # Check for mixing service interactions
        for mixer in self.risk_indicators['mixing_service']:
            if mixer in transactions['to_address'].values:
                risks.append(f'Interaction with mixing service: {mixer}')
        
        # Check for structuring patterns
        amounts = transactions['amount']
        if any((amounts > 9900) & (amounts < 10000)):
            risks.append('Potential structuring detected')
        
        # Check for round amounts
        if self.risk_indicators['suspicious_patterns']['round_amounts']:
            if any(amounts.apply(lambda x: x.is_integer())):
                risks.append('Multiple round-number transactions')
        
        return risks
    
    def calculate_velocity(self, transactions: pd.DataFrame) -> Dict:
        """Calculate transaction velocity metrics."""
        if len(transactions) == 0:
            return {'hourly_avg': 0, 'daily_avg': 0}
        
        transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
        time_range = transactions['timestamp'].max() - transactions['timestamp'].min()
        hours = time_range.total_seconds() / 3600
        
        return {
            'hourly_avg': len(transactions) / max(hours, 1),
            'daily_avg': len(transactions) / max(hours/24, 1)
        }
    
    def analyze_counterparties(self, address: str, transactions: pd.DataFrame) -> Dict:
        """Analyze patterns in counterparty interactions."""
        counterparties = []
        
        # Get unique counterparties
        sent_to = transactions[transactions['from_address'] == address]['to_address'].unique()
        received_from = transactions[transactions['to_address'] == address]['from_address'].unique()
        
        return {
            'unique_counterparties': len(set(sent_to) | set(received_from)),
            'top_counterparties': self.get_top_counterparties(address, transactions)
        }
    
    def get_top_counterparties(self, address: str, transactions: pd.DataFrame, top_n: int = 5) -> List[Dict]:
        """Get the top counterparties by transaction volume."""
        counterparty_volumes = {}
        
        for _, tx in transactions.iterrows():
            counterparty = tx['to_address'] if tx['from_address'] == address else tx['from_address']
            counterparty_volumes[counterparty] = counterparty_volumes.get(counterparty, 0) + tx['amount']
        
        return sorted(
            [{'address': k, 'volume': v} for k, v in counterparty_volumes.items()],
            key=lambda x: x['volume'],
            reverse=True
        )[:top_n]
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate a detailed analysis report."""
        report = f"""
Wallet Analysis Report
=====================
Address: {analysis['address']}

Transaction Summary
------------------
Total Transactions: {analysis['total_transactions']}
Total Volume: {analysis['total_volume']} ETH

Risk Indicators
--------------
{chr(10).join(analysis['risk_indicators']) if analysis['risk_indicators'] else 'No risk indicators detected'}

Transaction Velocity
------------------
Hourly Average: {analysis['transaction_velocity']['hourly_avg']:.2f}
Daily Average: {analysis['transaction_velocity']['daily_avg']:.2f}

Counterparty Analysis
--------------------
Unique Counterparties: {analysis['counterparties']['unique_counterparties']}
Top Counterparties by Volume:
{chr(10).join(f"- {cp['address']}: {cp['volume']:.2f} ETH" for cp in analysis['counterparties']['top_counterparties'])}
"""
        return report

def main():
    # Example usage
    analyzer = CryptoTransactionAnalyzer()
    
    # Sample transaction data structure
    sample_data = [
        {
            "timestamp": "2024-01-01T10:00:00",
            "from_address": "0x123...",
            "to_address": "0x456...",
            "amount": 1.5,
            "transaction_hash": "0xabc..."
        }
        # Add more transactions as needed
    ]
    
    # Save sample data
    with open('sample_transactions.json', 'w') as f:
        json.dump(sample_data, f)
    
    # Analyze transactions
    transactions = analyzer.load_transactions('sample_transactions.json')
    analysis = analyzer.analyze_wallet("0x123...", transactions)
    report = analyzer.generate_report(analysis)
    
    print(report)

if __name__ == "__main__":
    main()
