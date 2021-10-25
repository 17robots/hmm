import pandas as pd
import click

@click.command()
@click.argument()
@click.argument()
@click.argument()
def func():
    ...

if __name__ == '__main__':
    print('Hello World')
