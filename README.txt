Introduction to Artificial Intelligence – Project 1: Search in Blokus

This project was completed as part of the Introduction to Artificial Intelligence course. The goal is to implement and compare search algorithms on puzzles inspired by the board game Blokus.
The assignment includes implementing classical AI search techniques (DFS, BFS, UCS, A*) and designing admissible heuristics for extended problems like covering corners or multiple locations.

How to Run:

Run the Blokus game demo-
python3 game.py

DFS-
python3 game.py -p tiny_set.txt -s 4 7 -z fill

BFS-
python3 game.py -p tiny_set.txt -f bfs -s 4 7 -z fill

Uniform-Cost Search (UCS)-
python3 game.py -p tiny_set_2.txt -f ucs -s 6 6 -z corners
python3 game.py -p small_set.txt -f ucs -s 5 5 -z corners

A* Search with null heuristic-
python3 game.py -p tiny_set_2.txt -f astar -s 6 6 -z corners -H null_heuristic

A* Search with custom heuristics-
python3 game.py -p tiny_set_2.txt -f astar -s 6 6 -z corners -H blokus_corners_heuristic
python3 game.py -p small_set.txt -f astar -s 10 10 -H blokus_cover_heuristic -z cover -x 3 3 "[(2,2),(5,5),(6,7)]


Project Structure:

search.py: Implementations of DFS, BFS, UCS, A*
blokus_problems.py: Problem definitions and heuristics
game.py: Main file to run Blokus with different search strategies
board.py: Board logic and rules
util.py: Data structures (priority queues, stacks, etc.)
