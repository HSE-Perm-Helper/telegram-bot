from dataclasses import dataclass


@dataclass
class VerificationInfo:
    token: str
    next_attempt_in: int