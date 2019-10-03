import copy

import pytest
from faker import Faker

from v1.core.serializers import ChangelogSerializer

fake = Faker()


@pytest.fixture
def published_changelog_data(category, company):
    return {
        "company": company.id,
        "title": fake.name(),
        "content": fake.text(),
        "category": category.pk,
        "published": True
    }


@pytest.fixture
def unpublished_changelog_data(category, company):
    return {
        "company": company.id,
        "title": fake.name(),
        "content": fake.text(),
        "category": category.pk,
        "published": False
    }


@pytest.fixture
def changelog_data_without_company(published_changelog_data):
    data = published_changelog_data.copy()
    data.pop("company")
    return data


@pytest.fixture
def changelog1_data(published_changelog_data, user):
    return with_audit_entries(published_changelog_data, user)


@pytest.fixture
def changelog2_data(unpublished_changelog_data, user):
    return with_audit_entries(unpublished_changelog_data, user)


def create_changelog(data):
    serializer = ChangelogSerializer(data=data)
    if serializer.is_valid():
        return serializer.save()

    return None


def with_audit_entries(data, usr):
    data = copy.deepcopy(data)
    data.update({
        "created_by": usr.pk,
        "last_edited_by": usr.pk
    })
    return data


@pytest.fixture
def published_changelog(published_changelog_data, user):
    return create_changelog(with_audit_entries(published_changelog_data, user))


@pytest.fixture
def unpublished_changelog(unpublished_changelog_data, admin):
    return create_changelog(with_audit_entries(unpublished_changelog_data, admin))
