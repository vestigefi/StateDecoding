from typing import Optional, Dict, List
from src.common.logger import logger
from src.common.abstract import ApplicationType

# imports of Application Types
# from src.application_types.APP_KEY.APP_NAME import APP_NAME
from src.application_types import APPLICATION_TYPES


APPLICATION_TYPES_DICT: Dict[str, ApplicationType] = {
    T.get_meta()["key"]: T for T in APPLICATION_TYPES
}


def run_tests_of_applications():
    known_keys = []
    application_count = len(APPLICATION_TYPES)
    for index, application_type in enumerate(APPLICATION_TYPES):
        application_key = application_type.get_meta()["key"]
        if application_key in known_keys:
            logger.error(
                f"[ ] [{index + 1}/{application_count}] {application_key}: Application key NOT unique."
            )
            return
    for index, application_key in enumerate(APPLICATION_TYPES_DICT):
        try:
            ok = APPLICATION_TYPES_DICT[application_key].test_application_type()
            if not ok:
                raise Exception("Application test failed.")
            logger.info(
                f"[✓] [{index + 1}/{application_count}] {application_key}: Test passed."
            )
        except Exception as e:
            logger.error(
                f"[ ] [{index + 1}/{application_count}] {application_key}: Test failed: {e}"
            )


def get_application_type_by_key(application_key: str) -> Optional[ApplicationType]:
    if application_key in APPLICATION_TYPES_DICT:
        return APPLICATION_TYPES_DICT[application_key]
    return None


if __name__ == "__main__":
    run_tests_of_applications()
