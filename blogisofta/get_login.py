""" Get login data for PostgreSQL from Google Secret Manager """

# Secret Manager client library
from google.cloud import secretmanager
import os

def login_data():
    """
    Version id voi olla joko versionumero merkkijonomuodossa
    tai sit alias "latest", jos haluaa viimeisimmän.
    """
    project_id = os.environ['PROJECT_ID']

    # Luo yhteys
    client = secretmanager.SecretManagerServiceClient()

    # Määrittele salaisuuden polku:
    # projects/<PROJEKTI>/secrets/<SALAISUUS>/versions/latest
    sql_ip = f"projects/{project_id}/secrets/postgres-ip/versions/latest"
    database = f"projects/{project_id}/secrets/postgres-database/versions/latest"
    port = f"projects/{project_id}/secrets/postgres-port/versions/latest"
    username = f"projects/{project_id}/secrets/postgres-un/versions/latest"
    password = f"projects/{project_id}/secrets/postgres-pw/versions/latest"

    # Avaa access salaisuuteen
    response_ip = client.access_secret_version(request={"name": sql_ip})
    response_database = client.access_secret_version(request={"name": database})
    response_port = client.access_secret_version(request={"name": port})
    response_un = client.access_secret_version(request={"name": username})
    response_pw = client.access_secret_version(request={"name": password})

    # talleta salaisuus muuttujaan
    payload_ip = response_ip.payload.data.decode("UTF-8")
    payload_database = response_database.payload.data.decode("UTF-8")
    payload_port = response_port.payload.data.decode("UTF-8")
    payload_un = response_un.payload.data.decode("UTF-8")
    payload_pw = response_pw.payload.data.decode("UTF-8")
    
    return payload_ip, payload_database, payload_port, payload_un, payload_pw