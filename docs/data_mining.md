## Data Mining

### Definition

Data mining is the process of discovering patterns, correlations, anomalies, and useful information from large datasets using computational and statistical techniques. It combines methods from statistics, machine learning, database systems, and pattern recognition to extract actionable knowledge from data (Han et al., 2011). Data mining transforms raw data into useful information for decision-making.

### Core Process: CRISP-DM Framework

The Cross-Industry Standard Process for Data Mining (CRISP-DM) provides a structured approach:

1. **Business Understanding**
   - Define project objectives and requirements
   - Translate business questions into data mining goals
   - Develop preliminary project plan

2. **Data Understanding**
   - Collect initial data
   - Perform exploratory analysis
   - Assess data quality
   - Identify interesting subsets

3. **Data Preparation**
   - Select relevant data
   - Clean and transform data
   - Construct new features
   - Format data for modeling

4. **Modeling**
   - Select appropriate modeling techniques
   - Build and calibrate models
   - Test multiple algorithms
   - Optimize parameters

5. **Evaluation**
   - Assess model quality and validity
   - Review process to ensure business objectives are met
   - Determine if important issues have been overlooked

6. **Deployment**
   - Plan deployment and monitoring
   - Produce final reports
   - Implement models in production
   - Establish maintenance procedures

### Key Techniques

**Pattern Discovery:**
- Association rule mining (market basket analysis)
- Sequential pattern mining
- Frequent pattern mining (Apriori, FP-Growth algorithms)

**Classification:**
- Decision trees (C4.5, CART)
- Naive Bayes classifiers
- Support vector machines
- k-Nearest Neighbors

**Clustering:**
- K-means clustering
- Hierarchical clustering
- DBSCAN (Density-Based Spatial Clustering)
- Gaussian Mixture Models

**Anomaly Detection:**
- Statistical methods
- Distance-based approaches
- Isolation forests
- One-class SVM

**Regression:**
- Linear regression
- Polynomial regression
- Ridge and Lasso regression

### Practical Example: Association Rule Mining

```python
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

# Sample transaction data
data = {
    'TransactionID': [1, 2, 3, 4, 5],
    'Bread': [1, 1, 0, 1, 0],
    'Milk': [1, 1, 1, 1, 0],
    'Eggs': [0, 1, 1, 1, 1],
    'Butter': [1, 0, 0, 1, 0]
}

df = pd.DataFrame(data).set_index('TransactionID')

# Find frequent itemsets
frequent_itemsets = apriori(df, min_support=0.4, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)

# Display rules
print("Association Rules:")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# Interpretation:
# Support: How frequently the itemset appears
# Confidence: Likelihood of consequent given antecedent
# Lift: How much more likely consequent is when antecedent is present
```

### Example: Customer Segmentation with K-Means

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Prepare customer data
customer_features = df[['purchase_frequency', 'avg_transaction_value', 'recency']]

# Standardize features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(customer_features)

# Determine optimal number of clusters (elbow method)
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)
    inertias.append(kmeans.inertia_)

# Apply K-means
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(scaled_features)
df['cluster'] = clusters

# Analyze cluster characteristics
print(df.groupby('cluster').mean())
```

### Applications

- Customer segmentation and targeting
- Fraud detection in financial transactions
- Market basket analysis for retail
- Healthcare diagnosis and treatment optimization
- Predictive maintenance in manufacturing
- Social network analysis
- Web usage mining and recommendation systems

---
