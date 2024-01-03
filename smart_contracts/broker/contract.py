from typing import Final
import beaker
from beaker import Application, GlobalStateValue, LocalStateValue
from pyteal import (
    Approve,
    InnerTxnBuilder,
    Int,
    Seq,
    Subroutine,
    TealType,
    abi,
    Concat,
    Bytes,
    Expr,
)


class BrokerState:
    warehouse_id: Final[GlobalStateValue] = GlobalStateValue(
        stack_type=TealType.uint64, descr="Warehouse Id"
    )
    amount: Final[LocalStateValue] = LocalStateValue(
        stack_type=TealType.uint64, descr="Trade Amount"
    )


app = Application("broker", state=BrokerState())


@app.update
def update() -> Expr:
    return Approve()


@app.delete
def delete() -> Expr:
    return Approve()


@app.external
def start_trade(
    warehouse_id: abi.Uint64, amount: abi.Uint64, *, output: abi.String
) -> Expr:
    return Seq(
        app.state.warehouse_id.set(warehouse_id.get()),
        app.state.amount.set(amount.get()),
        (inner_txn := InnerTxnBuilder()).ExecuteMethodCall(
            app_id=warehouse_id.get(),
            method_signature="hold(uint64)string",
            args=[amount],
        ),
    )


@app.external
def complete_trade(
    warehouse_id: abi.Uint64, amount: abi.Uint64, *, output: abi.String
) -> Expr:
    return Seq(
        app.state.warehouse_id.set(warehouse_id.get()),
        app.state.amount.set(amount.get()),
        (inner_txn := InnerTxnBuilder()).ExecuteMethodCall(
            app_id=warehouse_id.get(),
            method_signature="transfer(uint64)string",
            args=[amount],
        ),
    )


@app.create
def create() -> Expr:
    return Seq(Approve())


@app.opt_in
def opt_in() -> Expr:
    return Seq(Approve())
