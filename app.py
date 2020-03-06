from world_simulation import WorldEngine, EngineConfig

mp = WorldEngine(5, 5)

EngineConfig.ModelsConfig.HerbivoreConfig.number_min = 1
EngineConfig.ModelsConfig.HerbivoreConfig.number_max = 1

EngineConfig.ModelsConfig.HerbivoreConfig.health_min = 4
EngineConfig.ModelsConfig.HerbivoreConfig.health_max = 6

EngineConfig.ModelsConfig.HerbivoreConfig.age_min = 20
EngineConfig.ModelsConfig.HerbivoreConfig.age_max = 35

EngineConfig.ModelsConfig.FoodConfig.number_min = 0
EngineConfig.ModelsConfig.FoodConfig.number_max = 2

EngineConfig.ModelsConfig.FoodConfig.spawn_number_min = 2
EngineConfig.ModelsConfig.FoodConfig.spawn_number_max = 3

EngineConfig.ModelsConfig.FoodConfig.age_min = 5
EngineConfig.ModelsConfig.FoodConfig.age_max = 5

EngineConfig.ModelsConfig.FoodConfig.health_min = 2
EngineConfig.ModelsConfig.FoodConfig.health_max = 5

EngineConfig.WorldConfig.load_model(EngineConfig.ModelsConfig.HerbivoreConfig)
EngineConfig.WorldConfig.load_model(EngineConfig.ModelsConfig.FoodConfig)

mp.run_loop(while_alive=True)
