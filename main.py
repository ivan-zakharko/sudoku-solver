import time
import re


class SudokuField:
    def __init__(self, start_string):
        self.start_string = str(start_string)
        self.defined_cells_counter = 0
        self.resolved_cells_to_proceed = set()
        self.list_of_cells = []
        self.list_of_rows = []
        self.list_of_threerows = []
        self.matrix = self.make_matrix()
        self.block_indexes = {(0, 1, 2, 9, 10, 11, 18, 19, 20), (3, 4, 5, 12, 13, 14, 21, 22, 23),
             (6, 7, 8, 15, 16, 17, 24, 25, 26),
             (27, 28, 29, 36, 37, 38, 45, 46, 47), (30, 31, 32, 39, 30, 41, 48, 49, 50),
             (33, 34, 35, 42, 43, 44, 51, 52, 53), (54, 55, 56, 63, 64, 65, 72, 73, 74),
             (57, 58, 59, 66, 67, 68, 75, 76, 77), (60, 61, 62, 69, 70, 71, 78, 79, 80)}
        for index in range(81):
            Cell(index, int(self.start_string[index]), self)

    @staticmethod
    def make_matrix():
        def creategenerator():
            for i in range(81):
                yield i

        nums = creategenerator()
        return [[next(nums) for _ in range(9)] for _ in range(9)]


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

        # find neighbours in row and column
        for row in self.field.matrix:
            if self.index in row:
                neighbours.update(row)
                index_in_row = row.index(self.index)
                for y in self.field.matrix:
                    neighbours.add(y[index_in_row])

        # find neighbours in block
        for block in self.field.block_indexes:
            if self.index in block:
                neighbours.update(block)
                break

        neighbours.discard(self.index)
        return neighbours


class Row:
    def __init__(self, row_number, field):
        self.field = field
        self.row = self.field.matrix[row_number]
        self.value = []
        self.make_rows()
        self.field.list_of_rows.append(self.value)

    def make_rows(self):
        for v0 in self.field.list_of_cells[self.row[0]].possible_values:
            prop = [v0]
            for v1 in self.field.list_of_cells[self.row[1]].possible_values:
                prop = prop[:1]
                if v1 in prop: continue
                prop.append(v1)
                for v2 in self.field.list_of_cells[self.row[2]].possible_values:
                    prop = prop[:2]
                    if v2 in prop: continue
                    prop.append(v2)
                    for v3 in self.field.list_of_cells[self.row[3]].possible_values:
                        prop = prop[:3]
                        if v3 in prop: continue
                        prop.append(v3)
                        for v4 in self.field.list_of_cells[self.row[4]].possible_values:
                            prop = prop[:4]
                            if v4 in prop: continue
                            prop.append(v4)
                            for v5 in self.field.list_of_cells[self.row[5]].possible_values:
                                prop = prop[:5]
                                if v5 in prop: continue
                                prop.append(v5)
                                for v6 in self.field.list_of_cells[self.row[6]].possible_values:
                                    prop = prop[:6]
                                    if v6 in prop: continue
                                    prop.append(v6)
                                    for v7 in self.field.list_of_cells[self.row[7]].possible_values:
                                        prop = prop[:7]
                                        if v7 in prop: continue
                                        prop.append(v7)
                                        for v8 in self.field.list_of_cells[self.row[8]].possible_values:
                                            prop = prop[:8]
                                            if v8 in prop: continue
                                            prop.append(v8)
                                            self.value.append(prop)


class ThreeRow:
    def __init__(self, threerow_number, field):
        self.field = field
        self.rows = [threerow_number, threerow_number + 1, threerow_number + 2]
        self.value = []
        self.make_threerows()
        self.field.list_of_threerows.append(self.value)

    @staticmethod
    def coll_repeat_checker(row, prop):
        for index in range(9):
            for r in prop:
                if row[index] == r[index]:
                    return True

    def make_threerows(self):
        for r1 in self.field.list_of_rows[self.rows[0]]:
            prop = [r1]
            for r2 in self.field.list_of_rows[self.rows[1]]:
                prop = prop[:1]
                if self.coll_repeat_checker(r2, prop): continue
                prop.append(r2)
                for r3 in self.field.list_of_rows[self.rows[2]]:
                    prop = prop[:2]
                    if self.coll_repeat_checker(r3, prop): continue
                    prop.append(r3)
                    self.value.append(prop)


class SudokuSolver:
    def __init__(self, start_string):
        fail_input = self.input_checker(start_string)
        if not fail_input:
            self.field = SudokuField(start_string)
            self.resolve()
        else:
            print(fail_input)

    @staticmethod
    def input_checker(row):
        if len(row) != 81:
            return f'the string length should be exactly 81 character. You have inputted {len(row)}.'
        if re.search(r"\D", row):
            return 'You have inputted the string, which contains non-digit characters. String should contain only digits.'

    def cell_possible_values_deleter(self):
        while self.field.resolved_cells_to_proceed:
            c = self.field.resolved_cells_to_proceed.pop()
            for neib_index in c.neighbours:
                neib = self.field.list_of_cells[neib_index]
                if len(neib.possible_values) > 1 and c.value in neib.possible_values:
                    neib.possible_values.remove(c.value)
                    if len(neib.possible_values) == 1:
                        neib.value = list(neib.possible_values)[0]
                        self.field.defined_cells_counter += 1
                        switcher = True
                        if self.field.defined_cells_counter == 81:
                            switcher = False
                            break
                        else:
                            self.field.resolved_cells_to_proceed.add(neib)

    def block_checker(self, stack):
        values_candidates = dict()
        for index in stack:
            cell = self.field.list_of_cells[index]
            if cell.value != 0: continue
            for possible in cell.possible_values:
                values_candidates[possible] = values_candidates.get(possible, [])
                values_candidates[possible].append(cell)
        for k, v in values_candidates.items():
            if len(v) == 1:
                c = v.pop()
                c.value = k
                c.possible_values.clear()
                c.possible_values.add(k)
                self.field.resolved_cells_to_proceed.add(c)
                self.field.defined_cells_counter += 1
                global switcher
                switcher = True

    def stack_checker(self):
        for block in self.field.block_indexes:
            self.block_checker(block)
        for row in self.field.matrix:
            self.block_checker(row)
        for index in range(9):
            vertical_list = []
            for row in self.field.matrix:
                vertical_list.append(row[index])
            self.block_checker(vertical_list)

    def row_creator(self):
        for i in range(9):
            Row(i, self.field)

    def threerow_creator(self):
        for i in [0, 3, 6]:
            ThreeRow(i, self.field)

    def values_maker(self, decision):
        counter = 0
        for row in decision:
            for elem in row:
                self.field.list_of_cells[counter].value = elem
                counter += 1

    def final_compose(self):
        for tr1 in self.field.list_of_threerows[0]:
            prop = [r for r in tr1]
            for tr2 in self.field.list_of_threerows[1]:
                prop = prop[:3]
                repeat = False
                for elem in tr2:
                    if ThreeRow.coll_repeat_checker(elem, prop):
                        repeat = True
                if repeat: continue
                prop.extend(tr2)
                for tr3 in self.field.list_of_threerows[2]:
                    prop = prop[:6]
                    repeat = False
                    for elem in tr3:
                        if ThreeRow.coll_repeat_checker(elem, prop):
                            repeat = True
                    if repeat: continue
                    prop.extend(tr3)
                    self.values_maker(prop)
                    break

    def final_bust(self):
        self.row_creator()
        self.threerow_creator()
        self.final_compose()

    def print_the_decision(self):
        counter = 1
        for i in range(81):
            print(self.field.list_of_cells[i].value, end='')
            if counter % 9 == 0:
                print()
            counter += 1
        print()

    def resolve(self):
        self.cell_possible_values_deleter()
        if self.field.defined_cells_counter == 81:
            self.print_the_decision()
        else:
            global switcher
            switcher = True
            while switcher and self.field.defined_cells_counter != 81:
                switcher = False
                self.stack_checker()
                self.cell_possible_values_deleter()
            if self.field.defined_cells_counter == 81:
                self.print_the_decision()
            else:
                self.final_bust()
                self.print_the_decision()


if __name__ == '__main__':
    row = input('please enter the start string: ')
    start_time = time.time()
    field = SudokuSolver(row)
    print(f'it took {time.time() - start_time} seconds to resolve')
    # easy level sudoku: 000090432120408900000720801000209740400675018370040620600007080754000100018904503
    # medium level 790000610000060207106470000582000461000000050000508020640200500900050000053080076
    # hard level 001000060000800000073000019005002007000760580704590006060020000000000078190003240
    # expert level 000060027000000005004091080008000004000430000070080030300009001720100000090000200
    # insane level 700000080050240001000006000040310002005000400000090000000005006008630010030009000
