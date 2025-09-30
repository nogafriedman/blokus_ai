# AI Search in Blokus

This project was completed as part of the Introduction to Artificial Intelligence course at HUJI. The goal is to implement and compare search algorithms on puzzles inspired by the board game Blokus.  
The assignment includes implementing classical AI search techniques (DFS, BFS, UCS, A*) and designing admissible heuristics for extended problems like covering corners or multiple locations.

<p float="left">
  <img src="https://github.com/user-attachments/assets/7521d567-ce2e-48c5-bf3d-374c2328f08d" width="172" /> 
  <img src="https://github.com/user-attachments/assets/d5ee9695-cb44-4d7a-a02b-7e34332a7ad9" width="172" /> 
  <img src="https://github.com/user-attachments/assets/b8e08b86-0b5a-45d4-afed-1e2244861596" width="173" />
</p>


# How to Run

__Run the Blokus game demo:__  
python3 game.py

__DFS:__  
python3 game.py -p tiny_set.txt -s 4 7 -z fill

__BFS:__  
python3 game.py -p tiny_set.txt -f bfs -s 4 7 -z fill

__Uniform-Cost Search (UCS):__  
python3 game.py -p tiny_set_2.txt -f ucs -s 6 6 -z corners
python3 game.py -p small_set.txt -f ucs -s 5 5 -z corners

__A* Search with null heuristic:__  
python3 game.py -p tiny_set_2.txt -f astar -s 6 6 -z corners -H null_heuristic

__A* Search with custom heuristics:__  
python3 game.py -p tiny_set_2.txt -f astar -s 6 6 -z corners -H blokus_corners_heuristic  
python3 game.py -p small_set.txt -f astar -s 10 10 -H blokus_cover_heuristic -z cover -x 3 3 "[(2,2),(5,5),(6,7)]

# Project Structure

```search.py```: Implementations of DFS, BFS, UCS, A*.  
```blokus_problems.py```: Problem definitions and heuristics.  
```game.py```: Main file to run Blokus with different search strategies.  
```board.py```: Board logic and rules.  
```util.py```: Data structures (priority queues, stacks, etc.).  
