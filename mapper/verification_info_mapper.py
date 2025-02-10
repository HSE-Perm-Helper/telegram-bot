from model.verification_info import VerificationInfo


def from_json(json: dict) -> VerificationInfo:
    return VerificationInfo(
        token=json["token"],
        next_attempt_in=json["nextAttemptIn"],
    )