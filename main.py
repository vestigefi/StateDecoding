from typing import Optional
from src.common._abstract import ApplicationType
from src._TMP import Template


APPLICATION_TYPES = {
    "0TMP": Template,
}


def get_application_type_by_id(application_type_id: str) -> Optional[ApplicationType]:
    if application_type_id in APPLICATION_TYPES:
        return APPLICATION_TYPES[application_type_id]
    return None
