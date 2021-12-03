import pandas as pd
import click
import math
from scipy.stats import norm

def dist(x1, y1, x2, y2):
    return math.sqrt(pow((x1-x2),2) + pow((y1-y2),2))

@click.command()
@click.argument("emissions")
@click.argument("transitions")
@click.argument("iterations", type=int)
def func(emissions, transitions, iterations):
    # read in the steps
    steps: pd.DataFrame
    transitions: pd.DataFrame
    try:
        steps = pd.read_csv(emissions)
        transitions = pd.read_csv(transitions)
    except Exception as e:
        print('Failed to open file(s)')
        return
        
    nLength = int(steps.loc[0]['gridSize'])
    # if len(transitions) != nLength:
    #     raise Exception('Transition matrix is not the same size as the grid')

    def calc_prob(x, y, _grid):
        return (
            """top"""(_grid[(x - 1 + nLength) % nLength][y] * transitions.loc[(x - 1) * nLength + y]['N']) + 
            """bot"""(_grid[(x + 1 + nLength) % nLength][y] * transitions.loc[(x + 1) * nLength + y]['S']) + 
            """lef"""(_grid[x][(y - 1 + nLength) % nLength] * transitions.loc[x * nLength + (y - 1)]['W']) + 
            """rig"""(_grid[x][(y + 1 + nLength) % nLength] * transitions.loc[x * nLength + (y + 1)]['E'])
            )

    grid = [[1/nLength**2] * nLength for _ in range(nLength)]
    pastGrid = grid

    for i in range(iterations):
        currentRow = steps.loc[i]
        for i in range(nLength):
            for j in range(nLength):
                # calculate the probability of the step
                grid[i][j] = grid[i][j] * norm.pdf(currentRow['eDist'], dist(currentRow['agentX'], currentRow['agentY'], i, j), 2/3) * calc_prob(i, j, pastGrid)
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