Creating an Algorand smart contract (ASC1) to manage architectural design requires clarity about the specific functionalities and workflows desired. Algorand's smart contracts are written in a language called Transaction Execution Approval Language (TEAL). For the sake of illustration, I'll present a simplified use case:

**Use Case**: An architectural design contest where participants submit their designs. An owner will select a winner, and then a prize (in Algos) will be sent to the winner.

1. Initialization: The contract is initialized with the total prize amount and a deadline for design submission.

2. Design Submission: Before the deadline, participants can submit their design by sending a small transaction with a note field detailing their design ID (or a link to the design).

3. Winner Selection: After the deadline, the owner selects a winner by sending a transaction with the winner's address.

4. Prize Distribution: The prize is sent to the winner.

Here is a very basic and abstracted TEAL code for this use case:


``` teal
#pragma version 3

// Check if the transaction is the first one (initialization)
txn GroupIndex
int 0
==
bnz initialization

// Check for design submission
global LatestTimestamp
byte "deadline"
app_global_get
<
bnz submit_design

// Check for winner selection and prize distribution
txn GroupIndex
int 1
==
bnz select_winner

// Initialization
initialization:
    // Check that the application is being created
    txn TypeEnum
    int appl
    ==
    txn OnCompletion
    int NoOp
    ==
    &&
    // Set the prize and deadline from the transaction's arguments
    byte "prize"
    txn ApplicationArgs 0
    app_global_put

    byte "deadline"
    txn ApplicationArgs 1
    app_global_put
    return

submit_design:
    // Store the design ID (or link) from the note field to the designer's address
    txn Sender
    txn Note
    app_local_put
    return

select_winner:
    // The owner selects a winner
    txn TypeEnum
    int pay
    ==
    txn CloseRemainderTo
    byte "winner_address"
    app_global_get
    ==
    &&
    txn Amount
    byte "prize"
    app_global_get
    ==
    &&
    return


```

## Note:

- This code is a high-level illustration and doesn't cover error handling, access control, and other important details.
- Actual implementations would require more sophistication and a proper understanding of the TEAL language.
- Storing designs on-chain may not be feasible due to size constraints. Instead, storing a hash or a link to the design would be more practical.

You may also want to use PyTEAL or Reach, which are high-level languages that compile down to TEAL, for a more user-friendly experience. Before deploying any smart contract, it's crucial to have it audited for security reasons.