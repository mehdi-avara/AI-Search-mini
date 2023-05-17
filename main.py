import pygame
import colors
from params import *
from Environment import Board
from Agent import Agent
import random
import numpy as np
# initialize:
FPS = 40
pygame.init()
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Search Game")

# setting start and end point :
start = {'x': 6, 'y': 0}
end = {'x': 12, 'y': 0}

gameBoard = Board(start, end,WIN)
clock = pygame.time.Clock()
agent = Agent(gameBoard,clock,FPS)


def main():
    run = True
    WIN.fill(colors.black)
    # agent.a_star()
    # agent.bfs()
    agent.dfs()

    while run:
        clock.tick(FPS)
    
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        gameBoard.draw_world()

    pygame.quit()
def MazeGenerator():
    for l in range(0,20):
        array = [ [0]*13 for i in range(13)]
        for i in range(0,13):
            for j in range(0,13):
                array[i][j] = random.choice([0,1])
        array = np.array(array)
        np.save("Mazes/"+str(l)+".npy",array)

main()
# MazeGenerator()
