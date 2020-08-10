import numpy as np;

np.random.seed(sum(map(ord, 'calmap')))
import pandas as pd
import calmap
import matplotlib.pyplot as plt


def random_events():
    """
    We create 500 events as random float values assigned to random days over a
    700-day period.
    """
    all_days = pd.date_range("1/15/2020", periods=1200, freq="4H")
    days = np.random.choice(all_days, 31)
    data = pd.Series(np.random.randn(len(days)), index=days)
    return data


def plot_calmap(events=random_events()):
    calmap.calendarplot(events, monthticks=True, daylabels='MTWTFSS',
                        cmap='YlGn', fillcolor='grey', linewidth=1, vmin=0,
                        fig_kws=dict(figsize=(12, 6)))
    plt.show()

