# Blockchains
This is the implementation of some core concepts of blockchain and cryptocurrency. From creating the Genesis block to a chain of blocks , Adding new Nodes into the network , Using the SHA256 hashing algorithm to get the nonce based on current target , implementing the consensus algorithm to find the longest Chain among the nodes , adding transactions into the mempool and mining block based on the proof of work mechanism and adding the block into the blockchain.

Flask is used to deploy the Nodes

# Dependencies
- ```pip install flask```
- ```pip install requests```
- Postman app
# Local testing
In order to run a node, simply run
```Node_8001.py```
You can start other nodes at desired port by editing the port number in the last line.

To interact with the node, we need postman app. After downloading postman you can do following:
- Add nodes by making a post request of json file in the format of nodes.json. If you are running at port 8001 then make the post request at
```http://192.168.1.33:8001/add_Node```
- Add a transaction by making a post request in json format as via postman. If you are running at port 8001 then make the post request at
```http://192.168.1.33:8001/add_transaction```
- Mine a block. This will place all the unconfirmed transaction in mempool into the upcomming block. If you are running at port 8001 then make the get request at
```http://192.168.1.33:8001/mine_block```
- Follow a concensus by getting the longest valid chain in the whole network. If you are running at port 8001 then make the get request at
```http://192.168.1.33:8001/replace_chain```
- View the current full chain. If you are running at port 8001 then make the get request at
```http://192.168.1.33:8001/get_chain```
# Sample Output

## Genesis Block
![alt text](https://github.com/yashgoel72/Blockchains/blob/main/sampleOutput/Screenshot%201943-10-28%20at%2010.25.41%20AM.png)

## Adding Node Port = 8001
![alt text](https://github.com/yashgoel72/Blockchains/blob/main/sampleOutput/Screenshot%201943-10-28%20at%2010.26.46%20AM.png)

## Adding Node Port = 8002
![alt text](https://github.com/yashgoel72/Blockchains/blob/main/sampleOutput/Screenshot%201943-10-28%20at%2010.27.05%20AM.png)

## Adding transaction
![alt text](https://github.com/yashgoel72/Blockchains/blob/main/sampleOutput/Screenshot%201943-10-28%20at%2010.27.40%20AM.png)

## Mining block from PORT = 8001
![alt text](https://github.com/yashgoel72/Blockchains/blob/main/sampleOutput/Screenshot%201943-10-28%20at%2012.44.19%20PM.png)

## Current Chain on Port = 8001
![alt text](https://github.com/yashgoel72/Blockchains/blob/main/sampleOutput/Screenshot%201943-10-28%20at%2010.29.31%20AM.png)

## Before Consensus on Port = 8002
![alt text](https://github.com/yashgoel72/Blockchains/blob/main/sampleOutput/Screenshot%201943-10-28%20at%2010.29.45%20AM.png)

## Consensus using /replace_chain on Port = 8002
![alt text](https://github.com/yashgoel72/Blockchains/blob/main/sampleOutput/Screenshot%201943-10-28%20at%2010.30.05%20AM.png)
