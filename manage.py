import typer
from fastapi_migrations.cli import MigrationsCli

app: typer.Typer = typer.Typer()

app.add_typer(MigrationsCli())

if __name__ == '__main__':
    app()
