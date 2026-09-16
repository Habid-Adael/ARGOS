context = {
    "last_app": None,
    "last_subject": None,
    "last_response": None,
    "last_person": None,
    "last_tool": None,
}


def set_last_app(app):
    context["last_app"] = app


def get_last_app():
    return context["last_app"]


def set_subject(subject):
    context["last_subject"] = subject


def get_subject():
    return context["last_subject"]


def set_response(response):
    context["last_response"] = response


def get_response():
    return context["last_response"]


def set_person(person):
    context["last_person"] = person


def get_person():
    return context["last_person"]


def set_tool(tool):
    context["last_tool"] = tool


def get_tool():
    return context["last_tool"]


def clear():

    context["last_app"] = None
    context["last_subject"] = None
    context["last_response"] = None
    context["last_person"] = None
    context["last_tool"] = None