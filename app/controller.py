from model import ReTrackerModel
from view import ReTrackerView

class ReTrackerController(object):

    def __init__(self):
        pass

    def index(self):
        return ReTrackerView().render_index(ReTrackerModel().get_index_content())
