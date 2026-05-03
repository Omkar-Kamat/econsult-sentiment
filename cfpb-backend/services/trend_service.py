from __future__ import annotations
import pandas as pd
import numpy as np
from shared.loader import ARTIFACTS, CLUSTER_LABELS

ANOMALY_SIGMA  = 2.0
MIN_MONTH_SIZE = 50


def _build_monthly(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Aggregate the severity_data df into monthly cluster-share series."""
    if "date_received" not in df.columns:
        raise ValueError(
            "severity_data.csv is missing 'date_received'. "
            "Re-run NB09 after attaching timestamps."
        )

    df = df.copy()
    df["date_received"] = pd.to_datetime(df["date_received"], errors="coerce")
    df["month"]         = df["date_received"].dt.to_period("M")
    df = df.dropna(subset=["month"])

    monthly = (
        df.groupby(["month", "cluster"])
        .size()
        .unstack(fill_value=0)
    )
    totals = monthly.sum(axis=1)
    valid  = totals[totals >= MIN_MONTH_SIZE].index
    monthly = monthly.loc[valid]
    totals  = totals.loc[valid]

    monthly_pct = monthly.div(totals, axis=0) * 100
    return monthly_pct, totals


def get_trends(months: int | None = None, cluster: int | None = None) -> dict:
    """Return monthly cluster share time-series with anomaly flags."""
    df            = ARTIFACTS["df"]
    monthly_pct, totals = _build_monthly(df)

    if months:
        monthly_pct = monthly_pct.iloc[-months:]
        totals      = totals.iloc[-months:]

    clusters_to_return = (
        [cluster] if cluster is not None
        else sorted(monthly_pct.columns.tolist())
    )

    data_points = []
    anomalies   = []

    for c in clusters_to_return:
        if c not in monthly_pct.columns:
            continue

        series = monthly_pct[c]
        mu     = series.mean()
        sigma  = series.std()
        if pd.isna(sigma) or sigma == 0.0:   # ← FIX: handles n=1 and constant series
            sigma = 1.0

        for month, value in series.items():
            z = float((value - mu) / sigma)
            is_anomaly = abs(z) > ANOMALY_SIGMA
            point = {
                "month":            str(month),
                "cluster":          int(c),
                "cluster_label":    CLUSTER_LABELS.get(int(c), f"Cluster {c}"),
                "share_pct":        round(float(value), 2),
                "total_complaints": int(totals.get(month, 0)),
                "is_anomaly":       is_anomaly,
                "z_score":          round(z, 3),
            }
            data_points.append(point)
            if is_anomaly:
                anomalies.append(point)

    return {
        "months_analysed": len(monthly_pct),
        "data":            data_points,
        "anomalies":       anomalies,
    }