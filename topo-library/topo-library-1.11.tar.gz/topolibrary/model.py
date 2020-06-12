"""Mongo data models."""


from mongoengine.fields import (Document, StringField, DateTimeField,
                                ListField, IntField, EmbeddedDocument,
                                EmbeddedDocumentListField, BooleanField,
                                DictField, FloatField)


class RepoEvents(Document):
    """The repository events collection model.

    Attributes:
        event_type (StringField): The GitHub event type https://developer.github.com/v3/activity/event_types
        repo_name (StringField): The full name of the GitHub repo.
        timestamp (DateTimeField): The datetime timestamp of the event.
    """

    meta = {'allow_inheritance': True}

    # Static list of valid event types
    valid_event_types = ("ReleaseEvent", "PushEvent", "PullRequestEvent")

    # Crawler fields
    event_type = StringField(required=True, choices=valid_event_types)
    repo_name = StringField(required=True)
    timestamp = DateTimeField(required=True)

    def __init__(self, **kwargs):
        """Pass any init parameters to the Document class."""
        Document.__init__(self, **kwargs)


class LinterScanEvent(EmbeddedDocument):
    """A sub-document for static analysis events.

    Attributes:
        linter_name (StringField): The name of the linter that ran against the file.
        file_path (StringField): The full path of the file in the repo.
        errors_total (IntField): Total number of errors.
        warnings_total (IntField): Total number of warnings.
        linter_output (StringField): Full output from the linter.
    """
    linter_name = StringField()
    file_path = StringField()
    errors_total = IntField()
    warnings_total = IntField()
    linter_output = StringField()

    def __init__(self, **kwargs):
        """Pass any init parameters to the Document class."""
        EmbeddedDocument.__init__(self, **kwargs)


class ReleaseEvent(RepoEvents):
    """The GitHub release events model."""

    def __init__(self, **kwargs):
        RepoEvents.__init__(self, **kwargs)
        self.event_type = "ReleaseEvent"


class PullRequestEvent(RepoEvents):
    """The GitHub pull requests events model."""

    sha = StringField(required=True)
    ref = StringField(required=True, null=True)

    merged = BooleanField(required=True)
    commits = IntField(required=True)
    additions = IntField(required=True)
    deletions = IntField(required=True)
    changed_files = IntField(required=True)

    def __init__(self, **kwargs):
        RepoEvents.__init__(self, **kwargs)
        self.event_type = "PullRequestEvent"


class PushEvent(RepoEvents):
    """The GitHub push events model.

    Attributes:
        sha (StringField): The SHA of the most recent commit on ref after the push.
        ref (StringField): The full git ref that was pushed. Example: refs/heads/master.
        content_flags (ListField, optional): Flags that matched the file content rules.
        filename_flags (ListField, optional): Flags that matched the filename rules.
        LinterScanEvents (Document): A sub-document for static analysis events.
    """

    # Push fields
    sha = StringField(required=True)
    ref = StringField(required=True)

    # Crawler flags
    actor = DictField()
    aspect_flags = ListField()
    filename_flags = ListField()
    files = ListField()

    # Linter fields
    linter_warnings_total = IntField()
    linter_errors_total = IntField()
    linter_events = EmbeddedDocumentListField(LinterScanEvent)

    # Analysis fields
    investment_kpi = FloatField()
    maturity_kpi = FloatField()
    quality_kpi = FloatField()
    risk_kpi = FloatField()
    velocity_kpi = FloatField()
    infra_kpi = FloatField()

    def __init__(self, **kwargs):
        RepoEvents.__init__(self, **kwargs)
        self.event_type = "PushEvent"


class PipelineRun(Document):
    name = StringField(max_length=120, required=True)
    number = IntField()
    repo = StringField(max_length=200)
    branch = StringField(max_length=50)
    buildnumber = IntField(required=True)
    building = BooleanField()
    durationMillis = IntField()
    result = StringField(max_length=50)
    timestamp = IntField(max_length=50)
    url = StringField(max_length=50)
    fail_stage = StringField(max_length=50)
    fail_logs = StringField(max_length=10000)
    tags = ListField(StringField(max_length=30))
    meta = {
        'indexes': [
            'name'
        ]
    }
