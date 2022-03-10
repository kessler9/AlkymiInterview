import requests
import json
import csv
from os import remove
from celery import shared_task
from TemporalProcessor.models import File, Row, Temporal


@shared_task
def resolve_temporals(file_uid):
    bearer_token = requests.post(
        'https://alkymi-staging.auth0.com/oauth/token',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'grant_type': 'client_credentials',
            'client_id': 'VZouYIRkBdYcho9uHjCqBdwpZAuodJSG',
            'client_secret': 'WbB1N1VMN8f0_c6QKaWpWCfZCMpWuUP8Xgir-y9aZt551cMUoc5vb_0TV6XDC0AS',
            'audience': 'stanford-public.alkymi.cloud'
        }
    ).json()['access_token']
    file = File.objects.get(uid=file_uid)
    filename = f'{file_uid}.csv'
    with open(filename, 'r') as fh:
        reader = csv.reader(fh, quotechar='"')
        for i, _row in enumerate(reader):
            row = Row(file=file, raw_row=json.dumps(_row))
            row.save()
            for j, col in enumerate(_row):
                resolve_temporal_thread(col, row, i, j, file, bearer_token)
    remove(filename)


def resolve_temporal_thread(to_search, row, row_id, col_id, file, bearer_token):
    resp = requests.get(
        f'https://stanford-public.alkymi.cloud/getTemporals',
        params={'text': to_search},
        headers={'Authorization': f'Bearer {bearer_token}'}
    )
    for result in resp.json():
        temporal = Temporal(
            file=file,
            row=row,
            row_index=row_id,
            column=col_id,
            **result
        )
        temporal.save()
        print(temporal.__dict__)



# resolve_temporal_thread('2020-01-01', Row.objects.get(id=1), 0, 1, File.objects.get(id=1))