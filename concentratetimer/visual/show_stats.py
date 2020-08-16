import sqlite3
import pandas as pd
from datetime import datetime, date, time, timedelta
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show


def get_week_dates(day_count=7):
    dates = [date.today() - timedelta(days=days) for days in reversed(range(0, day_count))]
    # Convert to week day: .weekday()
    return dates


def get_plotting_df(df, week_para=None):
    """
    week: supply week number, default: this week.

    """
    if week_para is None:
        dates_axis = get_week_dates()
        # print(dates_axis)
        entries_on_day = []
        top = []
        bottom = []
        weekdays = []
        goals = []
        reasons = []

        for i, a_date in enumerate(dates_axis):
            weekdays.append(a_date.weekday())
            df_on_date = df[df['date'] == f"{a_date}"]
            # print(df_on_date.shape[0])
            date_beginning = datetime.combine(a_date, time(9, 0, 0))
            length = df_on_date.shape[0]
            entries_on_day += [i + 1] * length
            start_time_in_seconds = [(datetime.fromtimestamp(int(float(x))) - date_beginning).total_seconds() for x in
                                     df_on_date['start_clock'].values]
            end_time_in_seconds = [(datetime.fromtimestamp(int(float(x))) - date_beginning).total_seconds() for x in
                                   df_on_date['end_clock'].values]
            # start time: top, end_time: bottom
            top += start_time_in_seconds
            bottom += end_time_in_seconds
            goals += list(df_on_date['task_description'].values)
            reasons += list(df_on_date['reason'].values)

        left = [x - 0.5 for x in entries_on_day]
        right = [x + 0.5 for x in entries_on_day]
        data = {'top': top, 'bottom': bottom, 'left': left, 'right': right, "goals": goals, "reasons": reasons}
        return data, weekdays


def plot_timetable(path="./ctimer.db"):
    conn = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM clock_details", conn)
    conn.close()
    output_file('rectangles.html')
    p = figure(plot_width=400, plot_height=400)
    data, weekdays = get_plotting_df(df)
    source = ColumnDataSource(data)
    p.quad(top=data["top"], bottom=data["bottom"], left=data["left"],
           right=data["right"], color="#B3DE69", )

    # Complaints reference fields not match up top, bottom, left, right.
    # p.quad(top=top, bottom=bottom, left=left,
    #       right=right, color="#B3DE69", source=source)
    show(p)
