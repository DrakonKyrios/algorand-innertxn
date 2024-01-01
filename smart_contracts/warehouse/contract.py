from typing import Final
from beaker import Application, GlobalStateValue, LocalStateValue
from pyteal import abi, Expr, Concat, Bytes, Seq, TealType


class WarehouseState:
    shared_stock: Final[GlobalStateValue] = GlobalStateValue(
        stack_type=TealType.uint64, descr="Galaxy Id"
    )
    local_stock: Final[LocalStateValue] = LocalStateValue(
        stack_type=TealType.uint64, descr="Mineral Amount"
    )


app = Application("warehouse", state=WarehouseState())


@app.external
def hello(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))


@app.external
def transfer(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))


@app.external
def sell(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))
