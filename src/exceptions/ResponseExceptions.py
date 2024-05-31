from src.exceptions.MyHTTPException import MyHTTPException


class NoResponse(MyHTTPException):
    def __init__(self, response_id: int):
        detail = f"Response with id '{response_id}' doesn't exist"
        super(NoResponse, self).__init__(detail)


class UserIsNotAuthor(MyHTTPException):
    def __init__(self, author_id: int, response_id: int, task_id: int):
        detail = f"You tried to confirm response (id='{response_id}') of task (id='{task_id}'), but author of task " \
                 f"is user with id '{author_id}'. You can't confirm responses of not yours tasks."
        super(UserIsNotAuthor, self).__init__(detail)


class TaskHasConfirmedResponse(MyHTTPException):
    def __init__(self, task_id: int, response_id: int):
        detail = f"Task with id '{task_id}' already has confirmed response: id '{response_id}'"
        super(TaskHasConfirmedResponse, self).__init__(detail)


class ResponseAlreadyConfirmed(MyHTTPException):
    def __init__(self, response_id: int):
        detail = f"Response with id '{response_id}' already confirmed"
        super(ResponseAlreadyConfirmed, self).__init__(detail)


class NotUsersResponse(MyHTTPException):
    def __init__(self, response_id: int):
        detail = f"You can't remove not yours response with id '{response_id}'"
        super(NotUsersResponse, self).__init__(detail)


class UserIsAuthorOfTask(MyHTTPException):
    def __init__(self, task_id: int):
        detail = f"You can't add response to your own task with id '{task_id}'"
        super(UserIsAuthorOfTask, self).__init__(detail)


# class ResponseException(MyHTTPException):
    # @staticmethod
    # def no_response(response_id: int):
    #     return ResponseException.http(
    #         code=404,
    #         detail=f"Response with id '{response_id}' doesn't exist"
    #     )

    # @staticmethod
    # def not_author(author_id: int, response_id: int, task_id: int):
    #     return ResponseException.http(
    #         code=404,
    #         detail=f"You tried to confirm response (id='{response_id}') of task (id='{task_id}'), but author of task "
    #                f"is user with id '{author_id}'. You can't confirm responses of not yours tasks."
    #     )

    # @staticmethod
    # def cant_confirm(task_id: int, response_id: int):
    #     return ResponseException.http(
    #         code=404,
    #         detail=f"Task with id '{task_id}' already has confirmed response: id '{response_id}'"
    #     )

    # @staticmethod
    # def already_confirmed(response_id: int):
    #     return ResponseException.http(
    #         code=404,
    #         detail=f"Response with id '{response_id}' already confirmed"
    #     )

    # @staticmethod
    # def cant_remove(response_id: int):
    #     return ResponseException.http(
    #         code=404,
    #         detail=f"You can't remove not yours response with id '{response_id}'"
    #     )

    # @staticmethod
    # def author_task(task_id: int):
    #     return ResponseException.http(
    #         code=404,
    #         detail=f"You can't add response to your own task with id '{task_id}'"
    #     )
