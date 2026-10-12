"""The data of version 1 and the transformations used in version 2.

data/usd_credit_tufe_ito.xlsx, sheet EVDS, holds 127 monthly observations, March 2014 to September 2024:
  credit  bank and credit card spending, thousand TRY (as described in version 1)
  usd     weighted average interest rate on USD commercial loans, percent
  tufe    consumer price index, 2003 = 100
  ito     price index of the Istanbul Chamber of Commerce (not used in version 1)

Author: Muhammed Ikbal Yilmaz
"""

import calendar
from pathlib import Path

import numpy as np
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "usd_credit_tufe_ito.xlsx"


def load(path=DATA_FILE):
    """The four series with a monthly DatetimeIndex (first day of the month)."""
    df = pd.read_excel(path, sheet_name="EVDS").dropna(how="all")
    df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y-%m")
    df = df.set_index("date").astype(float)
    expected = pd.date_range(df.index[0], df.index[-1], freq="MS")
    if not df.index.equals(expected):
        raise ValueError("the months in the data file are not consecutive")
    return df


def weekday_count(index, weekday):
    """Number of times a weekday (Monday = 0, ..., Friday = 4) occurs in each month of a monthly index."""
    return pd.Series([sum(1 for d in range(1, calendar.monthrange(t.year, t.month)[1] + 1)
                          if calendar.weekday(t.year, t.month, d) == weekday) for t in index], index=index)


def fridays(index):
    return weekday_count(index, 4)


def transformed(df):
    """The series analysed in version 2.

    log_credit_weekly : log of credit divided by the number of Fridays in the month (average per week)
    log_credit_real   : the same, deflated by the consumer price index
    usd               : unchanged (an interest rate)
    log_tufe, log_ito : logs of the two price indices
    """
    per_week = df["credit"] / fridays(df.index)
    return pd.DataFrame({
        "log_credit_weekly": np.log(per_week),
        "log_credit_real": np.log(per_week / df["tufe"]),
        "usd": df["usd"],
        "log_tufe": np.log(df["tufe"]),
        "log_ito": np.log(df["ito"]),
    })
