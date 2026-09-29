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
    # Sales dashboard

    Explore synthetic sales data with the controls below.
    """)
    return


@app.cell
def _(date, pl):
    dates = pl.date_range(
        start=date(2023, 1, 1),
        end=date(2025, 12, 31),
        interval="1d",
        eager=True,
    )
    categories = ["Books", "Games", "Music", "Tools"]
    sales = pl.DataFrame(
        {
            "date": dates,
            "category": [categories[index % len(categories)] for index in range(len(dates))],
            "revenue": [120 + (index * 17) % 280 for index in range(len(dates))],
            "orders": [8 + (index * 5) % 34 for index in range(len(dates))],
        }
    ).with_columns(pl.col("date").dt.year().alias("year"))
    return (sales,)


@app.cell
def _(mo):
    year = mo.ui.slider(start=2023, stop=2025, value=2025, step=1, label="Year")
    category = mo.ui.slider(start=0, stop=3, value=0, step=1, label="Category index")
    mo.vstack([year, category])
    return category, year


@app.cell
def _(category, pl, sales, year):
    selected_categories = ["Books", "Games", "Music", "Tools"]
    selected_category = selected_categories[int(category.value)]
    filtered_sales = sales.filter(
        (pl.col("year") == year.value) & (pl.col("category") == selected_category)
    )
    return filtered_sales, selected_category


@app.cell
def _(filtered_sales, mo, selected_category, year):
    mo.md(f"""
    **{selected_category}** in **{year.value}**: "
        f"{filtered_sales.height} daily records
    """)
    return


@app.cell
def _(filtered_sales, pl, plt):
    monthly = filtered_sales.group_by(pl.col("date").dt.month().alias("month")).agg(
        pl.col("revenue").sum().alias("revenue")
    ).sort("month")
    figure, axis = plt.subplots(figsize=(8, 4))
    axis.plot(monthly["month"], monthly["revenue"], marker="o")
    axis.set(title="Monthly revenue", xlabel="Month", ylabel="Revenue")
    axis.grid(alpha=0.25)
    figure.tight_layout()
    figure
    return


@app.cell
def _(pl, plt, sales, year):
    category_totals = (
        sales.filter(pl.col("year") == year.value)
        .group_by("category")
        .agg(pl.col("revenue").sum().alias("revenue"))
        .sort("revenue", descending=True)
    )
    figure, axis = plt.subplots(figsize=(8, 4))
    axis.bar(category_totals["category"], category_totals["revenue"])
    axis.set(title=f"Revenue by category in {year.value}", ylabel="Revenue")
    figure.tight_layout()
    figure
    return


if __name__ == "__main__":
    app.run()
