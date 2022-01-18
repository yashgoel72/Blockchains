# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask , jsonify , request
import requests
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
        self.chain=[]                                         # stores the current chain of blocks
        self.transactions = []                                # stores all the unconfirmed transactions , basically act as a mempool
        self.nodes = set()                                    # stores the address of all the nodes in the network
        self.create_block(proof = 1 , previous_hash = '0')    # Creating the genesis block

    def create_block(self , proof , previous_hash):           # Function to create the block
        block = {"index" : len(self.chain) + 1,
                "proof" : proof,
                "previous_hash" : previous_hash,
                "time_stamp" : str(datetime.datetime.now()),
                "transactions" : self.transactions }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self , previous_proof):                 # Returns the proof(nonce value) based on the current target by implementing SHA256 hashing algorithm
        proof = 1
        got_proof= False
        while got_proof is False:
            hash = hashlib.sha256(str(proof**2 - previous_proof **2).encode()).hexdigest()
            if(hash[:4] == "0000"):                           # Here current target is "0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
                got_proof = True
            else:
                proof += 1
        return proof

    def hash( self , block):                                  # Returns the sha256 hash of the block
        hash_operation = hashlib.sha256 ( json.dumps(block , sort_keys= True).encode()).hexdigest()
        return hash_operation

    def is_chain_valid(self , chain):                         # checks whether the chain is valid or not
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if( block['previous_hash'] != self.hash(previous_block)):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if( hash[ : 4] != '0000'):
                return False
            previous_block = block
            block_index +=1

        return True
    
    def add_transactions(self , sender , receiver , amount):      # Adds new transaction into the mempool
        self.transactions.append({"sender" : sender,
                                  "receiver" : receiver,
                                  "amount" : amount})
        previous_block = self.get_previous_block()
        return previous_block["index"] + 1            # returns the index of block which will contain this transactions
    
    def add_node(self , address):                     # adds new node into the network
        parsed_url = urlparse(address)
        self.nodes.add( parsed_url.netloc)
        
    def replace_chain(self):                          # Replaces the current chain with the lonhest Chain in the network
        network = self.nodes
        longestChain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if( response.status_code == 200):
                length = response.json()["length"]
                chain = response.json()["chain"]
                if length > max_length and self.is_chain_valid(chain) :
                    max_length = length
                    longestChain = chain
            
        if longestChain:
            self.chain = longestChain
            return True
        return False
                    
                
# FLASK IS USED TO DEPLOY THE NODES

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

node_address = str(uuid4()).replace('-' , '')
blockchain = Blockchain()                                             # Creating an object of Blockchain class

@app.route( '/mine_block' , methods =['GET'])                         # GET method to mine a new block and 
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(previous_block['proof'])
    blockchain.add_transactions(sender = node_address, receiver = 'Rohit', amount = 1)     # Transaction as a reward to the miner, here 'Rohit'.
    block = blockchain.create_block(proof , previous_hash)
    response = {'messgae' : "Congrats you have mined a block",
                    'block_index': block['index'],
                    'timestamp' : block['time_stamp'],
                    'proof' : block['proof'],
                    'previous_hash' : block['previous_hash'],
                    'transactions' : block['transactions']}

    return jsonify(response), 200

@app.route( '/get_chain' , methods =['GET'])                          # Returns the current chain in the node in the json format
def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(response) , 200 

@app.route( '/is_valid' , methods =['GET'])                           # Checks the validity of the current chain 
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    
    if is_valid:
        response = {"messgae" : "Blockchain is valid"}   
    else:
        response = {"messgae" : "Blockchain is Invalid"}
    return jsonify(response) , 200

@app.route('/add_transaction' , methods = ['POST'])                   # POST Request to post the transaction into the mempool , input must be int the form of "transaction.json"
def add_transaction():    
    json = request.get_json()
    transaction_keys = ['sender' , 'receiver' , 'amount']
    
    if not all ( key in json for key in transaction_keys):
        return 'Some elements are missing in the transaction' , 400
    index = blockchain.add_transactions(json['sender'] , json['receiver'] , json['amount'])
    response = {'message' : f'This Transaction will be added to Block {index} ' }
    return jsonify(response) , 201

@app.route('/add_Node' , methods = ['POST'])                          # POST Request to add node into the network , input must be int the form of "nodes.json"
def add_Node():
    json = request.get_json()                                         # here we input the address of all the other nodes in the network to connect to new Node
    nodes = json['nodes']
    
    if nodes is None:
        return 'No Nodes present ' , 400
    for node in nodes :
        blockchain.add_node(node)
    
    response = { " messgae" :"The Nodes now present in the network are following :",
                " Nodes " : list(blockchain.nodes)}
    return jsonify(response) , 201

@app.route('/replace_chain' , methods = ['GET'])                      # Checks whether the current chain is the longest or not , if not then replaces with the longest chain of the network
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced :
        response = {'message' : "The chain is replaced by the longest chain",
                    'New_chain' : blockchain.chain}
    else:
        response = {'message' : "The chain is already  the longest chain",
                    'Chain' : blockchain.chain}
    return jsonify(response) , 200
        
        

    
app.run(host = '0.0.0.0' , port = 8002)                # PORT 8001
