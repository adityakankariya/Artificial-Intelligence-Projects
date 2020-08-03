from BaseAI import BaseAI
import time
import math

time_limit = 0.19

cell_weights = [ # Assigns weights to each cell, where cells towards the top left are given more importance
	[0.13, 0.12, 0.1, 0.0999],
	[0.099, 0.088, 0.077, 0.07],
	[0.06, 0.055, 0.035, 0.015],
	[0.0125, 0.01, 0.005, 0.003],
]

class IntelligentAgent(BaseAI):   
    def getMove(self, grid):
        # Selects a random move and returns it
        moveset = grid.getAvailableMoves()
        self.start_time = time.process_time()
        move = self.ids(grid)[0]
        for i in range(len(moveset)):
            if moveset[i][0] == move:
                return moveset[i][0]
        
    def ids(self, grid):
        depth = 1
        max_score = -math.inf
        max_move = 0
        while True:
            if time.process_time() - self.start_time >= time_limit:
                return max_move, max_score
            
            move, utility = self.max_player(grid, depth, -math.inf, math.inf)
            if utility > max_score:
                max_move = move
                max_score = utility
                
            depth += 1
		
        return max_move
    
    def max_player(self, grid, depth, a, b):
        if time.process_time() - self.start_time >= time_limit or depth == 0:
            return -1, self.evaluate_heuristics(grid)
        
        children = grid.getAvailableMoves()
        if len(children) == 0:
            return -1, self.evaluate_heuristics(grid)
        
        max_move = None
        max_utility = -math.inf
        
        for child in children:
            updated_grid = child[1].clone()
            _, utility = self.chance_node(updated_grid, depth - 1, a, b)
            if utility > max_utility:
                max_move = child[0]
                max_utility = utility
            if max_utility >= b: # alpha > beta, remaining branches "pruned" as a result of break
                break
            if a > max_utility: # Updates alpha
                a = max_utility 
                
        return max_move, max_utility
    
    def chance_node(self, grid, depth, a, b):
        if time.process_time() - self.start_time >= time_limit or depth == 0:
            return -1, self.evaluate_heuristics(grid)
        
        updated_grid_two = grid.clone()
        updated_grid_four = grid.clone()
        _, utility_two = self.min_player(updated_grid_two, depth, a, b, 2)
        _, utility_four = self.min_player(updated_grid_four, depth, a, b, 4)
        utility = utility_two * 0.9 + utility_four * 0.1 # Expectiminimax
        return None, utility
    
    def min_player(self, grid, depth, a, b, two_or_four):
        if time.process_time() - self.start_time >= time_limit or depth == 0:
            return -1, self.evaluate_heuristics(grid)
        
        available_cells = grid.getAvailableCells()
        children = []
        for i in available_cells:
            grid_twofour = grid.clone()
            if two_or_four == 4:
                grid_twofour.insertTile(i, 4)
            else:
                grid_twofour.insertTile(i, 2)
            children.append(grid_twofour)
            
        if len(children) == 0:
            return -1, self.evaluate_heuristics(grid)
        
        min_utility = math.inf
        
        for child in children:
            updated_grid = child.clone()
            _, utility = self.max_player(updated_grid, depth - 1, a, b)
            if utility < min_utility:
                min_utility = utility
            if min_utility <= a: # beta < alpha, remaining branches "pruned" as a result of break
                break
            if b < min_utility: # Updates beta
                b = min_utility
                
        return None, min_utility
    
    def evaluate_heuristics(self, grid):
        available_cells = len(grid.getAvailableCells()) * 20
        max_tile_val = math.log(grid.getMaxTile())/math.log(2)
        max_tile_pos = self.get_max_tile_pos(grid) * 100
        cell_weights = self.get_cell_weights(grid) * 420
        mono = self.monotonicity(grid) * 10
        return available_cells + max_tile_val + max_tile_pos + cell_weights + mono
    
    def get_max_tile_pos(self, grid):
        if grid.getCellValue((0, 0)) == grid.getMaxTile():
            return 100000
        return -100000
    
    def get_cell_weights(self, grid):
        total = 0
        for i in range(4):
            for j in range(4):
                total += grid.getCellValue((i,j)) * cell_weights[i][j]
        return total
    
    def monotonicity(self, grid): 
        total = 0
        for i in range(4):
            diff = grid.getCellValue((i, 0)) - grid.getCellValue((i, 1))
            for j in range(3):
                if (grid.getCellValue((i, j)) - grid.getCellValue((i, j + 1))) * diff <= 0:
                    total += 1
                diff = grid.getCellValue((i, j)) - grid.getCellValue((i, j + 1))
        for i in range(4):
            diff = grid.getCellValue((0, i)) - grid.getCellValue((1, i))
            for j in range(3):
                if (grid.getCellValue((j, i)) - grid.getCellValue((j + 1, i))) * diff <= 0:
                    total += 1
                diff = grid.getCellValue((j, i)) - grid.getCellValue((j + 1, i))
        
        return total
    