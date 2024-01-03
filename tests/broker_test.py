import algokit_utils
import algosdk
import pytest
from algokit_utils import (
    TransactionParameters,
    TransferParameters,
    get_account,
    get_localnet_default_account,
    transfer,
)
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from artifacts.warehouse.client import WarehouseClient

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

    client.create_create()

    transfer(
        algod_client,
        parameters=TransferParameters(
            from_account=get_localnet_default_account(algod_client),
            to_address=client.app_client.app_address,
            micro_algos=1000000,
        ),
    )

    client.opt_in_opt_in()

    return client


@pytest.fixture(scope="session")
def country_party_client(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    broker_client: BrokerClient,
) -> BrokerClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )
    counter_party_account = get_account(algod_client, "Yutani", fund_with_algos=10000)
    client = BrokerClient(
        algod_client,
        creator=counter_party_account,
        indexer_client=indexer_client,
        app_id=broker_client.app_id,
    )

    client.create_create()
    client.opt_in_opt_in()
    return client


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

    transfer(
        algod_client,
        parameters=TransferParameters(
            from_account=get_localnet_default_account(algod_client),
            to_address=client.app_client.app_address,
            micro_algos=1000000,
        ),
    )

    client.create_create()

    transfer(
        algod_client,
        parameters=TransferParameters(
            from_account=get_localnet_default_account(algod_client),
            to_address=client.app_client.app_address,
            micro_algos=1000000,
        ),
    )

    client.opt_in_opt_in()
    return client


def test_transfer_complete(
    broker_client: BrokerClient,
    country_party_client: BrokerClient,
    warehouse_client: WarehouseClient,
) -> None:
    result = broker_client.start_trade(
        warehouse_id=warehouse_client.app_id,
        amount=200,
        transaction_parameters=TransactionParameters(
            foreign_apps=[warehouse_client.app_id]
        ),
    )
    global_state_result = warehouse_client.get_global_state()

    assert global_state_result.shared_stock == 300
