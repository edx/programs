"""
Tests for Programs API views (v1).
"""
import json

import ddt
from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import ANY

from programs.apps.programs.constants import CertificateType, ProgramCategory, ProgramStatus
from programs.apps.programs.tests.factories import ProgramFactory


POST_FIELDS = ("name", "description", "category", "certificate_type", "status")
CATEGORIES = (ProgramCategory.XSERIES, )
CERT_TYPES = (CertificateType.VERIFIED, )
STATUSES = (ProgramStatus.UNPUBLISHED, ProgramStatus.ACTIVE, ProgramStatus.RETIRED, ProgramStatus.DELETED)


@ddt.ddt
class ProgramsViewTests(TestCase):
    """
    Tests for listing / creating Programs.
    """
    @staticmethod
    def _build_post_data(**kwargs):
        """
        Build and return a dict representation to use for POST / create.
        """
        instance = ProgramFactory.build(**kwargs)
        return {k: getattr(instance, k) for k in POST_FIELDS}

    def test_list(self):
        """
        Verify the list includes all Programs, except those with DELETED status
        """
        # create one Program of each status
        for status in STATUSES:
            ProgramFactory(name="{} program".format(status), status=status)

        response = self.client.get(reverse("api:v1:programs-list"))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(len(content), 3)
        self.assertNotIn(ProgramStatus.DELETED, set(obj["status"] for obj in content))

    def test_create(self):
        """
        Ensure the API supports creation of Programs.
        """
        data = self._build_post_data()
        response = self.client.post(reverse("api:v1:programs-list"), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.content),
            {
                "name": data["name"],
                "description": data["description"],
                "category": data["category"],
                "certificate_type": data["certificate_type"],
                "status": data["status"],
                "id": ANY,
                "created": ANY,
                "modified": ANY,
            }
        )

    @ddt.data(*POST_FIELDS)
    def test_missing_fields(self, field):
        """
        Ensure that missing fields cause validation errors if required, and create with correct defaults otherwise.
        """
        defaults = {
            "description": None,
            "certificate_type": None,
            "status": ProgramStatus.UNPUBLISHED,
        }

        data = self._build_post_data()
        del data[field]
        if field in defaults:
            expected_status = 201
        else:
            expected_status = 400

        response = self.client.post(reverse("api:v1:programs-list"), data=data)
        self.assertEqual(response.status_code, expected_status)
        content = json.loads(response.content)
        if expected_status == 201:
            self.assertEqual(content[field], defaults[field])
        else:
            self.assertIn("field is required", content[field][0])

    @ddt.data(ProgramStatus.ACTIVE, ProgramStatus.RETIRED, ProgramStatus.DELETED, None, "", "unrecognized")
    def test_create_with_invalid_status(self, status):
        """
        Ensure that it is not allowed to create a Program with a status other than "unpublished"
        """
        data = self._build_post_data(status=status)
        response = self.client.post(reverse("api:v1:programs-list"), data=data)
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertIn("not a valid choice", content["status"][0])

    def test_create_with_invalid_certificate_type(self):
        """
        Ensure that it is not allowed to create a Program with an unrecognized certificate type
        """
        data = self._build_post_data(certificate_type="unrecognized-type")
        response = self.client.post(reverse("api:v1:programs-list"), data=data)
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertIn("not a valid choice", content["certificate_type"][0])

    @ddt.data(None, "", "unrecognized")
    def test_create_with_invalid_category(self, category):
        """
        Ensure that it is not allowed to create a Program with an empty or unrecognized category
        """
        data = self._build_post_data(category=category)
        response = self.client.post(reverse("api:v1:programs-list"), data=data)
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertIn("not a valid choice", content["category"][0])

    def test_create_duplicated_name(self):
        """
        Ensure that it is not allowed to create a Program with a duplicate name
        """
        ProgramFactory(name="duplicated name")  # saved directly to db
        data = self._build_post_data(name="duplicated name")
        response = self.client.post(reverse("api:v1:programs-list"), data=data)
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertIn("must be unique", content["name"][0])
