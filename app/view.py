from jinja2 import Environment, FileSystemLoader

class ReTrackerView:

    def __init__(self):
        pass

    def render_index(self, index_page):
        env = Environment(loader=FileSystemLoader('templates'))
        tmpl = env.get_template('./index.j2')
        return tmpl.render(page=index_page)
