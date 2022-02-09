import time

class SudokuField:
    def __init__(self, start_string):
        self.start_string = str(start_string)
        self.final_string = str(start_string)
        self.defined_cells_counter = 0
        self.resolved_cells_to_proceed = set()
        self.list_of_cells = []
        for index in range(81):
            Cell(index, int(self.start_string[index]), self)



class Cell:
    def __init__(self, index, value, field):
        self.index = index
        self.value = value
        self.field = field
        self.possible_values = self.possible_values_setter()
        self.neighbours = self.neighbours_indexes_setter()
        self.field.list_of_cells.append(self)
        if self.value != 0:
            self.field.resolved_cells_to_proceed.add(self)
            self.field.defined_cells_counter += 1

    def possible_values_setter(self):
        return {1, 2, 3, 4, 5, 6, 7, 8, 9} if self.value == 0 else {self.value}

    def neighbours_indexes_setter(self):
        neighbours = set()

        def createGenerator():
            for i in range(81):
                yield i

        nums = createGenerator()

        a = [[next(nums) for _ in range(9)] for _ in range(9)]
        for row in a:
            if self.value in row:
                neighbours.update(row)
                ind = row.index(self.value)
                for y in a:
                    neighbours.add(y[ind])

        a = {(0, 1, 2, 9, 10, 11, 18, 19, 20), (3, 4, 5, 12, 13, 14, 21, 22, 23), (6, 7, 8, 15, 16, 17, 24, 25, 26),
             (27, 28, 29, 36, 37, 38, 45, 46, 47), (30, 31, 32, 39, 30, 41, 48, 49, 50), (33, 34, 35, 42, 43, 44, 51, 52, 53),
             (54, 55, 56, 63, 64, 65, 72, 73, 74), (57, 58, 59, 66, 67, 68, 75, 76, 77), (60, 61, 62, 69, 70, 71, 78, 79, 80)}
        for cell in a:
            if self.index in cell:
                neighbours.update(cell)
                pass

        del(a, nums)
        neighbours.discard(self.index)
        return neighbours








class Row:
    pass


class ThreeRow:
    pass


class SudokuSolver:
    def __init__(self, start_string):
        self.field = SudokuField(start_string)
        self.resolve()

    def cell_possible_values_deleter(self):
        res_set = self.field.resolved_cells_to_proceed
        while res_set:
            c = res_set.pop()
            for neib_index in c.neighbours:
                neib = self.field.list_of_cells[neib_index]
                if len(neib.possible_values) > 1 and c.value in neib.possible_values:
                    neib.possible_values.remove(c.value)
                    if len(neib.possible_values) == 1:
                        neib.value = list(neib.possible_values)[0]
                        self.field.defined_cells_counter += 1
                        if self.field.defined_cells_counter == 81:
                            break
                        else:
                            res_set.add(neib)

    def print_the_decision(self):
        counter = 1
        self.field.final_string = ''
        for index in range(81):
            self.field.final_string += str(self.field.list_of_cells[index].value)
        for i in range(81):
            print(self.field.final_string[i], end='')
            if counter % 9 == 0:
                print()
            counter += 1
        print()



    def resolve(self):
        self.cell_possible_values_deleter()
        self.print_the_decision()


if __name__ == '__main__':
    row = input('please enter the start string: ')
    start_time = time.time()
    field = SudokuSolver(row)
    print(f'it took {time.time() - start_time} seconds to resolve')
    # easy level sudoku: 000090432120408900000720801000209740400675018370040620600007080754000100018904503