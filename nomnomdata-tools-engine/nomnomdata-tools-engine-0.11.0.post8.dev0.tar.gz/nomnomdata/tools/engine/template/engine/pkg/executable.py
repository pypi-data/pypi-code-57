import logging

from nomnomdata.engine.api import NominodeClient
from nomnomdata.engine.components import Engine, Parameter, ParameterGroup
from nomnomdata.engine.parameters import Int, String

logger = logging.getLogger("nnd.some-cool-engine")

engine = Engine(
    uuid="CHANGE-ME-PLEASE",
    alias="Some Cool Engine",
    description="Description of your engine",
    categories=["general"],
)


@engine.action(display_name="An Action", description="Action description")
@engine.parameter_group(
    ParameterGroup(
        Parameter(
            type=Int(),
            name="integer_parameter",
            display_name="An Integer Parameter",
            description="Description of what the parameter is used for",
        ),
        Parameter(
            type=String(),
            name="string_parameter",
            display_name="A String Parameter",
            description="Description of what the parameter is used for",
        ),
        name="general_parameters",
        display_name="General Parameters",
        description="Description of the parameter group",
    )
)
def an_action(parameters):
    nominode_client = NominodeClient()
    print(parameters)


if __name__ == "__main__":
    engine.main()
