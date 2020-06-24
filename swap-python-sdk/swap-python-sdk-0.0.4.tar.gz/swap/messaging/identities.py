from swap.common.logging import logger


class ServiceRequestIdentity:
    def match(self, service_request, config):
        service_catalogue_uuid = service_request.service_catalogue_uuid
        service_name = config.name

        if service_catalogue_uuid != service_name:
            logger.info(f'ServiceRequest service_catalogue_uuid did not match, ignoring message')
            logger.info(
                f'Message for {service_catalogue_uuid} not {service_name}'
            )

            return False

        return True


class OfferExecutionRequestIdentity:
    def match(self, offer_execution_request, config):
        service_offer_name = offer_execution_request.service_offer_name
        service_name = config.name

        if service_offer_name != service_name:
            logger.info(f'OfferExecutionRequest service_offer_name did not match, ignoring message')
            logger.info(
                f'Message for {service_offer_name} not {service_name}'
            )

            return False

        service_provider_header = offer_execution_request.service_provider_header

        attributes = [
            'service_provider_uuid',
            'service_provider_signature'
        ]

        for attribute in attributes:
            offer_execution_request_attribute = getattr(service_provider_header, attribute)
            config_attribute = getattr(config, attribute)

            if offer_execution_request_attribute != config_attribute:
                logger.info(f'OfferExecutionRequest {attribute} did not match, ignoring message')
                logger.info(
                    f'Message for {offer_execution_request_attribute} not {config_attribute}'
                )

                return False

        return True
