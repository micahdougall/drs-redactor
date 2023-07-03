
# Deploy function

Deploy function with new code:

```bash
# Add --gen2 flag for 2nd gen CFs
# From root folder:
gcloud functions deploy dlp-handler \
--runtime=python310 \
--region=europe-west2 \
--source=src/ \
--entry-point=app \
--trigger-http \
--allow-unauthenticated
```

Request to deployed version
```bash
# Update credentials in config before deployment
gcloud auth print-access-token
curl https://europe-west2-silken-apex-372315.cloudfunctions.net/python-http-function
```

Deploy function locally

```bash
# Update credentials in config before deployment
gcloud auth print-identity-token

gcloud auth application-default login

source dev/bin/activate
pip install -r requirements.txt

functions-framework-python --target app --debug --port=8081
curl http://localhost:8081
```




Upload new files
```
FILE = payload1.json
$ gsutil copy $FILE gs://sandbox-cms-payloads
```

## Requirements for working version deployed:
- google-cloud-storage
- attrs==22.2.0
- dataclass_wizard==0.22.2
- functions_framework==3.3.0
- jproperties==2.1.1
- protobuf==4.22.1
- requests==2.28.2


## Troubleshooting

- May be unable to deploy gen2 if not activated Cloud Run in GCP
- DLP may refuse request to to lack of OAuth


## Deployment notes
 The following packages are installed automatically in GCP:
- click==8.0.3
- cloudevents==1.2.0
- deprecation==2.1.0
- Flask==2.0.2
- functions-framework==3.0.0
- gunicorn==20.1.0
- itsdangerous==2.0.1
- Jinja2==3.0.3
- MarkupSafe==2.0.1
- packaging==21.3
- pathtools==0.1.2
- pyparsing==3.0.6
- setuptools==60.3.1
- watchdog==1.0.2
- Werkzeug==2.0.2
