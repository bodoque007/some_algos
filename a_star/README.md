Have Pygame installed and python 3.10 (at least).
The script generates a random maze each time it's run (a rather bad one, to be fair) and tries to get from starting cell to ending cell using A* algorithm.
As for now, no path reconstruction algorithm is implemented. The window simply closes whenever it reached the ending cell or realised the maze is impossible to solve, printing out to the terminal which of those possibilities happened.

This was simply made after finishing the conway script, as I saw I could take advantage of already having the grid implemented.