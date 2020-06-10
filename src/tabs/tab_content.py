import dash_bootstrap_components as dbc


class TabContent:
    def get_title(self):
        pass

    def get_desc(self):
        pass

    def get_form_data(self):
        pass

    def get_bad_figure(self):
        pass

    def get_good_figure(self):
        pass


class ExampleTabContent(TabContent):
    def get_title(self):
        return "This is title"

    def get_desc(self):
        return """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        """

    def get_form_data(self):
        return [
            ("Is this a question?", "text"),
            ("How you like it in 1-10 scale?", "number"),
            ("How are you?", "text"),
            ("Is this real?", "text"),
            ("Why?", "text")
        ]

        return [
            dbc.FormGroup([
                dbc.Label("{}. {}".format(nr + 1, data[0])),
                dbc.Input(type=data[1], placeholder="Put your answer here...")
            ])
            for nr, data in enumerate(form_data)
        ]

    def get_bad_figure(self):
        return {
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'hue'},
            ],
            'layout': {
                'title': 'BAAAAAD'
            }
        }

    def get_good_figure(self):
        return {
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'GOOOD'
            }
        }
