class rectangle():
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height


    def collide_point(self, point) -> bool:
        return not (
            point[0] > self.x + self.width or
            point[0] < self.x or
            point[1] > self.y + self.height or
            point[1] < self.y
        )

    
    def collide_rect(self, rect) -> bool:
        return not(
            rect.x > self.x + self. width or 
            rect.x + rect.width <= self.x or
            rect.y > self.y + self.height or
            rect.y + rect.height <= self.y
        )

    
    def contains_rect(self, rect) -> bool:
        return (
            self.x <= rect.x and
            self.x + self.width >= rect.x + rect.width and 
            self.y <= rect.y and
            self.y + self.height >= rect.y + rect.height 
        )

    
    def get_edges(self):
        return [
            ((self.x, self.y), (self.x, self.y + self.height)),
            ((self.x, self.y + self.height), (self.x + self.width, self.y + self.height)),
            ((self.x + self.width, self.y + self.height), (self.x + self.width, self.y)),
            ((self.x + self.width, self.y), (self.x, self.y))
        ]
    
    
    def get_axis_ranges(self):
        return (
            self.x,
            self.x + self.width,
            self.y,
            self.y + self.height
        )