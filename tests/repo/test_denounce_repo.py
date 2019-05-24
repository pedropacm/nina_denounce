import pytest

from nina_denounce.repo.denounce_repo import DenounceRepo, Denounce

def test_create_denounce():
	denounce_repo = DenounceRepo()

	denounce = Denounce()
	denounce.lat = "3.7255483"
	denounce.lon = "-38.5280283"
	denounce.bus_number = "12345"

	retrieved_denounce = denounce_repo.save(denounce)

	assert denounce.lat == retrieved_denounce.lat
	assert denounce.lon == retrieved_denounce.lon
	assert denounce.bus_number == retrieved_denounce.bus_number