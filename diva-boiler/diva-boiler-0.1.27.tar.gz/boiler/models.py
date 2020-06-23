"""
These models only provide the necessary properties for ingesting, exporting,
and validation of diva annotations for a SINGLE clip.  They are not intended
to map directly to stumpf models.

They are only useful internally to this library, and are intended as a
translation layer for data either before or after it exists within the stumpf
system.
"""
from typing import Any, Dict, Iterable, Iterator, List, NamedTuple, Optional, Tuple

import attr

from boiler import BoilerError
from boiler.definitions import ActivityPipelineStatuses, ActivityType, ActorType


def sort_detections(detections: List['Detection']) -> List['Detection']:
    return sorted(detections, key=lambda d: d.frame)


def get_next_keyframe(arr: List['Detection']) -> 'Detection':
    for d in arr:
        if d.keyframe:
            return d
    raise BoilerError('There are frames after the final keyframe!')


def interpolate_point(a, b, delta):
    return round(((1 - delta) * a) + (delta * b))


class Box(NamedTuple):
    left: int
    top: int
    right: int
    bottom: int

    def __and__(self, other: 'Box') -> 'Box':
        """Return intersection of two bounding boxes.

        For non-intersecting boxes, this will return a box of zero area.
        """
        left = max(self.left, other.left)
        right = min(self.right, other.right)
        top = max(self.top, other.top)
        bottom = min(self.bottom, other.bottom)
        return Box(left=left, right=max(left, right), top=top, bottom=max(top, bottom))

    @property
    def width(self) -> int:
        return self.left - self.right

    @property
    def height(self) -> int:
        return self.bottom - self.top

    @property
    def area(self) -> int:
        return self.width * self.height

    @property
    def aspect_ratio(self) -> float:
        height = self.height
        if height == 0:
            return 0
        return self.width / self.height

    @property
    def center(self) -> Tuple[float, float]:
        return (self.left + self.right) / 2, (self.top + self.bottom) / 2

    def interpolate(self, other: 'Box', distance: float) -> 'Box':
        left = interpolate_point(self.left, other.left, distance)
        top = interpolate_point(self.top, other.top, distance)
        right = interpolate_point(self.right, other.right, distance)
        bottom = interpolate_point(self.bottom, other.bottom, distance)
        return Box(left=left, top=top, right=right, bottom=bottom)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Box':
        return cls(left=d['left'], right=d['right'], top=d['top'], bottom=d['bottom'])


@attr.s(auto_attribs=True, kw_only=True, frozen=True)
class Detection:
    frame: int
    box: Box
    keyframe: bool = False

    @property
    def area(self) -> int:
        return self.box.area

    def interpolate(self, other: 'Detection', frame: int) -> 'Detection':
        distance = (frame - self.frame) / (other.frame - self.frame)
        box = self.box.interpolate(other.box, distance)
        return Detection(frame=frame, box=box, keyframe=False)


@attr.s(auto_attribs=True, kw_only=True, frozen=True, hash=False)
class Actor:
    actor_type: ActorType
    begin: int
    end: int
    detections: List[Detection] = attr.ib(converter=sort_detections)
    actor_id: int

    @property
    def keyframes(self):
        return filter(lambda d: d.keyframe, self.detections)

    def pruned(self) -> 'Actor':
        return attr.evolve(self, detections=list(self.keyframes))

    # Used for deduplicating lists of actors when serializing
    def __hash__(self) -> int:
        first_detection = None
        if self.detections:
            first_detection = self.detections[0]
        return hash((self.actor_type.value, self.begin, self.end, first_detection))


@attr.s(auto_attribs=True, kw_only=True, frozen=True)
class Activity:
    activity_type: ActivityType
    begin: int
    end: int
    actors: List[Actor]
    activity_id: int
    status: Optional[ActivityPipelineStatuses] = None

    def pruned(self) -> 'Activity':
        actors = [a.pruned() for a in self.actors]
        return attr.evolve(self, actors=actors)


@attr.s(auto_attribs=True, kw_only=True, frozen=True)
class ActivityList:
    activity_map: Dict[int, Activity] = attr.ib()
    actor_map: Dict[int, Actor] = attr.ib()

    @classmethod
    def create_from_activity_list(cls, activities: Iterable[Activity]) -> 'ActivityList':
        activity_map: Dict[int, Activity] = {}
        actor_map: Dict[int, Actor] = {}

        # TODO: The data model used for actors doesn't perfectly match with
        # either the database or annotation files.  The files themselves store
        # multiple "tracks" which can be joined by actor_id.  Instead of an
        # explicit "track_id", they use an (activity_id, actor_id) pair with
        # detections associated with that pair.  In the boiler representation,
        # there is no way to distinguish detections associated with a specific
        # "track" in this sense, so the frame range for which an actor is
        # involved in an activity is lost.  As a work around, we generate a new
        # actor_id for actors containing more than one track.  In practice,
        # this is rare.
        max_actor_id = 0

        for activity in activities:
            for actor in activity.actors:
                max_actor_id = max(actor.actor_id, max_actor_id)

        for activity in activities:
            if activity.activity_id in activity_map:
                raise Exception('Duplicate activity_ids detected')

            actors: List[Actor] = []
            for actor in activity.actors:
                if actor.actor_id in actor_map and actor != actor_map[actor.actor_id]:
                    max_actor_id += 1
                    actor_id = max_actor_id
                else:
                    actor_id = actor.actor_id

                actors.append(attr.evolve(actor, actor_id=actor_id))
                actor_map[actor_id] = actor

            activity_map[activity.activity_id] = attr.evolve(activity, actors=actors)

        return cls(activity_map=activity_map, actor_map=actor_map)

    @property
    def activity_types(self) -> Dict[ActivityType, Iterable[Activity]]:
        # TODO: make this more efficient
        activity_types = {a.activity_type for a in self.activity_map.values()}
        return {
            at: list(filter(lambda a: a.activity_type == at, self.activity_map.values()))
            for at in activity_types
        }

    def __iter__(self) -> Iterator[Activity]:
        for activity in self.activity_map.values():
            yield activity

    def __len__(self) -> int:
        return len(self.activity_map)
