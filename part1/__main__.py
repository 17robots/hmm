import pandas as pd
import click
import math

def normal_prob(emitted_dist, actual_dist):
    THETA = 0.66
    return pow(THETA*math.sqrt(2*math.pi*pow(THETA,2)), -1) * math.exp(-(pow(emitted_dist - actual_dist, 2))/(2*pow(THETA,2)))    

def dist(x1, y1, x2, y2):
    return math.sqrt(pow((x1-x2),2) + pow((y1-y2),2))

@click.command()
@click.argument("filename")
# @click.argument()
# @click.argument()
def func(filename):
    # read in the steps
    steps: pd.DataFrame
    try:
        steps = pd.read_csv(filename)
    except Exception as e:
        print(e)
        print('Failed to open file')
        return

    nLength = int(steps.iloc[0]['gridSize'])
    grid = [[1/(nLength*nLength) for x in range(nLength)] for y in range(nLength)]

    for index, row in steps.iterrows():
        for i in range(nLength):
            for j in range(nLength):
                # calculate the probability of the step
                prob = normal_prob(row['eDist'], dist(row['agentX'], row['agentY'], i, j))
                if( i == 0 and j == 9):
                    print('emitted distance', row['eDist'],'actual distance', dist(row['agentX'], row['agentY'], i, j))
                    print('prob', prob)
                    print('grid', grid[i][j])

                grid[i][j] = grid[i][j] * prob
                
        total = sum([sum(row) for row in grid])
        for i in range(nLength):
            for j in range(nLength):
                grid[i][j] = grid[i][j] / total 

    # print the grid to csv
    pd.DataFrame(grid).to_csv('grid.csv', header=False, index=False)
if __name__ == '__main__':
    func()
