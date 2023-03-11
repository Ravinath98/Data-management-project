from wtforms import Form, BooleanField

def wrapper_func(list_a):
    class Prefs(Form):
        pass

    for ele in list_a:
        setattr(Prefs, ele, BooleanField(ele))

    return Prefs