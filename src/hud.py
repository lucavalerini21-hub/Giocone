from ursina import *
import math

class CurvedBar(Entity):
    def __init__(self, radius=0.2, thickness=0.05, start_angle=0, max_angle=180, bar_color=color.green, **kwargs):
        super().__init__(**kwargs)
        self.radius, self.thickness = radius, thickness
        self.start_angle, self.max_angle = start_angle, max_angle
        self.bar_color = bar_color
        self.value = 1.0
        self.model = Mesh(vertices=[], triangles=[], uvs=[], mode='triangle')
        self.update_bar()

    def update_bar(self):
        vertices, triangles = [], []
        segments = 50
        current_max_angle = self.max_angle * self.value
        for i in range(segments + 1):
            angle_rad = math.radians(self.start_angle + i / segments * current_max_angle)
            for r in [self.radius, self.radius + self.thickness]:
                vertices.append((math.cos(angle_rad) * r, math.sin(angle_rad) * r, 0))
            if i < segments:
                idx = i * 2
                triangles.extend([(idx, idx + 1, idx + 2), (idx + 1, idx + 3, idx + 2)])
        self.model.vertices, self.model.triangles = vertices, triangles
        self.model.generate()
        self.color = self.bar_color

    def set_value(self, value):
        new_value = max(0.0, min(1.0, value))
        if new_value != self.value:
            self.value = new_value
            self.update_bar()
