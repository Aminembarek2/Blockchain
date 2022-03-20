from hashlib import sha256
from time import time
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()


    def create_genesis_block(self):
        self.chain.append(Block(1,"0000",[],0))

    def create_block(self,transactions_list):
        self.pr_hash_block = self.chain[-1].hash
        self.transactions_list = transactions_list
        self.chain.append(Block(len(self.chain)+1,self.pr_hash_block,self.transactions_list,self.proof_of_work(self.chain[-1].proof)))

    def proof_of_work(self, last_proof):
        proof = 0
        while self.validate_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def validate_proof(self,last_proof, proof):
        guess = f'{last_proof}{proof}'
        guess_hash = hash_block(guess)
        return guess_hash[:4] == "0000"

    def display_chain(self):
        for i in range(len(self.chain)):
            print("-------------------------")
            print(self.chain[i].data)
    
class Block:
    def __init__(self,index,pr_hash_block,transactions_list,proof):
        self.pr_hash_block = pr_hash_block
        self.transactions = []
        if type(transactions_list) is list:
            for i in transactions_list:
                self.transactions.append(i.transaction)
        else:
            self.transactions.append(transactions_list)
        self.unhashed_data = self.pr_hash_block+" "+json.dumps(self.transactions)
        self.hash = hash_block(self.unhashed_data)
        self.proof = proof
        self.create_data(index)

    def create_data(self,index):
        self.data = {
        'index':index,
        'timestamp':time(),
        'transactions': self.transactions,
        'proof':  self.proof,
        'previous_hash': self.pr_hash_block,
        }

class transaction:

    def __init__(self,sender,receiver,amount):
        self.transaction={
            'sender':sender,
            'receiver':receiver,
            'amount':amount,
        }
        

def hash_block(data):
    return sha256(data.encode()).hexdigest()

if __name__ == "__main__":
    chain = Blockchain()
    l1 = transaction("A","B",840)
    l2 = transaction("C","D",230)
    l3 = transaction("E","F",147)
    l4 = transaction("Alex","Bob",150)
    l5 = transaction("Test","Dinna",20)
    l6 = transaction("Elon","Fai",30)
    chain.create_block([l1,l2,l3])
    chain.create_block([l4,l5,l6])
    chain.create_block("X send Y 5 coins")
    chain.display_chain()

