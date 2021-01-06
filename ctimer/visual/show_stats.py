import sqlite3
from datetime import datetime, date, time, timedelta
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show
import numpy as np
import webbrowser
np.random.seed(sum(map(ord, "calmap")))
import pandas as pd
import calmap
import matplotlib.pyplot as plt
pd.set_option('colheader_justify', 'center')
from shutil import copyfile
import os

# For testing plot_calmap
def _get_random_events():
    """
    We create 500 events as random float values assigned to random days over a
    700-day period.
    """
    all_days = pd.date_range("1/15/2020", periods=1200, freq="4H")
    days = np.random.choice(all_days, 31)
    data = pd.Series(np.random.randn(len(days)), index=days)
    return data


# plot yearly stats
def plot_calmap(events=_get_random_events()):
    # cmap choices: viridis
    calmap.calendarplot(
        events,
        monthticks=True,
        daylabels="MTWTFSS",
        cmap="PuBuGn",
        fillcolor="whitesmoke",
        linewidth=1,
        vmin=0,
        fig_kws=dict(figsize=(12, 6)),
        fig_suptitle="CTimer clock count",
    )

    plt.show()


# plot weekly ctimer stats with bokeh
def _get_plotting_df(df, week_para=None, day_count=7, subset_logic=None):
    """
    week_para: supply week number, default: this week.
    df: whole sqlite table. Including breaks and focus-time
    TODO: plot (1) is_complete clocks (color Green)
               (2) clocks with pauses (color yellowgreen)
               (3) breaks (color blue)
    currently only plotting the (1) and (2) in same color.
    """
    if week_para is None:
        dates_axis = dates = [
            date.today() - timedelta(days=days)
            for days in reversed(range(0, day_count))
        ]
        # print(dates_axis)
        entries_on_day = []
        top = []
        bottom = []
        weekdays = []
        goals = []
        reasons = []

        for i, a_date in enumerate(dates_axis):
            weekdays.append(a_date.weekday())
#            subset_logic = (["is_break"] == 0)
            df = df[df["is_break"] == "0"]
            df_on_date = df[df["date"] == f"{a_date}"]
            # print(df_on_date.shape[0])
            date_beginning = datetime.combine(a_date, time(8, 0, 0))  # start from 8am
            length = df_on_date.shape[0]
            entries_on_day += [i + 1] * length
            start_time_in_seconds = [
                (
                    (
                        datetime.fromtimestamp(int(float(x))) - date_beginning
                    ).total_seconds()
                    / 3600
                )
                for x in df_on_date["start_clock"].values
            ]
            end_time_in_seconds = [
                (
                    (
                        datetime.fromtimestamp(int(float(x))) - date_beginning
                    ).total_seconds()
                    / 3600
                )
                for x in df_on_date["end_clock"].values
            ]
            # start time: top, end_time: bottom
            top += start_time_in_seconds
            bottom += end_time_in_seconds
            goals += list(df_on_date["task_description"].values)
            reasons += list(df_on_date["reason"].values)

        left = [x - 0.5 for x in entries_on_day]
        right = [x + 0.5 for x in entries_on_day]
        data = {
            "top": top,
            "bottom": bottom,
            "left": left,
            "right": right,
            "goals": goals,
            "reasons": reasons,
        }
        return data, weekdays

def quick_view_clocks(path, outpath="/tmp/"):
    conn = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM clock_details", conn)
    conn.close()
    # print clock times
    df_clocks = df[df["is_break"] == "0"].copy()
    df_clocks['Start'] = df_clocks['start_clock'].apply(lambda x:datetime.fromtimestamp(int(float(x))).time())
    df_clocks['End'] = df_clocks['end_clock'].apply(lambda x:datetime.fromtimestamp(int(float(x))).time())
    df_clocks_copy = df_clocks[
        ["date",
         "clock_count",
         "Start",
         "End",
         "is_complete",
         "task_description",
         "reached_bool",
         "reason",
         ]
    ]
    html_string = '''
    <html>
      <head><title>HTML Pandas Dataframe with CSS</title></head>
      <link rel="stylesheet" type="text/css" href="df_style.css"/>
      <body>
        {table}
      </body>
    </html>.
    '''
    css_path = f"{outpath}/ctimer_css_beautify_{date.today()}.html"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    copyfile(f"{dir_path}/df_style.css", f"{outpath}/df_style.css")
    with open(css_path, 'w') as f:
        f.write(html_string.format(table=df_clocks_copy.to_html(classes='mystyle')))
    webbrowser.open(f"file://{css_path}")


def simple_html_df(df_clocks, outpath):
    final_path = f"{outpath}/ctimer_readable_{date.today()}.html"
    df_clocks.to_html(final_path, columns=["date",
                                           "clock_count",
                                           "Start",
                                           "End",
                                           "is_complete",
                                           "task_description",
                                           "reached_bool",
                                           "reason",
                                           ])
    webbrowser.open(f"file://{final_path}")


def plot_timetable(path, outpath):
    conn = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM clock_details", conn)
    conn.close()
    output_file(f"{outpath}/ctimer_weekly_{date.today()}.html")
    data, weekdays = _get_plotting_df(df)
    weekday_num_to_str = {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun",
    }
    p = figure(
        plot_width=400,
        plot_height=400,
        x_range=[0, 8],
        y_range=[17, 0],
        title="Your weekly ctimer",
    )
    p.xaxis.ticker = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    xlabels = {0: "", 8: ""}
    for i, num in enumerate(weekdays, 1):
        xlabels[i] = weekday_num_to_str[num]
    p.xaxis.major_label_overrides = xlabels
    p.yaxis.ticker = [17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    p.yaxis.major_label_overrides = {
        0: "8:00am",
        1: "9:00am",
        2: "10:00am",
        3: "11:00am",
        4: "12:00pm",
        5: "1:00pm",
        6: "2:00pm",
        7: "3:00pm",
        8: "4:00pm",
        9: "5:00pm",
        10: "6:00pm",
        11: "7:00pm",
        12: "8:00pm",
        13: "9:00pm",
        14: "10:00pm",
        15: "11:00pm",
        16: "12:00am",
        17: "1:00am",
    }

    source = ColumnDataSource(data)
    p.quad(
        top=data["top"],
        bottom=data["bottom"],
        left=data["left"],
        right=data["right"],
        color="#8ed7e6",
    )

    # Complaints reference fields not match up top, bottom, left, right.
    # p.quad(top=top, bottom=bottom, left=left,
    #       right=right, color="#B3DE69", source=source)
    show(p)
