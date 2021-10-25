import pandas as pd
import click

@click.command()
@click.argument("filename")
# @click.argument()
# @click.argument()
def func(filename):
    # read in the steps
    try
        pd.readCSV(filename)
    except:
        print('Failed to open file')

if __name__ == '__main__':
    func()
