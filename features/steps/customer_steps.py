######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Customers Steps

Steps file for usage with customers.feature using Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import os
import requests
from behave import given, when, then
from compare import expect


@given('the following customers')
def step_impl(context):
    """ Delete all Customer and load new ones """
    # List all of the customers and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/api/customers"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for promotion in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{promotion['id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new customers
    for row in context.table:
        payload = {
            "id" : row['ID'],
            "firstname" : row['Firstname'],
            "lastname" : row['Lastname'],
            "email" : row['Email'],
            "phone" : row['Phone'],
            "street_line1" : row['Street_Line1'],
            "street_line2" : row['Street_Line2'],
            "city" : row['City'],
            "state" : row['State'],
            "country" : row['Country'],
            "zipcode" : row['Zipcode']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)
