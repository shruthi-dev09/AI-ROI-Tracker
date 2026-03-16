import pandas as pd
import matplotlib.pyplot as plt

class AIRoITracker:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def calculate_metrics(self):
        # 1. Calculate Human Labor Cost Saved ($)
        # Formula: (Minutes Saved / 60) * Hourly Rate
        self.df['labor_savings_usd'] = (self.df['manual_time_saved_mins'] / 60) * self.df['hourly_labor_rate']

        # 2. Calculate Net Profit per call
        self.df['net_savings'] = self.df['labor_savings_usd'] - self.df['api_cost_usd']

        return self.df

    def get_feature_report(self):
        self.calculate_metrics()

        # Aggregate data by feature
        report = self.df.groupby('feature_name').agg({
            'api_cost_usd': 'sum',
            'labor_savings_usd': 'sum',
            'net_savings': 'sum',
            'tokens_used': 'mean'
        }).reset_index()

        # Calculate Percentage ROI
        report['ROI_percent'] = (report['net_savings'] / report['api_cost_usd']) * 100

        # Rounding for clean display
        return report.round(2).sort_values(by='ROI_percent', ascending=False)

# Execution with Visualization
tracker = AIRoITracker('ai_feature_logs.csv')
roi_report = tracker.get_feature_report()

print("--- Cleaned Feature-Level AI ROI Report ---")
print(roi_report)

# Generate a Chart for GitHub
plt.figure(figsize=(10, 6))
plt.bar(roi_report['feature_name'], roi_report['ROI_percent'], color=['#4CAF50', '#2196F3', '#FF9800'])
plt.xlabel('AI Feature')
plt.ylabel('ROI Percentage (%)')
plt.title('Return on Investment per AI Feature')
plt.savefig('roi_chart.png')  # This saves a picture you can put in your README
print("\nSuccess! 'roi_chart.png' has been saved to your folder.")