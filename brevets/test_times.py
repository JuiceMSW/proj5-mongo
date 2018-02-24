import nose
import acp_times

"""
	According to ACP Rules a Control Point at Zero Has a Open Time at Brevet Start Time
	and Close Time at Brevet Start Time + 1 Hour
"""
def test_zero_control():
	test_open = acp_times.open_time(0, 200, "2017-01-01 00:00") == "2017-01-01T00:00:00+00:00"
	test_close = acp_times.close_time(0, 200, "2017-01-01 00:00") == "2017-01-01T01:00:00+00:00"
	assert test_open and test_close

"""
	According to ACP Rules a Control Point Less Than or Equal to 20% Longer than the Brevet Distance
	has Open and Close times equal to the Open and Close times at the Brevet Distance 
"""
def test_less_than_20_percent_longer():
	test_open = acp_times.open_time(210, 200, "2017-01-01 00:00") == acp_times.open_time(200, 200, "2017-01-01 00:00")
	test_close = acp_times.close_time(210, 200, "2017-01-01 00:00") == acp_times.close_time(200, 200, "2017-01-01 00:00")
	assert test_open and test_close

"""
	The ACP Calculator throws an Error when a Control Point is More than 20% Longer than the Brevet Distance
"""
def test_more_than_20_percent_longer():
	test_open = acp_times.open_time(300, 200, "2017-01-01 00:00") == acp_times.open_time(200, 200, "2017-01-01 00:00")
	test_close = acp_times.close_time(300, 200, "2017-01-01 00:00") == acp_times.close_time(200, 200, "2017-01-01 00:00")
	assert not test_open and not test_close

"""
	The ACP Calculator throws an Error when a Control Point has a Negative Distance
"""
def test_negative_control():
	test_open = "Error" in acp_times.open_time(-10, 200, "2017-01-01 00:00")
	test_close = "Error" in acp_times.close_time(-10, 200, "2017-01-01 00:00") 
	assert test_open and test_close

"""
	Works with Different Brevet Distances
	These times match those given by the Official ACP Caluclator
"""
def test_different_brevets():
	test_open_300 = acp_times.open_time(210, 300, "2017-01-01 00:00") == "2017-01-01T06:11:41.470588+00:00"
	test_close_300 = acp_times.close_time(210, 300, "2017-01-01 00:00") == "2017-01-01T14:00:00+00:00"
	test_open_400 = acp_times.open_time(310, 400, "2017-01-01 00:00") == "2017-01-01T09:19:11.470588+00:00"
	test_close_400 = acp_times.close_time(310, 400, "2017-01-01 00:00") == "2017-01-01T20:40:00+00:00"
	assert test_open_300 and test_close_300 and test_open_400 and test_close_400


"""
	If the Open or Close time is Greater than 24 hours it Correctly Changes Date and Time
"""
def test_date_change():
	test_open = acp_times.open_time(200, 300, "2017-01-01 23:00") == "2017-01-02T04:52:56.470588+00:00"
	test_close = acp_times.close_time(200, 300, "2017-01-01 23:00") == "2017-01-02T12:20:00+00:00"



