# click_greeter.py
import click

@click.command()
# CLI contract defined via decorators, outside the function body
@click.option(
    "--formal", 
    "-f", 
    is_flag=True, 
    help="Use a formal greeting.",
)
@click.argument("name", type=str)
def greet(name, formal):
    """Greets a person using a simple or formal tone."""
    if formal:
        click.echo(f"Good day, {name}!")
    else:
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    greet()