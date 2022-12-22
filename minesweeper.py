def increment_vertical(grid, row_index, column_index):
    # if there exists a cell above, attempt to increment 
    if 0 <= column_index-1 < len(grid):
        if grid[column_index-1][row_index] != "#":
            grid[column_index-1][row_index] += 1

    # if there exists a cell below, attempt to increment 
    if 0 <= column_index+1 < len(grid):
        if grid[column_index+1][row_index] != "#":
            grid[column_index+1][row_index] += 1


def minesweeper(grid):
    column_index = 0  # track current column
    # replaces all "-" with integer 0
    for row in grid:
        row_index = 0
        for row_index in range(len(row)):
            if row[row_index] == "-":
                row[row_index] = 0
                row_index += 1
    
    for row in grid:
        row_index = 0

        # "#"s will increment values of adjacent cells in same row
        for row_index in range(len(row)):
            if row[row_index] == "#":
                
                # if there exist a cell on left, attempt to increment
                if 0 <= row_index-1 < len(row):
                    if row[row_index-1] != "#":
                        row[row_index-1] += 1
                    increment_vertical(grid, row_index-1, column_index)
                
                # if there exists a cell on right, attempt to increment
                if 0 <= row_index+1 < len(row):
                    if row[row_index+1] != "#":
                        row[row_index+1] += 1
                    increment_vertical(grid, row_index+1, column_index)
                    
                # calls to increment above and below mine
                increment_vertical(grid, row_index, column_index)

        column_index += 1

    # cast integers into string
    for row in grid:
        row_index = 0
        for row_index in range(len(row)):
            row[row_index] = str(row[row_index])
        print(row)


mine_grid = []

while True:
    try:
        mine_grid_rows = int(input("Enter number of rows."))
        mine_grid_cols = int(input("Enter number of columns."))
        break
    except ValueError:
        print("Please input an integer.")

for i in range(0, mine_grid_cols):
    mine_grid_rows_list = []
    for a in range(mine_grid_rows):
        mine_grid_rows_list.append(" ")
    mine_grid.append(mine_grid_rows_list)

for col_index, row in enumerate(mine_grid):
    mine_grid_rows_list = []
    for row_index, element in enumerate(row):
        while True:
            mine_grid_form = input("Enter '-' for an empty space and '#' for a mine.")
            if mine_grid_form == "-" or mine_grid_form == "#":
                mine_grid[col_index][row_index] = mine_grid_form
                break
            else:
                print("Invalid input.")
        for elements in mine_grid:
            print(elements)

print("\n")
minesweeper(mine_grid)