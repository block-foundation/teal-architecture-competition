from pyteal import *

def architectural_design_contest():

    on_initialization = Seq([
        App.localPut(Int(0), Bytes("prize"), Txn.application_args[0]),
        App.localPut(Int(0), Bytes("deadline"), Txn.application_args[1]),
        Return(Int(1))
    ])

    on_submit_design = Seq([
        Assert(Txn.application_id() != Int(0)),  # Ensure this is not the initialization call
        Assert(Global.latest_timestamp() < App.localGet(Int(0), Bytes("deadline"))),
        App.localPut(Txn.sender(), Bytes("design"), Txn.application_args[0]),
        Return(Int(1))
    ])

    on_select_winner = Seq([
        Assert(Txn.application_id() != Int(0)),  # Ensure this is not the initialization call
        Assert(Global.latest_timestamp() > App.localGet(Int(0), Bytes("deadline"))),
        Assert(Txn.close_remain_to() == App.localGet(Int(0), Bytes("winner_address"))),
        Assert(Txn.amount() == App.localGet(Int(0), Bytes("prize"))),
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_initialization],
        [Txn.application_id() != Int(0), on_submit_design],
        [Txn.application_id() != Int(0), on_select_winner]
    )

    return compileTeal(program, mode=Mode.Application)

if __name__ == "__main__":
    print(compileTeal(architectural_design_contest(), mode=Mode.Application))
