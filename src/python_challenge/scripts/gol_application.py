from game_of_life import GOL
import numpy as np
import time

print("Conway's Game of Life -  Implementation by Mihir Kulkarni for JDERobot GSoC 2020")

g = GOL()
d = {1: g.BLOCK, 2: g.TUB, 3: g.BLINKER,  4: g.BEACON, 5: g.GLIDER, 6: g.LWSS}

for _ in range(20):
	print("Please enter the number (1-8) of the pattern you would like to add to the grid or enter 9 for random. To start the game with the selected settings enter 0")
	print("0 Start Game\n1 Block\n2 Tub\n3 Blinker\n4 Beacon\n5 Glider\n6 Light Space Ship\n9 Random Grid")
	selection = int(input("Your Choice: "))
	if selection == 0:
		break
	elif selection == 9:
		g.init_env()
	else:
		i,j = map(int,input("Please enter the location for the pattern as two space-seperated integers: ").split())
		g.add_object(occupied_list = d[selection], x_ref = i, y_ref = j)

print("Press Ctrl+C at any point to exit. The program shall automatically exit after the maximum iterations.")
generations = int(input("Please enter the number of generations you want to simulate:- "))
for counter in range(generations):
    g.update_environment(g.active)
    g.show_env()
    g.update()
    print("Active: " +str(len(g.active)) + "\t Neighbourhood:"+ str(len(g.neighbours)))

print("Thank you for playing!")