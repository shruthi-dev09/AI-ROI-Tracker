import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_roi_data(rows=500):
    features = {
        'AI_Support_Bot': {'cost_per_1k': 0.02, 'mins_saved_avg': 10, 'labor_rate': 25},
        'AI_Code_Refactor': {'cost_per_1k': 0.03, 'mins_saved_avg': 20, 'labor_rate': 60},
        'AI_Email_Composer': {'cost_per_1k': 0.01, 'mins_saved_avg': 5, 'labor_rate': 30}
    }
    
    data = []
    for _ in range(rows):
        f_name = np.random.choice(list(features.keys()))
        meta = features[f_name]
        
        tokens = np.random.randint(500, 4000)
        cost = (tokens / 1000) * meta['cost_per_1k']
        time_saved = np.random.normal(meta['mins_saved_avg'], 2)
        
        data.append({
            'timestamp': datetime.now() - timedelta(days=np.random.randint(0, 30)),
            'feature_name': f_name,
            'tokens_used': tokens,
            'api_cost_usd': round(cost, 4),
            'manual_time_saved_mins': round(time_saved, 2),
            'hourly_labor_rate': meta['labor_rate']
        })
        
    df = pd.DataFrame(data)
    df.to_csv('ai_feature_logs.csv', index=False)
    print("Dataset 'ai_feature_logs.csv' generated successfully!")

generate_roi_data()