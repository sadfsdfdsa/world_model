from world_simulation.EngineModels import *


class EngineConfig:
    class WorldConfig:
        use_models = []

        @classmethod
        def load_model(cls, model_config):
            cls.use_models.append(model_config)

    class ModelsConfig:
        class PredatorConfig:
            number_min = 0
            number_max = 0
            health_min = 5
            health_max = 5

            health_reduce_flag = True
            log_flag = True

            age_min = 100000
            age_max = 100000

            model = PredatorObject

            health_to_reproduce = 10

        class HerbivoreConfig:
            number_min = 0
            number_max = 0
            health_min = 5
            health_max = 5

            health_reduce_flag = True
            log_flag = True

            age_min = 100000
            age_max = 100000

            model = HerbivoreObject

            health_to_reproduce = 10

        class FoodConfig:
            number_min = 0
            number_max = 0
            health_min = 5
            health_max = 5

            health_reduce_flag = False
            log_flag = False

            age_min = 100000
            age_max = 100000

            model = FoodObject

            spawn_number_min = 1
            spawn_number_max = 1
