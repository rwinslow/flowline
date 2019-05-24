import inspect
import logging
import sys


logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


class Flowline(object):
    """Flowline Python workflow engine.

    Accepts a single object as a context at runtime. Each task is called in
    order where the returned value from each task is passed to the following
    one in the workflow.

    All additional kwargs given at instantiation or runtime are stored within
    identically named attributes within the Flowline instance.

    Tasks may be:
    - Functions that take one argument that will store the context. An
        optional second argument named `flowline` may be added as a reference
        to the parent Flowline for store and access to constants.
    - Task object declarations with a run method defined.
    - Task object instances with a run method defined.
    - Flowline instances with defined tasks.
    """

    def __init__(self, name, tasks=tuple(), verbose=False, **kwargs):
        self.name = name
        self.tasks = tasks
        self.self_arg = self.__class__.__name__.lower()
        self.verbose = verbose
        self.save_kwargs(kwargs)

    def run(self, context, **kwargs):
        """Run Flowline with all tasks.

        Args:
            context (object): Input object that is passed to the first task.
            **kwargs (object): Objects to be stored within identically named
                attributes within the Flowline instance.

        Returns:
            result (object): Last returned result from the last task.
        """
        result = None
        for result in self.walk(context, **kwargs):
            pass
        return result

    def walk(self, context, **kwargs):
        """Iterator that steps through each task in the Flowline.

        Args:
            context (object): Input object that is passed to the first task.
            **kwargs (object): Objects to be stored within identically named
                attributes within the Flowline instance.

        Yields:
            result (object): Returned result from each called task.
        """
        self.save_kwargs(kwargs)
        for task in self.tasks:
            # Function.
            if inspect.isfunction(task):
                # Logging.
                self.logger.info("Running {}".format(task.__name__))

                # Call with appropriate args.
                if self.self_arg in inspect.signature(task).parameters:
                    context = task(context, flowline=self)
                else:
                    context = task(context)

            # Class declaration.
            elif isinstance(task, type):
                # Instantiation.
                if self.self_arg in inspect.signature(task).parameters:
                    task_inst = task(flowline=self)
                else:
                    task_inst = task()

                # Logging.
                if getattr(task_inst, "name", False):
                    name = task_inst.name
                else:
                    name = task.__class__.__name__
                self.logger.info("Running {}".format(name))

                # Run insertion point with appropriate args.
                if self.self_arg in inspect.signature(task.run).parameters:
                    context = task_inst.run(context, flowline=self)
                else:
                    context = task_inst.run(context)

            # Class instance.
            elif not isinstance(task, type):
                # Logging.
                self.logger.info("Running {}".format(task.__class__.__name__))

                # Run insertion point with appropriate args.
                if self.self_arg in inspect.signature(task.run).parameters:
                    context = task.run(context, flowline=self)
                else:
                    context = task.run(context)

            yield context

    def save_kwargs(self, kwargs):
        """Save given kwargs as identically named instance attributes.

        Args:
            kwargs (object): Objects to be stored within identically named
                attributes within the Flowline instance.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        if self.verbose:
            logger.setLevel(logging.DEBUG)
        return logger
