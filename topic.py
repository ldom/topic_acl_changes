class Topic:
    def __init__(self, name, nb_partitions, placement, config_properties):
        self.name = name
        self.nb_partitions = nb_partitions
        self.placement = placement
        self.config_properties = config_properties
