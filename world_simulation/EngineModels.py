from random import randint
from world_simulation.EngineEvents import Event


class BaseObject:
    def __init__(self, column: int, row: int, config: object):
        self.row = row
        self.column = column
        self.config = config
        self.age = randint(self.config.age_min, self.config.age_max)
        self.health = randint(self.config.health_min, self.config.health_max)
        self.age_now = 0

    def produce_child(self) -> object:
        tmp = self.config.model(0, 0, self.config)
        return tmp

    def tick(self, world) -> Event:
        pass

    def _move(self, world):
        pass

    def info(self) -> str:
        return self._str_position()

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def _str_position(self):
        return '[' + str(self.column) + ', ' + str(self.row) + ']'


########################################################################
class BeingEntity:
    pass


class PeacefulEntity(BeingEntity):
    pass


class KillerEntity(BeingEntity):
    pass


class FoodEntity:
    pass


########################################################################
class FoodObject(BaseObject, FoodEntity):
    def __init__(self, row: int, column: int, config: object):
        super().__init__(row, column, config)

    def tick(self, world):
        self.age_now += 1
        if self.config.health_reduce_flag:
            self.health -= 1
        if self.age_now >= self.age or self.health <= 0:
            return Event.Die()
        return Event.Stay()

    def info(self) -> str:
        position: str = self._str_position()
        return 'F_' + position + '_health=' + str(self.health) + '_age=' + str(self.age_now) + '/' + str(self.age)

    def __str__(self):
        return str(self.health)

    def __repr__(self):
        return str(self.health)


########################################################################
class PredatorObject(BaseObject, KillerEntity):
    def __init__(self, column: int, row: int, config: object):
        super().__init__(column, row, config)

    def tick(self, world):
        self.age_now += 1

        if self.config.health_reduce_flag:
            self.health -= 1

        if self.age_now >= self.age or self.health <= 0:
            return Event.Die()

        if self.health >= 10:
            return Event.Reproduce(self.produce_child())

        return Event.Move()

    def info(self) -> str:
        position: str = self._str_position()
        return 'P_' + position + '_health=' + str(self.health) + '_age=' + str(self.age_now) + '/' + str(self.age)

    def __str__(self):
        return 'P'

    def __repr__(self):
        return 'P'


########################################################################
class HerbivoreObject(BaseObject, PeacefulEntity):
    def __init__(self, column: int, row: int, config: object):
        super().__init__(column, row, config)
        self.optima_path_last = -1  # todo
        self.optima_coords_last = (self.row, self.column)

    def tick(self, world):
        self.age_now += 1

        if self.config.health_reduce_flag:
            self.health -= 1

        if self.age_now >= self.age or self.health <= 0:
            return Event.Die()

        if self.health >= 10:
            self.health -= 5
            return Event.Reproduce(self.produce_child())

        self._move(world)

        if type(world[self.row][self.column]) is FoodObject:
            self.health += world[self.row][self.column].health
            self.optima_path_last = -1

        return Event.Move()

    def _move(self, world):
        if not isinstance(world[self.optima_coords_last[0]][self.optima_coords_last[1]], FoodObject):
            self.optima_path_last = -1
            self.optima_coords_last = (self.row, self.column)

        for i in range(len(world)):
            for j in range(len(world[i])):
                if isinstance(world[i][j], FoodEntity):
                    tmp_path = abs(self.row + self.column - i - j)
                    if tmp_path < self.optima_path_last or self.optima_path_last == -1 or \
                            (world[self.optima_coords_last[0]][self.optima_coords_last[1]].health < world[i][
                                j].health and tmp_path <= self.optima_path_last):
                        self.optima_path_last = tmp_path
                        self.optima_coords_last = (i, j)

        if self.row < self.optima_coords_last[0] and not isinstance(world[self.row + 1][self.column], BeingEntity):
            self.row += 1
        elif self.row > self.optima_coords_last[0] and not isinstance(world[self.row - 1][self.column], BeingEntity):
            self.row -= 1
        elif self.column < self.optima_coords_last[1] and not isinstance(world[self.row][self.column + 1], BeingEntity):
            self.column += 1
        elif self.column > self.optima_coords_last[1] and not isinstance(world[self.row][self.column - 1], BeingEntity):
            self.column -= 1
        else:
            try:
                self._move(world)
            except RecursionError:
                self.optima_path_last = -1
                self.optima_coords_last = (self.row, self.column)
                # random move to space
                if self.row < len(world) - 1 and (not isinstance(world[self.row + 1][self.column], BeingEntity)):
                    self.row += 1
                elif self.row == len(world) - 1 and (not isinstance(world[self.row - 1][self.column], BeingEntity)):
                    self.row -= 1
                elif self.column < len(world[0]) - 1 and (
                        not isinstance(world[self.row][self.column + 1], BeingEntity)):
                    self.column += 1
                elif self.column == len(world[0]) - 1 and (
                        not isinstance(world[self.row][self.column - 1], BeingEntity)):
                    self.column -= 1

    def info(self) -> str:
        position: str = self._str_position()
        return 'H_' + position + '_health=' + str(self.health) + '_age=' + str(self.age_now) + '/' + str(self.age)

    def __str__(self):
        return 'H'

    def __repr__(self):
        return 'H'
