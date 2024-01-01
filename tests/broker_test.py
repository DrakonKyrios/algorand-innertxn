import algokit_utils
import algosdk
import pytest
from algokit_utils import get_localnet_default_account
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.broker.client import BrokerClient


@pytest.fixture(scope="session")
def broker_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> BrokerClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = BrokerClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
        delete_args=algokit_utils.DeployCallArgs(),
    )
    return client


def test_says_hello(broker_client: BrokerClient) -> None:
    result = broker_client.hello(name="World")

    assert result.return_value == "Hello, World"
