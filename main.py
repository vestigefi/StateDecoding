from typing import Optional, Dict
from src.common.logger import logger
from src.common.abstract import ApplicationType

# imports of Application Types
# from src.APP_KEY import APP_NAME
from src.common.TMPL import Template


APPLICATION_TYPES: Dict[str, ApplicationType] = {
    Template.get_meta()['key']: Template,
}


def run_tests_of_applications():
    application_count = len(APPLICATION_TYPES)
    for index, application_key in enumerate(APPLICATION_TYPES):
        try:
            ok = APPLICATION_TYPES[application_key].test_application_type()
            if not ok:
                raise Exception("Application test failed.")
            logger.info(
                f"[✓] [{index + 1}/{application_count}] {application_key}: Test passed."
            )
        except Exception as e:
            logger.info(
                f"[ ] [{index + 1}/{application_count}] {application_key}: Test failed: {e}"
            )


def get_application_type_by_key(application_key: str) -> Optional[ApplicationType]:
    if application_key in APPLICATION_TYPES:
        return APPLICATION_TYPES[application_key]
    return None


if __name__ == "__main__":
    run_tests_of_applications()
