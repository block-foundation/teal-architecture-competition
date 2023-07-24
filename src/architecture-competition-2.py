from pyteal import *

def architectural_competition(app_id: int):

    def check_if_voting_open():
        return Global.latest_timestamp() < App.globalGet(Bytes("votingDeadline"))

    on_initialization = Seq([
        App.globalPut(Bytes("votingDeadline"), Add(Global.latest_timestamp(), Mul(Int(60 * 60 * 24 * 7), Int(1000)))),
        Return(Int(1))
    ])

    on_update_call = Return(Int(1))

    on_submit_entry = Seq([
        Assert(check_if_voting_open()),
        App.globalPut(Txn.application_args[0], Int(0)),
        Return(Int(1))
    ])

    on_vote = Seq([
        Assert(And(
            check_if_voting_open(),
            App.localGet(Int(0), Bytes("hasVoted")) == Int(0)
        )),
        App.localPut(Int(0), Bytes("hasVoted"), Int(1)),
        App.globalPut(Txn.application_args[0], Add(App.globalGet(Txn.application_args[0]), Int(1))),
        Return(Int(1))
    ])

    on_query_vote_count = Return(App.globalGet(Txn.application_args[0]))

    program = Cond(
        [Txn.application_id() == Int(0), on_initialization],
        [Txn.application_id() == Int(app_id), Cond(
            [Txn.application_call().Enum() == Int(0), on_update_call],
            [Txn.application_call().Enum() == Int(1), on_submit_entry],
            [Txn.application_call().Enum() == Int(2), on_vote],
            [Txn.application_call().Enum() == Int(3), on_query_vote_count],
        )],
    )

    return compileTeal(program, mode=Mode.Application, version=4)

if __name__ == "__main__":
    print(compileTeal(architectural_competition(1234), mode=Mode.Application))
