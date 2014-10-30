import re

class Action(object):
    def __init__(self, actions):
        self.desc = None
        self.code = None
        self.short_desc = None
        self.parameters = []
        actions.actions.append(self)
        self.buttons = []
    def add_parameter(self, name, min, max, decimals):
        self.parameters.append(Parameter(name, min, max, decimals))
    def add_button(self, **kwargs):
        self.buttons.append(dict(**kwargs))

    def get_short_desc(self, params):
        desc = self.short_desc
        for p in self.parameters:
            desc = desc.replace('{%s}' % p.name, p.get_text(params[p.name]))
        return desc

    def get_code(self, params):
        code = self.code
        for p in self.parameters:
            code = code.replace('{%s}' % p.name, p.get_text(params[p.name]))
        return code

    def parse_code(self, code):
        pattern = self.code
        pattern = pattern.replace('*', r'\*')
        for p in self.parameters:
            k = p.name
            pattern = pattern.replace('{%s}' % k, r'(?P<%s>\d*\.*\d+)' % k)
        m = re.match(pattern, code)
        if m is not None:
            return {k: float(v) for k,v in m.groupdict().items()}

    def make_buttons(self):
        html = []
        for b in self.buttons:
            short = self.get_short_desc(b)
            code = self.get_code(b)
            text = '''<input type='button' value='%s' onclick='doaction("%s");'/>'''
            text = text % (short, code)
            html.append(text)
        return ''.join(html)

    def make_control_html(self, params):
        desc = self.desc
        sliders = []
        for p in self.parameters:
            span = '<span id="slider_%s_value">%s</span>' % (p.name,
                                                p.get_text(params[p.name]))
            desc = desc.replace('{%s}' % p.name, span)
            slider = '<div id="slider_%s"></div>' % p.name
            sliders.append(slider)
        return '%s %s' % (desc, ''.join(sliders))

    def make_control_code(self, params):
        replace = ''
        for p in self.parameters:
            replace += "action=action.replace('{%s}', d3.select('#slider_%s_value').text()); " % (p.name, p.name)
        code = []
        for p in self.parameters:
            code.append('''
function slide_%(name)s_func(event, value) {
        d3.select('#slider_%(name)s_value').text(value.toFixed(%(decimals)d));
}

function slide_%(name)s_funcend(event, value) {
    action = "%(code)s";
    %(replace)s
    doaction(action, true);
}

d3.select('#slider_%(name)s').call(d3.slider()
                             .min(%(min)g)
                             .axis(true)
                             .max(%(max)g)
                             .value(%(value)g)
                             .on("slide", slide_%(name)s_func)
                             .on("slideend", slide_%(name)s_funcend));
''' % dict(name=p.name, min=p.min, max=p.max, value=params[p.name],
           decimals=p.decimals, code=self.code, replace=replace))

        return ''.join(code)







class Parameter(object):
    def __init__(self, name, min, max, decimals):
        self.name = name
        self.min = min
        self.max = max
        self.decimals = decimals
    def get_text(self, value):
        return '%g' % round(value, self.decimals)


class Actions(object):
    def __init__(self):
        self.actions = []
        self.make_actions()

    def find_action(self, code):
        for a in self.actions:
            result = a.parse_code(code)
            if result is not None:
                return a, result
        return None

    def make_buttons(self):
        html = []
        for a in self.actions:
            html.append(a.make_buttons())
        return ' '.join(html)

    def make_actions(self):
        a = Action(self)
        a.desc = '''Make no policy changes.'''
        a.code = 'nothing'
        a.short_desc = 'Do nothing'
        a.add_button()

        a = Action(self)
        a.add_parameter('price', min=0.01, max=100.0, decimals=2)
        a.desc = '''Farmers sell organic peaches at ${price} per ton.'''
        a.code = 'price:peachesOrganicBabyGold={price}'
        a.short_desc = 'OrganicBG={price}'
        a.add_button(price=20)
        a.add_button(price=50)
        a.add_button(price=100)

        a = Action(self)
        a.add_parameter('price', min=0.01, max=100.0, decimals=2)
        a.add_parameter('tax', min=0.00, max=100.0, decimals=2)
        a.desc = '''Farmers sell non-organic peaches at ${price} per ton taxed at {tax}%.'''
        a.code = 'taxprice:peachesBabyGold={price},{tax}'
        a.short_desc = 'Non-organicBG={price},{tax}'
        a.add_button(price=10, tax=0)
        a.add_button(price=40, tax=0)
        a.add_button(price=90, tax=0)

        a = Action(self)
        a.add_parameter('scale', min=0.1, max=10.0, decimals=2)
        a.desc = '''Farmers sell organic peaches at {scale} times old price.'''
        a.code = 'price:peachesOrganicBabyGold*{scale}'
        a.short_desc = 'OrganicBG*{scale}'
        a.add_button(scale=0.5)
        a.add_button(scale=2)




if __name__ == '__main__':
    actions = Actions()
    a, p = actions.find_action('price:peachesOrganicBabyGold=20.5')
    print a.get_short_desc(p)
    a, p = actions.find_action('price:peachesOrganicBabyGold*2')
    print a.get_short_desc(p)
    a, p = actions.find_action('nothing')
    print a.get_short_desc(p)


