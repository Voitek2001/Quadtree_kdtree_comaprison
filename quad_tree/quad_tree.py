from quad_tree.quad_tree_node import quad_tree_node
from visualizer.visualizer import *
from helper_classes.rectangle import rectangle 


class quad_tree:
    def __init__(self, initial_points, x = 0, y = 0, width = 100, height = 100):
        self.rect = rectangle(x, y, width, height)
        self.point_list = []
        self.point_set = set()
        quad_tree_node.point_list = self.point_list
        self.root = quad_tree_node(None, x, y, width, height)
        self.__add_all(initial_points)


    def find(self, x1 ,x2, y1, y2):
        scope_rect = rectangle(min(x1, x2), min(y1, y2), abs(x1- x2), abs(y1- y2))
        if not self.rect.contains_rect(scope_rect):
            raise TypeError('quad_tree does not fully contain given area')
        search_res = self.root.find(scope_rect)
        return self.__process_search_result(search_res)


    def add(self, new_point):
        new_point = tuple(new_point)
        self.__can_be_added(new_point)
        self.root.add(self.__add_to_structures(new_point))


    def __add_all(self, iterable):
        for point in iterable:
           self.add(point)


    def visualized_find(self, x1, x2, y1, y2):
        scope_rect = rectangle(min(x1, x2), min(y1, y2), abs(x1- x2), abs(y1- y2))
        scenes = []
        search_res = self.root.visualized_find(scenes, scope_rect)
        scenes.append(self.root.create_find_scene(scenes, scope_rect, []))
        Plot(scenes = scenes).draw() 
        return self.__process_search_result(search_res)


    def visualized_add(self, new_point):
        self.__can_be_added(new_point)
        scenes = []
        self.root.visualized_add(scenes, self.__add_to_structures(new_point))
        Plot(scenes = scenes).draw() 


    def __can_be_added(self, point):
        if not len(point) == 2:
            raise TypeError('quad_tree cannot handle points of different \
                dimension than 2, given point {point}')

        if not self.root.is_overlapping(point):
            raise ValueError('Given point: {point} is out of quad_tree bounds')
        
        if point in self.point_set:
            raise ValueError('quad_tree cannot handle duplicate points')


    def __add_to_structures(self, point):
        self.point_list.append(point)
        self.point_set.add(point)
        return len(self.point_list) - 1


    def __process_search_result(self, search_res):
        found_points = [self.point_list[i] for i in search_res]
        # print('found {} points: '.format(len(found_points)))
        # print(found_points)
        return found_points
