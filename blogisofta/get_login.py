""" Get login data for PostgreSQL from Google Secret Manager """

# Secret Manager client library
from google.cloud import secretmanager

def login_data():
    """
    Version id voi olla joko versionumero merkkijonomuodossa
    tai sit alias "latest", jos haluaa viimeisimmän.
    """

    # Luo yhteys
    client = secretmanager.SecretManagerServiceClient()

    # Määrittele salaisuuden polku
    usernm = "projects/fall-week7-3/secrets/postgres-un/versions/latest"
    passwd = "projects/fall-week7-3/secrets/postgres-pw/versions/latest"

    # Avaa access salaisuuteen
    response_un = client.access_secret_version(request={"name": usernm})
    response_pw = client.access_secret_version(request={"name": passwd})

    # Tulosta salaisuuden sisältö
    payload_un = response_un.payload.data.decode("UTF-8")
    payload_pw = response_pw.payload.data.decode("UTF-8")
    
    return payload_un, payload_pw