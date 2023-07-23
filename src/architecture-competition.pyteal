from pyteal import *

def architectural_competition(app_id: int):

    on_initialization = Seq([
        App.localPut(Int(0), Bytes("hasVoted"), Int(0)),
        App.localPut(Int(0), Bytes("voteCount"), Int(0)),
        Return(Int(1))
    ])

    on_update_call = Return(Int(1))

    on_vote = Seq([
        Assert(App.localGet(Int(0), Bytes("hasVoted")) == Int(0)),
        App.localPut(Int(0), Bytes("hasVoted"), Int(1)),
        App.localPut(Int(0), Bytes("voteCount"), Add(App.localGet(Int(0), Bytes("voteCount")), Int(1))),
        Return(Int(1))
    ])

    on_query_vote_count = Return(App.localGet(Int(0), Bytes("voteCount")))

    program = Cond(
        [Txn.application_id() == Int(0), on_initialization],
        [Txn.application_id() == Int(app_id), Cond(
            [Txn.application_call().Enum() == Int(0), on_update_call],
            [Txn.application_call().Enum() == Int(1), on_vote],
            [Txn.application_call().Enum() == Int(2), on_query_vote_count],
        )],
    )

    return compileTeal(program, mode=Mode.Application, version=4)

if __name__ == "__main__":
    print(compileTeal(architectural_competition(1234), mode=Mode.Application))
