import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
from scipy import stats
import os
import warnings

warnings.filterwarnings("ignore")

# ============================================================
# ✅ PATH HANDLING — Works in .py AND Jupyter Notebook
# ============================================================

def get_base_dir():
    """Return the base directory of the project, notebook-safe."""
    try:
        # Running as a .py file
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # Running inside a notebook
        return os.getcwd()

BASE_DIR = get_base_dir()

DATA_RAW = os.path.join(BASE_DIR, "..", "data", "raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "..", "data", "processed")
RESULTS_DIR = os.path.join(BASE_DIR, "..", "data", "processed", "metrics")

os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# ✅ DATA LOADING FUNCTIONS
# ============================================================

def load_prices():
    """Load raw sp500 prices."""
    path = os.path.join(DATA_RAW, "sp500_prices.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df

def load_returns():
    """Load processed sp500 returns."""
    path = os.path.join(DATA_PROCESSED, "sp500_returns.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df.dropna()

def load_metrics():
    """Load processed sp500 metrics."""
    path = os.path.join(DATA_PROCESSED, "sp500_metrics.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    df = pd.read_csv(path, index_col=0)
    return df

# ============================================================
# ✅ PortfolioRiskAnalyzer
# ============================================================

class PortfolioRiskAnalyzer:
    def __init__(self, returns, weights=None):
        self.returns = returns
        if weights is None:
            self.weights = np.ones(len(returns.columns)) / len(returns.columns)
        else:
            self.weights = np.array(weights)

        self.portfolio_returns = returns @ self.weights

    def calculate_var(self, confidence_level=0.95):
        return np.percentile(self.portfolio_returns, (1 - confidence_level) * 100)

    def calculate_cvar(self, confidence_level=0.95):
        var = self.calculate_var(confidence_level)
        return self.portfolio_returns[self.portfolio_returns <= var].mean()

    def calculate_maximum_drawdown(self):
        cumulative = (1 + self.portfolio_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max

        max_dd = drawdown.min()
        max_dd_date = drawdown.idxmin()

        dd_series = drawdown[drawdown < 0]
        if len(dd_series) > 0:
            dd_groups = (dd_series == 0).cumsum()
            durations = dd_groups.value_counts()
            max_duration = durations.max()
        else:
            max_duration = 0

        return {
            "max_drawdown": max_dd,
            "max_drawdown_date": max_dd_date,
            "max_duration_days": max_duration,
            "drawdown_series": drawdown,
        }

    def calculate_downside_deviation(self, mar=0.0):
        downside_returns = self.portfolio_returns[self.portfolio_returns < mar]
        return np.sqrt(np.mean(downside_returns ** 2))

    def calculate_sortino_ratio(self, risk_free_rate=0.02, periods=252):
        excess_return = self.portfolio_returns.mean() * periods - risk_free_rate
        downside_dev = self.calculate_downside_deviation() * np.sqrt(periods)
        return excess_return / downside_dev if downside_dev > 0 else 0

    def calculate_calmar_ratio(self, periods=252):
        annual_return = self.portfolio_returns.mean() * periods
        max_dd = abs(self.calculate_maximum_drawdown()["max_drawdown"])
        return annual_return / max_dd if max_dd > 0 else 0

    def calculate_sharpe_ratio(self, risk_free_rate=0.02, periods=252):
        excess_return = self.portfolio_returns.mean() * periods - risk_free_rate
        volatility = self.portfolio_returns.std() * np.sqrt(periods)
        return excess_return / volatility if volatility > 0 else 0

    def calculate_tail_ratio(self):
        return abs(
            np.percentile(self.portfolio_returns, 95)
            / np.percentile(self.portfolio_returns, 5)
        )

    def calculate_skewness(self):
        return stats.skew(self.portfolio_returns)

    def calculate_kurtosis(self):
        return stats.kurtosis(self.portfolio_returns)

    def get_risk_metrics(self):
        dd_info = self.calculate_maximum_drawdown()

        return {
            "Annual Return": self.portfolio_returns.mean() * 252,
            "Annual Volatility": self.portfolio_returns.std() * np.sqrt(252),
            "Sharpe Ratio": self.calculate_sharpe_ratio(),
            "Sortino Ratio": self.calculate_sortino_ratio(),
            "Calmar Ratio": self.calculate_calmar_ratio(),
            "Max Drawdown": dd_info["max_drawdown"],
            "Max Drawdown Duration": dd_info["max_duration_days"],
            "VaR (95%)": self.calculate_var(0.95),
            "CVaR (95%)": self.calculate_cvar(0.95),
            "Downside Deviation": self.calculate_downside_deviation() * np.sqrt(252),
            "Skewness": self.calculate_skewness(),
            "Kurtosis": self.calculate_kurtosis(),
            "Tail Ratio": self.calculate_tail_ratio(),
        }

# ============================================================
# ✅ PortfolioBacktester
# ============================================================

class PortfolioBacktester:
    def __init__(self, returns_data, lookback_years=3, rebalance_frequency="Q"):
        self.returns_data = returns_data
        self.lookback_days = lookback_years * 252
        self.rebalance_frequency = rebalance_frequency

    def optimize_portfolio(self, returns_train, method="max_sharpe", risk_free_rate=0.02):
        n_assets = len(returns_train.columns)
        mean_returns = returns_train.mean() * 252
        cov_matrix = returns_train.cov() * 252

        def portfolio_volatility(weights):
            return np.sqrt(weights.T @ cov_matrix @ weights)

        def neg_sharpe(weights):
            ret = weights @ mean_returns
            vol = np.sqrt(weights.T @ cov_matrix @ weights)
            return -(ret - risk_free_rate) / vol if vol > 0 else 999

        if method == "max_sharpe":
            objective = neg_sharpe
        elif method == "min_variance":
            objective = portfolio_volatility
        elif method == "max_return":
            objective = lambda w: -(w @ mean_returns)
        else:
            objective = neg_sharpe

        constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
        bounds = tuple((0, 0.10) for _ in range(n_assets))
        w0 = np.array([1 / n_assets] * n_assets)

        result = minimize(
            objective,
            w0,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
            options={"maxiter": 1000},
        )

        return result.x if result.success else w0

    def calculate_transaction_costs(self, old_weights, new_weights, portfolio_value, cost_rate=0.001):
        turnover = np.sum(np.abs(new_weights - old_weights))
        return turnover * portfolio_value * cost_rate

    def backtest(self, strategy="max_sharpe", include_costs=True):
        if self.rebalance_frequency == "M":
            freq = "MS"
        elif self.rebalance_frequency == "Q":
            freq = "QS"
        else:
            freq = "YS"

        rebalance_dates = pd.date_range(
            self.returns_data.index[self.lookback_days],
            self.returns_data.index[-1],
            freq=freq,
        )

        portfolio_value = 100000
        portfolio_values = []
        all_weights = []
        rebalance_info = []
        current_weights = None

        for i, rebal_date in enumerate(rebalance_dates):
            # Use nearest trading day instead of exact match
            train_end_idx = self.returns_data.index.get_indexer([rebal_date], method="nearest")[0]
            train_start_idx = max(0, train_end_idx - self.lookback_days)
            returns_train = self.returns_data.iloc[train_start_idx:train_end_idx]

            new_weights = self.optimize_portfolio(returns_train, method=strategy)

            if include_costs and current_weights is not None:
                cost = self.calculate_transaction_costs(current_weights, new_weights, portfolio_value)
                portfolio_value -= cost
            else:
                cost = 0

            next_rebal = (
                rebalance_dates[i + 1]
                if i < len(rebalance_dates) - 1
                else self.returns_data.index[-1]
            )

            period_returns = self.returns_data[
                (self.returns_data.index >= rebal_date)
                & (self.returns_data.index < next_rebal)
            ]

            for date, daily_returns in period_returns.iterrows():
                portfolio_return = np.dot(new_weights, daily_returns.values)
                portfolio_value *= (1 + portfolio_return)
                portfolio_values.append(
                    {"date": date, "value": portfolio_value, "return": portfolio_return}
                )

            rebalance_info.append(
                {
                    "date": rebal_date,
                    "weights": new_weights.copy(),
                    "cost": cost,
                    "portfolio_value": portfolio_value,
                }
            )

            all_weights.append(new_weights)
            current_weights = new_weights.copy()

        results_df = pd.DataFrame(portfolio_values).set_index("date")

        returns_series = pd.Series(
            [x["return"] for x in portfolio_values],
            index=[x["date"] for x in portfolio_values],
        )

        risk_analyzer = PortfolioRiskAnalyzer(
            self.returns_data.loc[results_df.index], weights=current_weights
        )
        risk_analyzer.portfolio_returns = returns_series

        metrics = risk_analyzer.get_risk_metrics()
        metrics["Total Return"] = (portfolio_value - 100000) / 100000
        metrics["CAGR"] = (portfolio_value / 100000) ** (252 / len(results_df)) - 1

        return {
            "portfolio_values": results_df,
            "returns": returns_series,
            "weights_history": all_weights,
            "rebalance_info": rebalance_info,
            "metrics": metrics,
            "final_weights": current_weights,
        }