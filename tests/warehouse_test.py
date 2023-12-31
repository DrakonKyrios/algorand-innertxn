import algokit_utils
import algosdk
import pytest
from algokit_utils import get_localnet_default_account
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.warehouse.client import WarehouseClient


@pytest.fixture(scope="session")
def warehouse_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> WarehouseClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = WarehouseClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )
    client.create_create()
    # client.deploy(
    #     on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    #     on_update=algokit_utils.OnUpdate.AppendApp,
    #     delete_args=algokit_utils.DeployCallArgs(),
    # )
    client.opt_in_opt_in()
    return client


def test_initial(warehouse_client: WarehouseClient) -> None:
    result = warehouse_client.get_global_state()

    assert result.shared_stock == 100


def test_hold(warehouse_client: WarehouseClient) -> None:
    warehouse_client.hold(value=200)

    global_result = warehouse_client.get_global_state()
    local_result = warehouse_client.get_local_state()

    assert global_result.shared_stock == 300
    # assert local_result.local_stock == 800


def test_transfer(warehouse_client: WarehouseClient) -> None:
    warehouse_client.hold(value=200)
    warehouse_client.transfer(value=200)

    global_result = warehouse_client.get_global_state()
    local_result = warehouse_client.get_local_state()

    assert global_result.shared_stock == 300
    # assert local_result.local_stock == 1000
