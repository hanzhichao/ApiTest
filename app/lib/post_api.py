import json
import requests
from .models import ProjectEnv


def post(env, api):
    project_env = get_object_or_404(ProjectEnv, env=env, project=api.project)
    base_url = project_env.base_url
    access_id = project_env.access_id
    access_key = project_env.access_key

    api.url = api.url if api.url.startswith("/") else "/" + api.url
    url = base_url + api.url
    data = json.loads(api.request_body)  # try ...
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf8"}
    if api.data_type = 1:  # json
        data = json.dumps()
        headers = {"Content-Type": "application/json; charset=utf8"}

    resp = requests.post(url=url, headers=headers, data=data)
    if api.data_type = 1:
        return resp.json()

    return resp.text

