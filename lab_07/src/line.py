import PyQt5
from PyQt5.QtCore import QPoint, QLine


class Line(QLine):
    def __init__(self, *args):
        super().__init__(*args)

        self.scene_item = None
    
    def setSceneItem(self, scene_item):
        self.scene_item = scene_item
    
    def sceneItem(self):
        return self.scene_item
