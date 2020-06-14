# This file is part of openreviewio-py.
#
# openreviewio-py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# openreviewio-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with openreviewio-py.  If not, see <https://www.gnu.org/licenses/>

from pathlib import Path
import toml


class Content:
    """Meta class for dynamically generated content objects from OpenReviewIO standard definition."""


def constructor(self, **kwargs):
    """Function to be used as __init__() for dynamically generated objects.
    If all required arguments hasn't been filled, it raises a TypeError.
    """

    given_args = set(dict(**kwargs).keys())

    # Get dynamically created attributes
    all_attributes = set([a for a in dir(self) if not a.startswith("_")])
    required_attributes = set([a for a in all_attributes if getattr(self, a) is None])

    # Test arguments, if not all required provided, raise the ones missing
    missing_args = required_attributes.difference(given_args)
    if required_attributes.difference(given_args):
        raise TypeError(
            f"All required arguments are not implemented for {self.__name__}, "
            f"please fill: '{', '.join(missing_args)}'."
        )

    # Set arguments, if doesn't exist, raise unknown arg
    for arg in given_args:
        if arg in all_attributes:
            setattr(self, arg, dict(**kwargs).get(arg))
        else:
            raise TypeError(f"Unknown argument for {self.__name__}: {arg}")

    # Specific cases
    if "Image" in self.__name__:
        # Check mime for file extension
        file = Path(self.path_to_image)
        if file.suffix.replace(".", "") not in self.__mime__:
            raise TypeError(
                f"Image file '{file.suffix}' extension format is not valid. "
                f"Please select either: {', '.join(sorted(self.__mime__))}."
            )


# Get all contents
all_orio_classes = []
for file in Path(__file__).parent.joinpath("orio_classes").iterdir():
    # Load definition from TOML
    definition = toml.load(file)
    content = (file.stem, definition)

    # Sort them by dependencies, every inherited content follows its parent
    names = [d[0] for d in all_orio_classes]
    if definition.get("type") in names:
        parent_index = names.index(definition["type"])
        all_orio_classes.insert(parent_index + 1, content)
    else:
        all_orio_classes.insert(0, content)

# Build classes from definitions
content_classes = []
all_contents = [c for c in all_orio_classes if c[1].get("type") != "Object"]
for d in all_contents:
    # Get attributes
    if d[1].get("type") and d[1].get("type") not in ["Abstract", "Object"]:
        names = [d[0] for d in all_contents]
        parent_index = names.index(d[1].get("type"))
        parent_class = content_classes[parent_index]
    else:
        parent_class = object

    # Set definition parameters
    definition_parameters = {}
    annotations_types = {}
    for k, v in d[1].get("parameters", {}).items():
        annotations_types[k] = v
        if type(v) is dict:  # Process specificity
            if k == "optional":
                for key, val in v.items():
                    definition_parameters[key] = ""
        else:
            definition_parameters[k] = None

    # Set definition attributes
    definition_attributes = {}
    for k, v in d[1].items():
        if type(v) is not dict:
            definition_attributes[f"__{k}__"] = v

    class_attributes = {
        **{
            "__init__": constructor,
            "__name__": d[0],
            "__annotations__": annotations_types,
        },
        **definition_attributes,
        **definition_parameters,
    }

    # Generate class and add it as Content class attribute
    new_class = type(d[0], (parent_class,), class_attributes)
    setattr(Content, d[0], new_class)

    content_classes.append(new_class)
