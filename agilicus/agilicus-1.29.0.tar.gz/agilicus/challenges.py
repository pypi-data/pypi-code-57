import agilicus

from . import context


def create_challenge(ctx, user_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    spec = agilicus.ChallengeSpec(user_id=user_id, **kwargs)
    challenge = agilicus.Challenge(spec=spec)

    resp = apiclient.challenges_api.create_challenge(challenge)
    return resp


def replace_challenge(ctx, challenge_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    existing = apiclient.challenges_api.get_challenge(challenge_id)

    spec_as_dict = existing.spec.to_dict()
    spec_as_dict.update(kwargs)
    spec = agilicus.ChallengeSpec(**spec_as_dict)
    existing.spec = spec

    resp = apiclient.challenges_api.replace_challenge(challenge_id, existing)
    return resp


def get_challenge(ctx, challenge_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    resp = apiclient.challenges_api.get_challenge(challenge_id)
    return resp


def delete_challenge(ctx, challenge_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    resp = apiclient.challenges_api.delete_challenge(challenge_id)
    return resp
