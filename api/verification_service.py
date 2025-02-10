from api.utils import post_request, get_request
from exception.verification.cannot_resent_email_by_attempts_exception import CanNotResentEmailByAttemptsException
from exception.verification.cannot_resent_email_by_delay_exception import CannotResentEmailByDelayException
from exception.verification.verification_request_not_found_exception import VerificationRequestNotFoundException
from mapper import verification_info_mapper
from model.verification_info import VerificationInfo


async def resend_verification(token: str) -> VerificationInfo:
    response = await post_request(path=f"/verification/{token}")

    if response.status_code == 400:
        response = await get_request(path=f"/verification/{token}")
        info = verification_info_mapper.from_json(response.json())

        if info.next_attempt_in is None:
            raise CanNotResentEmailByAttemptsException()

        raise CannotResentEmailByDelayException(info.next_attempt_in)

    if response.status_code == 404:
        raise VerificationRequestNotFoundException()

    return verification_info_mapper.from_json(response.json())