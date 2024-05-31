from src.exceptions.MyHTTPException import MyHTTPException


class NoTask(MyHTTPException):
    def __init__(self, task_id: int):
        detail = f"Task with id '{task_id}' doesn't exist"
        super(NoTask, self).__init__(detail)


class UnlinkedCollar(MyHTTPException):
    def __init__(self, collar_id: int):
        detail = f"Collar with id '{collar_id}' doesn't have any linked dog, so task can't be added to this collar"
        super(UnlinkedCollar, self).__init__(detail)


class TooShortText(MyHTTPException):
    def __init__(self):
        detail = "Transmitted text must be longer than 10 symbols"
        super(TooShortText, self).__init__(detail)


class NotUsersTask(MyHTTPException):
    def __init__(self, task_id: int):
        detail = f"You can't remove not yours task with id '{task_id}'"
        super(NotUsersTask, self).__init__(detail)


class TaskHasResponses(MyHTTPException):
    def __init__(self, task_id: int):
        detail = f"Task with id '{task_id}' has responses and can't be removed"
        super(TaskHasResponses, self).__init__(detail)
