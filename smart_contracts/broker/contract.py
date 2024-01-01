import beaker
from pyteal import Approve, Subroutine, abi, Concat, Bytes, Expr


app = beaker.Application("broker")


@app.update
def update() -> Expr:
    return Approve()


@app.delete
def delete() -> Expr:
    return Approve()


@app.external
def hello(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))


@app.external
def trade(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))
