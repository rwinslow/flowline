from flowline import Flowline, Task


class TestTask(Task):
    pass

def test_task_function(context):
    return context

def test_task_function_full(context, flowline):
    if flowline:
        print('Flowline reference given.')
    return context

test_task_inst = TestTask(None)

test_flowline = Flowline(
    name='Test',
    tasks=[
        TestTask,
        test_task_inst,
        test_task_function,
        test_task_function_full
    ],
    verbose=True
)

if __name__ == '__main__':
    result = test_flowline.run(True)
    assert result
