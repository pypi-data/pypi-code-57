import logging
import sentry_sdk


logger = logging.getLogger(__name__)


class SentryMixin:
    SENTRY_DSN: str = 'TESTING'

    def initialize_sentry(self, integrations=()):
        """
        Initialize sentry sdk
        """
        if self.SENTRY_DSN == "TESTING":
            logger.debug("Sentry testing mode")
        else:
            logger.debug("Using sentry.")
            sentry_sdk.init(
                dsn=self.SENTRY_DSN,
                integrations=integrations,
            )
