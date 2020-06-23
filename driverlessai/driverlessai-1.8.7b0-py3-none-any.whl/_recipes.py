"""Recipe module of official Python client for Driverless AI."""

import re
from typing import Any, List

from driverlessai import _core
from driverlessai import _utils


class ModelRecipe:
    """Interact with a model recipe on the Driverless AI server.

    Attributes:
        name (str): recipe name
        is_custom (bool): ``True`` if the recipe is custom
    """

    def __init__(self, info: Any) -> None:
        if info.is_custom:
            self.name = info.name + " Model"
        else:
            self.name = info.name
        self.is_custom = info.is_custom

    def __repr__(self) -> str:
        return f"{self.__class__} {self!s}"

    def __str__(self) -> str:
        return self.name


class ModelRecipes:
    """Interact with model recipes on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> List["ModelRecipe"]:
        """Return list of model recipe objects."""
        return [ModelRecipe(m) for m in self._client._backend.list_model_estimators()]


class RecipeJob(_utils.ServerJob):
    """Monitor creation of a custom recipe on the Driverless AI server.

    Attributes:
        key: unique ID of job
    """

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)

    def _update(self) -> None:
        self._info = self._client._backend.get_custom_recipe_job(self.key)

    def result(self, silent: bool = False) -> "RecipeJob":
        """Wait for job to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self

    def status(self, verbose: int = 0) -> str:
        """Return job status string.

        Args:
            verbose:
                - 0: short description
                - 1: short description with progress percentage
                - 2: detailed description with progress percentage
        """
        status = self._status()
        if verbose == 1:
            return f"{status.message} {self._info.progress:.2%}"
        if verbose == 2:
            if status == _utils.JobStatus.FAILED:
                message = " - " + self._info.error
            else:
                message = ""  # message for recipes is partially nonsense atm
            return f"{status.message} {self._info.progress:.2%}{message}"
        return status.message


class Recipes:
    """Create and interact with recipes on the Driverless AI server.

    Attributes:
        models (ModelRecipes): see model recipes
        scorers (ScorerRecipes): see scorer recipes
        transformers (TransformerRecipes): see transformer recipes
    """

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self.models = ModelRecipes(client)
        self.scorers = ScorerRecipes(client)
        self.transformers = TransformerRecipes(client)

    def create(self, recipe: str) -> None:
        """Create a recipe on the Driverless AI server.

        Args:
            recipe: path to recipe or url for recipe
        """
        self.create_async(recipe).result()
        return

    def create_async(self, recipe: str) -> RecipeJob:
        """Launch creation of a recipe on the Driverless AI server.

        Args:
            recipe: path to recipe or url for recipe
        """
        if re.match("^http[s]?://", recipe):
            key = self._client._backend.create_custom_recipe_from_url(recipe)
        else:
            key = self._client._backend._perform_recipe_upload(recipe)
        return RecipeJob(self._client, key)


class ScorerRecipe:
    """Interact with a scorer recipe on the Driverless AI server.

    Attributes:
        name (str): recipe name
        description (str): recipe description
        for_binomial (bool): ``True`` if scorer works for binomial models
        for_multiclass (bool): ``True`` if scorer works for multiclass models
        for_regression (bool): ``True`` if scorer works for regression models
        is_custom (bool): ``True`` if the recipe is custom
    """

    def __init__(self, info: Any) -> None:
        self.name = info.name
        self.description = info.description
        self.for_binomial = info.for_binomial
        self.for_multiclass = info.for_multiclass
        self.for_regression = info.for_regression
        self.is_custom = info.is_custom

    def __repr__(self) -> str:
        return f"{self.__class__} {self!s}"

    def __str__(self) -> str:
        return self.name


class ScorerRecipes:
    """Interact with scorer recipes on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> List["ScorerRecipe"]:
        """Return list of scorer recipe objects."""
        return [ScorerRecipe(s) for s in self._client._backend.list_scorers()]


class TransformerRecipe:
    """Interact with a transformer recipe on the Driverless AI server.

    Attributes:
        name (str): recipe name
        is_custom (bool): ``True`` if the recipe is custom
    """

    def __init__(self, info: Any) -> None:
        self.name = info.name
        self.is_custom = info.is_custom

    def __repr__(self) -> str:
        return f"{self.__class__} {self!s}"

    def __str__(self) -> str:
        return self.name


class TransformerRecipes:
    """Interact with transformer recipes on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> List["TransformerRecipe"]:
        """Return list of transformer recipe objects."""
        return [TransformerRecipe(t) for t in self._client._backend.list_transformers()]
