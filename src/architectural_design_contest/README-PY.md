Sure, I can help with that. PyTeal is a Python language binding for Algorand Smart Contracts that abstracts away many of the complexities and makes it more user-friendly. Here is the equivalent PyTeal code for the smart contract.


``` python

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

```



This PyTeal script works similarly to the previous TEAL script.

1. **Initialization**: The `on_initialization` branch sets up the `prize` and `deadline` from the transaction arguments.

2. **Design Submission**: The `on_submit_design` branch allows participants to submit their designs before the `deadline`, storing the design ID (or a link to the design) against the sender's address.

3. **Winner Selection**: The `on_select_winner` branch enables the owner to select a winner after the deadline, and the prize (in Algos) is sent to the winner.

This is a high-level concept and does not handle all cases or errors that may arise. You need to validate and test the smart contract thoroughly before using it in a production environment. This example assumes you are familiar with Algorand's Atomic Transactions and the usage of PyTeal. Please use this code as a starting point and modify it to suit your specific needs.

Also, note that as of my knowledge cutoff in September 2021, Algorand does not directly support storing large data on-chain. Therefore, the design is stored as a small string or ID. In practice, you would likely store the design off-chain (like on IPFS) and store the hash of the design on-chain for verification.
