import marimo

app = marimo.App()


@app.cell
def __():
    import marimo as mo

    return mo


@app.cell
def _(mo):
    mo.md("# Test Marimo application")
    return


if __name__ == "__main__":
    app.run()
