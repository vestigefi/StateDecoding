from typing import List
from src.common.abstract import ApplicationType

# add your application type here
from src.application_types.TEMPLATE.main import Template
from src.application_types.HMBLFARM.main import HumbleFarm
from src.application_types.PACTFARM.main import PactFarm

APPLICATION_TYPES: List[ApplicationType] = [Template, HumbleFarm, PactFarm]
