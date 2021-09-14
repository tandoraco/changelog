import logging
from logging import Logger

from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET
from slack_sdk import WebClient
from slack_sdk.oauth import AuthorizeUrlGenerator
from slack_sdk.oauth.state_store import OAuthStateStore

from frontend.custom.decorators import is_authenticated
from v1.integrations.slack.models import SlackState, Slack


class ModelStateStore(OAuthStateStore):

    @transaction.atomic
    def issue(self, *args, **kwargs) -> str:
        request = kwargs['request']
        slack_state = SlackState.objects.create(company=request.user.company)
        return str(slack_state)

    def consume(self, state: str) -> bool:
        try:
            state = SlackState.objects.get(uuid=state)
            return state.is_valid()
        except SlackState.DoesNotExist:
            return False

    @property
    def logger(self) -> Logger:
        return logging.getLogger('integrations')


@require_GET
@is_authenticated
def slack_oauth_start(request):
    state_store = ModelStateStore()
    state = state_store.issue(request=request)
    authorized_url_generator = AuthorizeUrlGenerator(
        client_id=settings.SLACK_CLIENT_ID,
        scopes=['channels:read', 'chat:write'],
        user_scopes=[],
    )
    url = authorized_url_generator.generate(state)
    return HttpResponse(
        f'<a href="{url}">'
        f'<img alt=""Add to Slack"" height="40" width="139"'
        f'src="https://platform.slack-edge.com/img/add_to_slack.png" '
        f'srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, '
        f'https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>'
    )


def slack_oauth_callback(request):
    state_store = ModelStateStore()
    code = request.GET['code']
    if state_store.consume(request.GET['state']):
        client = WebClient()
        oauth_response = client.oauth_v2_access(
            client_id=settings.SLACK_CLIENT_ID,
            client_secret=settings.SLACK_CLIENT_SECRET,
            code=code
        )
        slack_state = SlackState.objects.get(uuid=request.GET['state'])
        slack, _ = Slack.objects.get_or_create(company=slack_state.company)
        slack.oauth_response = oauth_response.data
        slack.save()
        return HttpResponseRedirect('/')
    else:
        print('invalid')
        return HttpResponseRedirect('/')
