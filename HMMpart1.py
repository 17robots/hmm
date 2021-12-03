import pandas as pd
import click
import math
from scipy.stats import norm

def dist(x1, y1, x2, y2):
    return math.sqrt(pow((x1-x2),2) + pow((y1-y2),2))

@click.command()
@click.argument("filename")
@click.argument("iterations", type=int)
def func(filename, iterations):
    # read in the steps
    steps: pd.DataFrame
    try:
        steps = pd.read_csv(filename)
    except Exception as e:
        print('Failed to open file')
        return

    nLength = int(steps.iloc[0]['gridSize'])
    grid = [[1/nLength**2] * nLength for _ in range(nLength)]

    for i in range(iterations):
        currentRow = steps.loc[i]
        for i in range(nLength):
            for j in range(nLength):
                # calculate the probability of the step
                grid[i][j] = grid[i][j] * norm.pdf(currentRow['eDist'], dist(currentRow['agentX'], currentRow['agentY'], i, j), 2/3)
        # normalize the grid   
        total = 0
        for i in range(nLength):
            for j in range(nLength):
                total = total + grid[i][j] 

        for i in range(nLength):
            for j in range(nLength):
                grid[i][j] = grid[i][j] / total
    
    maxCoords = (0,0)
    for i in range(nLength):
        for j in range(nLength):
            if grid[i][j] > grid[maxCoords[0]][maxCoords[1]]:
                maxCoords = (i,j)
        

    print(f"Car Estimated Location: {maxCoords}, probability: {grid[maxCoords[0]][maxCoords[1]]}")
    # print the grid to csv
    pd.DataFrame(grid).to_csv('grid.csv', header=False, index=False)
if __name__ == '__main__':
    func()