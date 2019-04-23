import inspect


class Flowline(object):
    def __init__(self, name, tasks=tuple(), **kwargs):
        self.name = name
        self.tasks = tasks
        for key, value in kwargs.items():
            setattr(self, key, value)

    def run(self, context):
        for context in self.walk(context):
            pass
        return context

    def walk(self, context):
        for task in self.tasks:
            if inspect.isfunction(task):
                if 'flowline' in inspect.signature(task).parameters:
                    context = task(context, flowline=self)
                else:
                    context = task(context)
        yield context
