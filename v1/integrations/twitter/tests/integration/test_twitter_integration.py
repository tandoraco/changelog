import json

import pytest
from background_task.models import Task

from v1.core.serializers import ChangelogSerializer
from v1.core.tests.fixtures import create_changelog


@pytest.mark.django_db
def test_integration_background_job_created_for_changelog_create_and_edit(company, changelog1_data):
    assert Task.objects.count() == 0

    changelog = create_changelog(changelog1_data)

    assert Task.objects.count() == 1
    task = Task.objects.get()
    assert 'trigger_integration_background_tasks' in task.task_name
    assert task.task_params == json.dumps([[changelog.company.id, changelog.id], {'created': True}])

    changelog.title = 'Update changelog'
    changelog.save()
    # always use a ChangelogSerializer to save.. only then task entry will be created
    # here we used model.save(), so no background task will be created
    assert Task.objects.count() == 1

    serializer = ChangelogSerializer(instance=changelog, data={'title': 'Update 1'})
    if serializer.is_valid():
        changelog = serializer.save()
        assert Task.objects.count() == 2
        task = Task.objects.last()
        assert task.task_params == json.dumps([[changelog.company.id, changelog.id], {'created': False}])
