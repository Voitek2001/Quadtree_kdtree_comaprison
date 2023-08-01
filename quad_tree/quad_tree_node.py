import itertools
from copy import deepcopy

from visualizer.visualizer import *
import helper_classes.colors as colors
import helper_classes.points_manager as pm
from helper_classes.rectangle import rectangle 

class quad_tree_node:

    point_list : list = None
    
    def __init__(self, parent, x, y, width, height):
        if self.point_list == None:
            raise AttributeError("points attribute has to be " + 
            "initialized for quad_tree_node instance to work properly")
        self.__rect = rectangle(x, y, width, height)
        self.children = [None for _ in range(4)]
        self.children : list[quad_tree_node]
        self.point_indexes = []
        self.parent = parent


    def is_overlapping(self, point): 
        return rectangle.collide_point(self.__rect, point)


    def add(self, point_index):
        if self.__should_point_be_passed_to_child(point_index):
            self.__pass_point_to_child(point_index)
        self.point_indexes.append(point_index)


    def visualized_add(self, scenes, point_index):
        scene = self.__create_standard_add_scene(scenes, point_index)
        scene.add_lines_collection(
            LinesCollection(
                self.__rect.get_edges(),
                color = colors.ADD['curr_rect']
            )
        )
        scenes.append(scene)

        do_pass = self.__should_point_be_passed_to_child(
            point_index, lambda obj: obj.__visualized_divide(scenes, point_index)
        )
        
        if do_pass:
            self.__pass_point_to_child(
                point_index, 
                lambda obj, point_index: obj.visualized_add(scenes, point_index)
            )
        self.point_indexes.append(point_index)


    def find(self, rect:rectangle) -> list:
        if rect.contains_rect(self.__rect):
            return self.point_indexes.copy()

        if self.__has_children():
            search_res = []
            for child in self.children:
                if child.is_intersecting(rect):
                    search_res.extend(child.find(rect))
            return search_res
        else:
            overlapped_points = []
            if len(self.point_indexes) != 0:
                for point_index in self.point_indexes:
                    if rect.collide_point(self.point_list[point_index]):
                        overlapped_points.append(point_index)
            return overlapped_points



    def visualized_find(self, scenes, rect:rectangle) -> list:
        if rect.contains_rect(self.__rect):
            scenes.append(self.create_find_scene(scenes, rect, self.point_indexes, self.__rect))
            return self.point_indexes.copy()

        if self.__has_children():
            scenes.append(self.create_find_scene(scenes, rect, [], self.__rect))
            search_res = []
            for child in self.children:
                if child.is_intersecting(rect):
                    search_res.extend(child.visualized_find(scenes, rect))
            return search_res
        else:
            overlapped_points = []
            if len(self.point_indexes) != 0:
                for point_index in self.point_indexes:
                    if rect.collide_point(self.point_list[point_index]):
                        overlapped_points.append(point_index)
            scenes.append(self.create_find_scene(scenes, rect, overlapped_points, self.__rect))
            return overlapped_points


    def __divide(self):
        self.__create_children()
        self.__pass_point_to_child(self.point_indexes[0])


    def __visualized_divide(self, scenes, point_index):
        self.__create_children()
        self.__pass_point_to_child(self.point_indexes[0])

        scene = self.__create_standard_add_scene(scenes, point_index)
        scene.add_lines_collection(
            LinesCollection(
                list(itertools.chain.from_iterable([child.__rect.get_edges() for child in self.children])),
                color = colors.ADD['added_rect'],
                zorder = 50
            )
        )
        scenes.append(scene)


    def __get_all_rect_edges(self):
        edges = []
        if self.__has_children():
            for child in self.children:
                edges.extend(child.__get_all_rect_edges())
        edges.extend(self.__rect.get_edges())
        return edges
        

    def __create_standard_add_scene(self, scenes, added_point_index) -> Scene:
        head = self
        while head.parent != None:
            head = head.parent

        if len(scenes) != 0:
            std_points = scenes[0].points[0:2]
            return Scene(
                points = std_points,
                lines = [
                    LinesCollection(
                        head.__get_all_rect_edges(),
                        color = colors.STD['rect']
                    )
                ]
            )

        return Scene(
            points=[
                PointsCollection(
                    self.point_list,
                    color = colors.STD['point']
                ),
                PointsCollection(
                pm.get_points(self.point_list, [added_point_index])
                )
               
            ],
            lines=[
                LinesCollection(
                    head.__get_all_rect_edges(),
                    color = colors.STD['rect']
                )
            ]
        )
    

    def create_find_scene(self, scenes, search_rect, newly_included_point_indexes, curr_rect = None) -> Scene:
        if len(scenes) != 0:
            std_points = scenes[-1].points[0]
            std_lines = scenes[-1].lines[0:2]
            included_points = deepcopy(scenes[-1].points[1])
            included_points.points.extend(pm.get_points(self.point_list, newly_included_point_indexes))
            curr_rect_edges = []
            if curr_rect != None:
                curr_rect_edges.extend(curr_rect.get_edges())

            curr_rect_lines = LinesCollection(
                curr_rect_edges,
                color = colors.FIND['curr_rect']
            )
            return Scene(
                points = [std_points, included_points],
                lines = [*std_lines, curr_rect_lines]
            )

        head = self
        while head.parent != None:
            head = head.parent

        return Scene(
            points=[
                PointsCollection(
                    self.point_list,
                    color = colors.STD['point']
                ),
                PointsCollection(
                    [],
                    color = colors.FIND['included_points']
                )
            ],
            lines=[
                LinesCollection(
                    head.__get_all_rect_edges(),
                    color = colors.STD['rect']
                ),
                LinesCollection(
                    search_rect.get_edges(),
                    color = colors.FIND['search_rect']
                )
            ]
        )

    def is_intersecting(self, rect):
        return self.__rect.collide_rect(rect)


    def __create_children(self):
        hf_width = self.__rect.width / 2
        hf_height = self.__rect.height / 2

        my_rect = self.__rect
        self.children = [
            quad_tree_node(self, my_rect.x , my_rect.y, hf_width, hf_height),
            quad_tree_node(self, my_rect.x + hf_width, my_rect.y, hf_width, hf_height),
            quad_tree_node(self, my_rect.x + hf_width, my_rect.y + hf_height, hf_width, hf_height),
            quad_tree_node(self, my_rect.x, my_rect.y + hf_height, hf_width, hf_height)
        ]

    
    def __should_point_be_passed_to_child(self, point_index, divide_function = lambda obj: obj.__divide()):
        if self.__has_children():
            return True
        if len(self.point_indexes) == 0:
            self.point_indexes.append(point_index)
            return False
        divide_function(self)
        return True

        
    def __pass_point_to_child(self, point_index, add_function = lambda obj, point_index: obj.add(point_index) ):
        point = self.point_list[point_index]
        for child in self.children:
            if child.is_overlapping(point):
                add_function(child, point_index)
                break


    def __has_children(self):
        for child in self.children:
            if child:
                return True
        return False


    def add(self, point_index):
        if self.__should_point_be_passed_to_child(point_index):
            self.__pass_point_to_child(point_index)
        self.point_indexes.append(point_index)