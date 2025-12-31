# typer_greeter.py
import typer
from typing_extensions import Annotated 

app = typer.Typer()

@app.command()
def greet(
    # CLI contract defined inside the function signature
    name: Annotated[str, typer.Argument(help="The person to greet.")],
    formal: Annotated[
        bool, 
        typer.Option("--formal", "-f", help="Use a formal greeting.")
    ] = False,
):
    """Greets a person using a simple or formal tone."""
    if formal:
        print(f"Good day, {name}!")
    else:
        print(f"Hello, {name}!")

if __name__ == "__main__":
    app()