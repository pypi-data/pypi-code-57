import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from requests import HTTPError

from forge_template.exception.exceptions import AccessDeniedException
from forge_template.tool_info import ToolInfo

NOT_FOUND_CODE = 404
UNAUTHORIZED_CODE = 401
FORBIDDEN_CODE = 403
BAD_REQUEST_CODE = 400


class BaseHandler(ABC):
    def __init__(self, config: Dict[str, Any], tool_info: ToolInfo):
        self.name = tool_info.name
        self.capitalized_name = tool_info.name.capitalize()
        self.config = config
        self.tool_info = tool_info

    def __run_function(self, f: Callable, text: str, print_footer: bool = False, should_rollback: bool = False) -> None:
        header = f"{text}"
        logging.info(header)
        try:
            f(self)
        except HTTPError as e:
            status = e.response.status_code
            if status in [UNAUTHORIZED_CODE, FORBIDDEN_CODE]:
                raise AccessDeniedException(
                    f"Access denied. Please check your {self.capitalized_name} access token. Details: {e}"
                )
            self.__handle_rollback(should_rollback=should_rollback)
            raise
        except Exception:
            self.__handle_rollback(should_rollback=should_rollback)
            raise

        if print_footer:
            footer = "-" * len(header)
            logging.info(footer)

    def __handle_rollback(self, should_rollback: bool) -> None:
        if should_rollback:
            self.rollback()

    def run_setup(self) -> None:
        text = f"\nCreating/Updating resources for {self.capitalized_name} ..."
        self.__run_function(lambda handler: handler.setup(), text, should_rollback=True)

    @abstractmethod
    def setup(self) -> None:
        pass

    def run_create_preview(self) -> None:
        text = f"\nCreating preview of resource creation/updates for {self.capitalized_name} ..."
        self.__run_function(lambda handler: handler.create_preview(), text)

    @abstractmethod
    def create_preview(self) -> None:
        pass

    def run_print_preview(self) -> None:
        text = f"\n{self.name} preview".upper()
        self.__run_function(lambda handler: handler.print_preview(), text)

    @abstractmethod
    def print_preview(self) -> None:
        pass

    def run_rollback(self) -> None:
        text = f"\nRolling back {self.capitalized_name} due to creation/update error"
        self.__run_function(lambda handler: handler.rollback(), text)

    @abstractmethod
    def rollback(self) -> None:
        pass

    def perform_action(self, action: Callable, should_rollback: bool = True) -> Any:
        try:
            return action(self)
        except HTTPError as e:
            if e.response.status_code == FORBIDDEN_CODE:
                raise AccessDeniedException(f"Access denied. Please check your {self.capitalized_name} access token.")
            if should_rollback:
                self.rollback()
            raise e
        except RuntimeError as e:
            if should_rollback:
                self.rollback()
            raise e

    def run_delete_all_resources(self):
        text = f"\nDeleting all resources for {self.capitalized_name} ..."
        self.__run_function(lambda handler: handler.delete_all_resources(), text)

    @abstractmethod
    def delete_all_resources(self):
        pass

    @staticmethod
    def get_dict_list_subtraction(d: Dict, l: List) -> Dict:
        return {e: d[e] for e in set(d) - set(l)}
