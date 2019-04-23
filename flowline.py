import inspect


class Flowline(object):

    def __init__(self, name, tasks=tuple(), **kwargs):
        self.name = name
        self.tasks = tasks
        self.self_arg = self.__class__.__name__.lower()
        self.save_kwargs(kwargs)

    def run(self, context, **kwargs):
        self.save_kwargs(kwargs)
        result = None
        for result in self.walk(context):
            pass
        return result

    def walk(self, context):
        for task in self.tasks:
            if inspect.isfunction(task):
                if self.self_arg in inspect.signature(task).parameters:
                    context = task(context, flowline=self)
                else:
                    context = task(context)
        yield context

    def save_kwargs(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
