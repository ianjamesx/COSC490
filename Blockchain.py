from hashlib import sha256
import json
import time
from flask import Flask, request


class Block_info: # holds all the information for each block
    def __init__(self, index, status, timestamp, prev_hash):
        self.index = index  # index of block
        self. status = status  # status ex. pending or accepted
        self.timestamp = timestamp  # timestamp of when created
        self.prev_hash = prev_hash  # holds hash of previous block in chain

    def hash_func(self):  # hash function to sha 256
        return sha256(json.dumps(self.__dict__, sort_keys=True).encode()).hexdigest()

    '''
    Alternate way of doing hash function in sha 256
    
    def hash_func(self):
        sha = hashlib.sha256()
        sha.update(self.serialize(['hash']).encode('utf-8'))
        return sha.hexdigest()
    
    '''

class Blockchain:
    def __init__(self):
        self.pend_queue = []  # queue for blocks waiting to be accepted
        self.chain = []  # Array for blockchain
        self.first_block()  # Creates the initial block

    def first_block(self):
        initial_block = Block_info(0, [], time.time(), "0")  # data for first block

        initial_block.hash = initial_block.hash_func()  # hash first block
        self.chain.append(initial_block)  # appends to blockchain array

    @property
    def last_block(self):  # method to return previous block
        return self.chain[-1]

    difficulty = 2

    def testing(self, info):
        hash = Block_info.hash_func()
        while not hash.startswith('0' * Blockchain.difficulty):
            hash = Block_info.hash_func()
            return hash

    def add_block(self, block, proof):
        prev_hash = self.last_block.hash
        if prev_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block_info(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

app =  Flask(__name__)
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})
app.run(debug=True, port=5000)
