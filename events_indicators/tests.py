from datetime import datetime
from .api_connections import RequestEventsRawData
from .models import EventData
from .models import EventLanguage
from .models import LastUpdateEventDate
from .views import populate_event_data
from quero_cultura.views import ParserYAML
import requests_mock
import json


class TestLastUpdateEventDate(object):
    def test_last_update_event_date(self):
        LastUpdateEventDate.drop_collection()
        create_date = datetime.now().__str__()
        LastUpdateEventDate(create_date).save()
        query = LastUpdateEventDate.objects.first()
        assert query.create_date == create_date


class TestEventLanguage(object):
    def test_event_language(self):
        EventLanguage.drop_collection()
        instance = "SP"
        language = "Cinema"
        EventLanguage(instance, language).save()
        query = EventLanguage.objects.first()
        assert query.instance == instance
        assert query.language == language


class TestEventData(object):
    def test_event_data(self):
        EventData.drop_collection()
        instance = "SP"
        date = datetime(2017, 11, 14, 3, 5, 55, 88000)
        age_range = "Livre"
        EventData(instance, age_range, date).save()
        query = EventData.objects.first()
        assert query.instance == instance
        assert query.date == date
        assert query.age_range == age_range


class TestPopulateEventData(object):
    @requests_mock.Mocker(kw='mock')
    def test_populate_event_data(self, **kwargs):
        parser_yaml = ParserYAML()
        urls = parser_yaml.get_multi_instances_urls

        result = [{"createTimestamp": {"date": "2012-01-01 00:00:00.000000"},
                   "terms": {"linguagem": "Cinema"},
                   "classificacaoEtaria": "livre"}]

        for url in urls:
            kwargs['mock'].get(url + "event/find/", text=json.dumps(result))

        LastUpdateEventDate.drop_collection()
        EventLanguage.drop_collection()
        EventData.drop_collection()

        populate_event_data()

        assert LastUpdateEventDate.objects.count() != 0
        assert EventData.objects.count() != 0
        assert EventLanguage.objects.count() != 0


class TestClassRequestEventsRawData(object):

    def test_success_request(self):
        current_time = datetime.now().__str__()
        request_events_raw_data = RequestEventsRawData(
            current_time, "http://mapas.cultura.gov.br/api/")
        response_events_raw_data = request_events_raw_data.response
        response_status_code = response_events_raw_data.status_code
        assert response_status_code == 200

    def test_data_content(self):
        current_time = datetime.now().__str__()
        request_events_raw_data = RequestEventsRawData(
            current_time, "http://mapas.cultura.gov.br/api/")
        events_raw_data = request_events_raw_data.data
        type_events_raw_data = type(events_raw_data)
        empty_list = []
        assert type_events_raw_data == type(empty_list)

    def test_data_lenght(self):
        current_time = datetime.now().__str__()
        request_events_raw_data = RequestEventsRawData(
            current_time, "http://mapas.cultura.gov.br/api/")
        events_raw_data = request_events_raw_data.data_length
        type_events_raw_data = type(events_raw_data)
        intenger = 1
        assert type_events_raw_data == type(intenger)
