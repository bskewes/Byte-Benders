## run tests by typing the following in cmd: python -m pytest
## pytest.ini specifies where all the tests are stored

import pytest

from data.stop import Stop
from data.route import Route
from data.trip import Trip
from analysis.relevant_trips import RelevantTrips

class TestValidation:

    def validate_stop_exists(self):
        
        pass

