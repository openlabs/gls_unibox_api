#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_gls_unibox_api
----------------------------------

Tests for `gls_unibox_api` module.
"""
import os
import logging
from decimal import Decimal
from datetime import date, time

import pytest

from gls_unibox_api import fields
from gls_unibox_api.api import Response, Client, Shipment, logger

logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class TestForm(object):
    f_char = fields.Char('f_char')
    f_int = fields.Int('f_int')
    f_long = fields.Long('f_long')
    f_decimal = fields.Decimal('f_decimal')
    f_date = fields.Date('f_date')
    f_date2 = fields.Date('f_date2', separator='.')
    f_time = fields.Time('f_time')


@pytest.fixture
def test_form():
    test_form = TestForm()
    test_form.values = {
        'f_char': 'hello world',
        'f_int': '1',
        'f_long': '1234567890987654321',
        'f_decimal': '12345,6',
        'f_date': '13121987',
        'f_date2': '13.12.1987',
        'f_time': '11:10',
    }
    return test_form


class TestFields:

    def test_char_field(self, test_form):
        assert test_form.f_char == 'hello world'

        # Set a new value and check
        new_value = 'hello'
        test_form.f_char = new_value
        assert test_form.f_char == new_value

    def test_int_field(self, test_form):
        assert test_form.f_int == 1

        # Set a new value and check
        new_value = 100
        test_form.f_int = new_value
        assert test_form.f_int == new_value

    def test_long_field(self, test_form):
        assert test_form.f_long == 1234567890987654321

        # Set a new value and check
        new_value = 1234567890123456
        test_form.f_long = new_value
        assert test_form.f_long == new_value

    def test_decimal_field(self, test_form):
        assert test_form.f_decimal == Decimal('12345.6')

        # Set a new value and check
        new_value = Decimal('12345.78')
        test_form.f_decimal = new_value
        assert test_form.f_decimal == new_value

    def test_date_field(self, test_form):
        assert test_form.f_date == date(1987, 12, 13)

        # Set a new value and check
        new_value = date(2009, 7, 1)
        test_form.f_date = new_value
        assert test_form.f_date == new_value

    def test_date2_field(self, test_form):
        assert test_form.f_date2 == date(1987, 12, 13)

        # Set a new value and check
        new_value = date(2009, 7, 1)
        test_form.f_date2 = new_value
        assert test_form.f_date2 == new_value

    def test_time_field(self, test_form):
        assert test_form.f_time == time(11, 10)

        # Set a new value and check
        new_value = time(10, 30)
        test_form.f_time = new_value
        assert test_form.f_time == new_value


@pytest.fixture
def client():
    return Client('217.7.25.136', '3030', test=True)


@pytest.fixture
def shipment(client):
    shipment = Shipment(client)

    # Now set the values
    # The values are based on Standard Shipment example in docs 3.5.6
    shipment.software.name = 'Python'
    shipment.software.version = '2.7'

    shipment.consignee.country = 'DE'
    shipment.consignee.zip = '99334'
    shipment.parcel_number = '463500000007'
    shipment.parcel_weight = Decimal('31.5')
    shipment.shipping_date = date.today()

    shipment.consignor.customer_number = 12
    shipment.consignor.name = 'GLS IT Services GmbH'
    shipment.consignor.name2 = 'Project Management'
    shipment.consignor.street = 'GLS-Germany-Str, 1-7'
    shipment.consignor.country = 'DE'
    shipment.consignor.zip = '36286'
    shipment.consignor.place = 'Neuenstein'
    shipment.consignor.label = 'Empfanger'

    shipment.consignee.customer_number_label = 'Kd-Nr'
    shipment.consignee.customer_number = 10166
    shipment.consignee.id_type = 'ID-Nr'
    shipment.consignee.id_value = 800018406

    shipment.consignee.salutation = 'Firma'
    shipment.consignee.name = 'GLS Germany'
    shipment.consignee.name2 = 'GmbH & Co. KG'
    shipment.consignee.street = 'Am Sulzenbruckener Weg'
    shipment.consignee.place = 'Ichtershausen'

    shipment.parcel = 1
    shipment.quantity = 1

    return shipment


class TestShipment:

    def test_shipment(self, shipment):
        # TODO: Based on the response parse and use it
        shipment.create_label()


class TestResponse:

    def test_parsing(self):
        response = Response.parse(
            read('example_response.txt')
        )
        assert response.consignee.name == u'GLS Germany'
        assert response.shipping_date == date(2009, 1, 26)
