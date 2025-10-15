if __name__ == "__main__":
    class Point:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y
        def set_x(self, x):
            self.x = x
        def get_x(self):
            return self.x
        def set_y(self, y):
            self.y = y
        def get_y(self):
            return self.y
        def compute_distance(self, point):
            return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5

    class Line:
        def __init__(self, start_point, end_point):
            self.start_point = start_point
            self.end_point = end_point
            self.length = self.compute_length()
        def compute_length(self):
            return self.start_point.compute_distance(self.end_point)
        def set_start(self, point):
            self.start_point = point
        def get_start(self):
            return self.start_point
        def set_end(self, point):
            self.end_point = point
        def get_end(self):
            return self.end_point
        def get_length(self):
            return self.length

    class Shape:
        def __init__(self):
            self.vertices = []
            self.edges = []
            self.inner_angles = []
            self.is_regular = False
        def set_vertices(self, vertices):
            self.vertices = vertices
        def get_vertices(self):
            return self.vertices
        def set_edges(self, edges):
            self.edges = edges
        def get_edges(self):
            return self.edges
        def set_inner_angles(self, angles):
            self.inner_angles = angles
        def get_inner_angles(self):
            return self.inner_angles
        def set_is_regular(self, regular):
            self.is_regular = regular
        def get_is_regular(self):
            return self.is_regular
        def compute_area(self):
            return 0
        def compute_perimeter(self):
            return 0
        def compute_inner_angles(self):
            return []

    class Triangle(Shape):
        def __init__(self, p1, p2, p3):
            super().__init__()
            self.vertices = [p1, p2, p3]
            self.edges = [Line(p1, p2), Line(p2, p3), Line(p3, p1)]
        def compute_perimeter(self):
            return sum(line.length for line in self.edges)
        def compute_area(self):
            a, b, c = [line.length for line in self.edges]
            s = (a + b + c) / 2
            return (s*(s-a)*(s-b)*(s-c))**0.5

    class Isosceles(Triangle):
        def __init__(self, p1, p2, p3):
            super().__init__(p1, p2, p3)
            lengths = [line.length for line in self.edges]
            self.is_regular = len(set(round(l,5) for l in lengths)) <= 2

    class Equilateral(Triangle):
        def __init__(self, p1, p2, p3):
            super().__init__(p1, p2, p3)
            lengths = [line.length for line in self.edges]
            self.is_regular = len(set(round(l,5) for l in lengths)) == 1

    class Scalene(Triangle):
        def __init__(self, p1, p2, p3):
            super().__init__(p1, p2, p3)
            lengths = [line.length for line in self.edges]
            self.is_regular = len(set(round(l,5) for l in lengths)) == 3

    class TriRectangle(Triangle):
        def __init__(self, p1, p2, p3):
            super().__init__(p1, p2, p3)

    class Rectangle(Shape):
        def __init__(self, **kwargs):
            super().__init__()
            if "bottom_left" in kwargs and "width" in kwargs and "height" in kwargs:
                bottom_left = kwargs["bottom_left"]
                width = kwargs["width"]
                height = kwargs["height"]
                p1 = bottom_left
                p2 = Point(bottom_left.x + width, bottom_left.y)
                p3 = Point(bottom_left.x + width, bottom_left.y + height)
                p4 = Point(bottom_left.x, bottom_left.y + height)
                self.vertices = [p1, p2, p3, p4]
            elif "corner1" in kwargs and "corner2" in kwargs:
                corner1 = kwargs["corner1"]
                corner2 = kwargs["corner2"]
                self.vertices = [corner1, Point(corner2.x, corner1.y),
                                 corner2, Point(corner1.x, corner2.y)]
            else:
                raise ValueError("Argumentos inválidos para inicializar el rectángulo")
            self.edges = [Line(self.vertices[i], self.vertices[(i+1)%4]) for i in range(4)]
            self.width = self.edges[0].length
            self.height = self.edges[1].length
        def set_width(self, w):
            self.width = w
        def get_width(self):
            return self.width
        def set_height(self, h):
            self.height = h
        def get_height(self):
            return self.height
        def compute_area(self):
            return self.width * self.height
        def compute_perimeter(self):
            return 2 * (self.width + self.height)

    class Square(Rectangle):
        def __init__(self, center_point, side):
            x = center_point.x - side/2
            y = center_point.y - side/2
            bottom_left = Point(x, y)
            super().__init__(bottom_left=bottom_left, width=side, height=side)
            self.is_regular = True
        def compute_area(self):
            return self.width ** 2
        def compute_perimeter(self):
            return 4 * self.width

#Pruebas generales de todo
    p1 = Point(0, 0)
    p2 = Point(4, 0)
    p3 = Point(2, 3)
    p4 = Point(4, 3)

    print("---- TRIÁNGULOS ----")
    t = Triangle(p1, p2, p3)
    print("Área triángulo:", round(t.compute_area(), 2))
    print("Perímetro triángulo:", round(t.compute_perimeter(), 2))

    iso = Isosceles(Point(0,0), Point(2,0), Point(1,3))
    print("Isósceles regular:", iso.get_is_regular())

    eq = Equilateral(Point(0,0), Point(2,0), Point(1,1.732))
    print("Equilátero regular:", eq.get_is_regular())

    sc = Scalene(Point(0,0), Point(4,0), Point(3,2))
    print("Escaleno regular:", sc.get_is_regular())

    print("---- RECTÁNGULOS ----")
    rect = Rectangle(corner1=p1, corner2=p4)
    print("Área rectángulo:", rect.compute_area())
    print("Perímetro rectángulo:", rect.compute_perimeter())

    print("---- CUADRADOS ----")
    sq = Square(Point(2, 2), 4)
    print("Área cuadrado:", sq.compute_area())
    print("Perímetro cuadrado:", sq.compute_perimeter())
