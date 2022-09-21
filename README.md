# Polly Chain
Polly Chain is a simple blockchain operating fully on PoW Nakamoto-like consensus.

It's made purely out of curiosity, should be used only as an educational material e.t.c. Not exclusively safe, not too fast and still in development 🌳


## How to use?
The blockchain consists of 3 main modules, modules are not dependent on each other and can be easily run and used with a couple prerequisites taken into consideration:
- **Node** is an entry point in user interaction with the blockchain. It recieves blocks and transactions, validates them, constantly exchanges data with other known nodes and miners, as well as stores its own copy of the blockchain. 

  To host a node launch the _Node.py_ file. A socket will be instantly opened using your LAN IP address and binded on the port 8330.
  The program will ping all the known nodes( predefined in the _TRUSTED_IPS_ variable ) to fetch the current state of the blockchain. 
  If none of the pinged nodes have the actual copy of the blockchain( ***non - empty with at least one valid block*** ) - an empty blockchain will be created and the Node will start waiting for the miners to submit new blocks e.t.c.

  Node recieves transactions from the Wallet interface and stores them in the '_mempool_' - a list of all the transactions, which were not included into a block. These pending transactions are later fed to the miners🔨




 
