import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    from datetime import date

    import marimo as mo
    import matplotlib.pyplot as plt
    import polars as pl

    return date, mo, pl, plt


@app.cell
def _(mo):
    mo.md("""
    # Website traffic dashboard

    Adjust the date window and rolling average to inspect traffic patterns.
    """)
    return


@app.cell
def _(date, pl):
    dates = pl.date_range(
        start=date(2025, 1, 1),
        end=date(2025, 3, 31),
        interval="1d",
        eager=True,
    )
    traffic = pl.DataFrame(
        {
            "date": dates,
            "visits": [900 + (index * 83) % 700 for index in range(len(dates))],
            "device": [
                ["Desktop", "Mobile", "Tablet"][index % 3]
                for index in range(len(dates))
            ],
        }
    )
    return (traffic,)


@app.cell
def _(mo):
    days = mo.ui.slider(start=14, stop=90, value=60, step=1, label="Days to display")
    rolling_window = mo.ui.slider(
        start=1, stop=14, value=7, step=1, label="Rolling average window"
    )
    mo.vstack([days, rolling_window])
    return days, rolling_window


@app.cell
def _(days, pl, rolling_window, traffic):
    visible_traffic = traffic.tail(days.value).with_columns(
        pl.col("visits")
        .rolling_mean(window_size=rolling_window.value)
        .alias("rolling_visits")
    )
    return (visible_traffic,)


@app.cell
def _(mo, visible_traffic):
    mo.md(f"""
    Average visits: **{visible_traffic['visits'].mean():,.0f}** | "
        f"Peak visits: **{visible_traffic['visits'].max():,.0f}**
    """)
    return


@app.cell
def _(plt, rolling_window, visible_traffic):
    figure, axis = plt.subplots(figsize=(8, 4))
    axis.plot(visible_traffic["date"], visible_traffic["visits"], alpha=0.35, label="Daily")
    axis.plot(
        visible_traffic["date"],
        visible_traffic["rolling_visits"],
        linewidth=2,
        label=f"{rolling_window.value}-day average",
    )
    axis.set(title="Website visits", xlabel="Date", ylabel="Visits")
    axis.legend()
    axis.grid(alpha=0.25)
    figure.autofmt_xdate()
    figure.tight_layout()
    figure
    return


@app.cell
def _(pl, plt, traffic):
    device_totals = traffic.group_by("device").agg(pl.col("visits").sum().alias("visits"))
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.pie(device_totals["visits"], labels=device_totals["device"], autopct="%1.0f%%")
    axis.set_title("Visits by device")
    figure.tight_layout()
    figure
    return


if __name__ == "__main__":
    app.run()
