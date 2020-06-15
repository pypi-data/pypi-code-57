# -*- coding: utf-8 -*-
""" mindstone.

The mindstone package offers an easy to use framework for creating control systems.
This package houses a collection of tools that make it possible
for a remote processing source to control a local actor.

The package defines two entities. The first being whats known as a driver. This entity
interfaces directly with a given platform, such as a Raspberry Pi micro-controller,
and acts as a bridge between said platform and a higher functioning controller.
The other entity is the controller. The controller handles most of the processing and
defines the behaviours and protocols by which a driver operates. The controller does
this by processing abjects called gates that are connected to each other, forming a network.
These gates represent simple processes that can be that can be ordered and arranged in
different ways to produce different behaviours. Gates also allow users to extend the
functions of a control system by allowing users to embed their own custom-made functions
and operations into the network.

Example:
    On the driver side, the mindstone package can be used to start a new driver by running
    the following command:

        & python3 mindstone/run.py raspberry --port=5000 --hostname="10.0.0.2"

     where 'raspberry' is the platform.


 TODO: Implement engines (spacial awareness, reasoning and knowledge-base engines)
 TODO: Complete source code documentation
"""
