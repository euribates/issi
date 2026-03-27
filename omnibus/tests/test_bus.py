#!/usr/bin/env python3

from dataclasses import dataclass
import pytest

from omnibus.bus import Bus, Evento
from unittest.mock import Mock


class FaKeMessages:

    def __init__(self):
        self.messages = []
        self.last_level = None

    def __len__(self):
        return len(self.messages)

    def last_message(self):
        return self.messages[-1]

    def debug(self, request, message):
        self.messages.append(message)
        self.last_level = 'debug'

    def info(self, request, message):
        self.messages.append(message)
        self.last_level = 'info'
        
    def success(self, request, message):
        self.messages.append(message)
        self.last_level = 'success'

    def warning(self, request, message):
        self.messages.append(message)
        self.last_level = 'warning'
        
    def error(self, request, message):
        self.messages.append(message)
        self.last_level = 'error'


@pytest.fixture
def dummy_bus():
    fake_request = Mock(user=Mock(username='jileon'))
    return Bus(fake_request, FaKeMessages())


def test_create_bus(dummy_bus):
    assert dummy_bus.username == 'jileon'


@dataclass
class FakeModel:

    pk: int
    texto: str

    def __str__(self):
        return self.texto


@pytest.mark.django_db
def test_bus_publica(dummy_bus):

    item = FakeModel(pk=1, texto="Test Fake model")
    msg = f'Mensaje sobre "{item}" de tipo **debug**'
    dummy_bus.publica(item, msg, 'debug')

    assert len(dummy_bus.messages) == 1
    assert dummy_bus.messages.last_message() == (
        '<p>Mensaje sobre &quot;Test Fake model&quot;'
        ' de tipo <strong>debug</strong></p>'
        )
    assert dummy_bus.messages.last_level == 'debug'
    event = Evento.objects.filter(sujeto=1, nombre_clase='FakeModel')
    assert event.exists()

if __name__ == "__main__":
    pytest.main()
