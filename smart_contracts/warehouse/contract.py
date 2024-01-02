from typing import Final, Literal
from beaker import Application, GlobalStateValue, LocalStateValue
from pyteal import (
    Approve,
    Int,
    Itob,
    ScratchVar,
    abi,
    Expr,
    Concat,
    Bytes,
    Seq,
    TealType,
)


class WarehouseState:
    trade_constracts: Final[GlobalStateValue] = GlobalStateValue(
        stack_type=TealType.bytes, descr="Trade Contracts App Ids"
    )
    shared_stock: Final[GlobalStateValue] = GlobalStateValue(
        stack_type=TealType.uint64, descr="Galaxy Id"
    )
    local_stock: Final[LocalStateValue] = LocalStateValue(
        stack_type=TealType.uint64, descr="Mineral Amount"
    )


app = Application("warehouse", state=WarehouseState())


@app.create
def create() -> Expr:
    return Seq(app.state.shared_stock.set(Int(10)), Approve())


@app.opt_in
def opt_in() -> Expr:
    return Seq(app.state.local_stock.set(Int(1000)), Approve())


@app.external
def hello(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))


@app.external
def transfer(value: abi.Uint64, *, output: abi.String) -> Expr:
    return Seq(
        app.state.shared_stock.set(value.get()),
        output.set(Bytes("Done")),
    )


@app.external
def deposit(value: abi.Uint64, *, output: abi.String) -> Expr:
    return Seq(
        app.state.local_stock.set(app.state.local_stock.get() - value.get()),
        app.state.shared_stock.set(value.get()),
        output.set(Bytes("Done")),
    )


@app.external
def test(*, output: abi.Uint64) -> Expr:
    stats2 = abi.DynamicArray(abi.DynamicArrayTypeSpec(abi.Uint64TypeSpec()))
    stats_length = abi.Uint64()

    return Seq(
        (a := abi.Uint64()).set(Int(10)),
        stats2.set([a]),
        stats2[0].store_into(stats_length),
        output.set(stats2.length()),
    )
