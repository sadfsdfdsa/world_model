from world_simulation.EngineConfig import *
from world_simulation.EngineLogger import EngineLogger


class WorldEngine:
    class State:
        iteration = 0
        objects = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.world = [[0 for _ in range(x)] for _ in range(y)]
        self.WorldConfig = EngineConfig.WorldConfig
        self.FoodConfig = EngineConfig.ModelsConfig.FoodConfig
        # todo logger
        self.Logger = EngineLogger

    def configure_map(self) -> None:
        for obj in self.WorldConfig.use_models:
            tmp = randint(obj.number_min, obj.number_max)
            for item in range(tmp):
                self.__create_instance(obj)
        print('Init map success!')

    def mp_print(self) -> None:
        for row in self.world:
            print(row)

    def mp_print_state(self) -> None:
        for obj in self.State.objects:
            if obj.config.log_flag:
                print(obj.info())

    def mp_draw(self):
        self.mp_print_state()
        self.mp_print()
        print('____________________' + str(self.State.iteration))

    def __random_position(self) -> (int, int):
        if self.__world_full:
            self.mp_print()
            raise Exception('World is full in iteration: ' + str(self.State.iteration))
        tmp_x = randint(0, self.x - 1)
        tmp_y = randint(0, self.y - 1)
        while self.world[tmp_y][tmp_x] != 0:
            tmp_x = randint(0, self.x - 1)
            tmp_y = randint(0, self.y - 1)
        return int(tmp_x), int(tmp_y)

    @property
    def __world_full(self) -> bool:
        for row in self.world:
            for item in row:
                if item == 0:
                    return False
        return True

    @property
    def __being_entities_in_world(self):
        for obj in self.State.objects:
            if isinstance(obj, BeingEntity):
                return True
        return False

    def __create_instance(self, config):
        column, row = self.__random_position()
        tmp: object = config.model(column, row, config)
        self.world[row][column] = tmp
        self.State.objects.append(tmp)

    def __create_instance_from_object(self, obj):
        column, row = self.__random_position()
        obj.column = column
        obj.row = row
        self.world[row][column] = obj
        self.State.objects.append(obj)

    def tick(self) -> None:
        for i in range(
                randint(self.FoodConfig.spawn_number_min, self.FoodConfig.spawn_number_max)):
            self.__create_instance(self.FoodConfig)

        for obj in self.State.objects:
            prev_coord = (obj.row, obj.column)

            event = obj.tick(self.world)

            if type(event) is Event.Die:
                self.world[obj.row][obj.column] = 0
                self.State.objects.remove(obj)

            elif type(event) is Event.Reproduce:
                tmp = event.child
                self.__create_instance_from_object(tmp)

            elif type(event) is Event.Move:
                if self.world[obj.row][obj.column] in self.State.objects and obj != self.world[obj.row][obj.column]:
                    self.State.objects.remove(self.world[obj.row][obj.column])
                self.world[prev_coord[0]][prev_coord[1]] = 0
                self.world[obj.row][obj.column] = obj

            elif type(event) is Event.Stay:  # food
                pass

        self.State.iteration += 1

    def run_loop(self, number: int = -1, step_by_step: bool = False, while_alive: bool = False):
        self.configure_map()
        self.mp_draw()

        if number > 0:
            for i in range(number):
                self.tick()
                self.mp_draw()
                if while_alive and not self.__being_entities_in_world:
                    break
            self.mp_draw()
            return

        while True:
            if step_by_step:
                input()
            self.tick()
            self.mp_draw()

            if while_alive and not self.__being_entities_in_world:
                return
