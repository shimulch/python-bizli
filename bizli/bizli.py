import typer
import os

app = typer.Typer()


@app.command()
def hello(name: str):
    cwd = os.getcwd()
    typer.echo(f'{name}')
