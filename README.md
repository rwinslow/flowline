# Flowline Python workflow engine.

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

## Installation

From the command line or your virtual environment, run

```python
pip install git+https://github.com/rwinslow/flowline.git
```

## Usage

```python
from flowline import Flowline, Task


# Tasks can inherit from Task for complicated logic.
class TestTask(Task):
    def run(self, num):
        return num + self.get_num()

    def get_num(self):
        return 4

# Tasks can be your own class as long as it has a run method with one arg.
class SimpleTask(object):
    def __init__(self, add_value=3):
        self.add_value = add_value

    # You can optionally include a flowline arg to get a reference to the
    # operating Flowline.
    def run(self, num, flowline):
        return num + self.add_value + flowline.add_value

# Tasks can be instanced as long as they have a run method with one arg.
simple_task_instance = SimpleTask(2)

# Tasks can be a simple function with one arg.
def test_task_function(num):
    return num + 1

# Task functions can optionally include a flowline arg to get a reference to
# the operating Flowline.
def test_task_function_full(num, flowline):
    return num + flowline.add_value

# Tasks can even be entire Flowlines.
intermediate_flowline = Flowline(
    name='Intermediate',
    tasks=[test_task_function],
    verbose=True
)

# You instance the flowline with your predefined tasks and any values that may
# need to be accessed by tasks.
play = Flowline(
    name='All types of functionality',
    tasks=[
        TestTask,                # 1 (Given on run) + 4 (Hard coded) = 5
        simple_task_instance,    # 5 + 2 (Class init) + 3 (Flowline attr) = 10
        SimpleTask,              # 10 + 3 (Init kwarg) + 3 (Flowline attr) = 16
        test_task_function,      # 16 + 1 (Hard coded) = 17
        intermediate_flowline,   # 17 + 1 (From function) = 18
        test_task_function_full  # 18 + 3 (Flowline attribute) = 21
    ],
    add_value=3,
    verbose=True  # To see operational logs.
)

# Then you run it and get your result.
result = play.run(1)

# You can even walk through each task independently and see the intermediate
# results.
for value in play.walk(1):
    print(value)
```
