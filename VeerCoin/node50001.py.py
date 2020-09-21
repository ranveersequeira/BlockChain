#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 21:00:28 2020

@author: ranveersequeira
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 21:43:29 2020

@author: ranveersequeira
"""


import datetime
import hashlib
import json
from flask import Flask,jsonify

#BUILDING A BLOCKCHAIN

class Blockchain:
    #all components of block
    def __init__(self):
        self.chain = []
        #we'll define this function later.used to create blocks
        self.create_block(proof = 1 , prev_hash = '0')
        
        
    def create_block(self,proof,prev_hash):
        block = {"index":len(self.chain)+1 ,
                 "timestamp": "datetime.datetime.now()",
                 "proof" : proof,
                 "prev_hash": prev_hash
                 #we can add data too
                 }
        self.chain.append(block)
        return block
    #method to get prev_block which is usually last element in block list
    def get_prev_block(self):
        return self.chain[-1]
    
    
    
    #method to define proof of work
    def poW(self,prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #using hash function
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            
            if(hash_operation[:4] == "0000"):
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    #method to check & verify
    def hash(self,block):
        #use json to dumps block to convert it into string
        encoded_block = json.dumps(block,sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    #take the chain and check every block
    def isValid(self,chain):
        prev_block = chain[0]
        block_idx = 1
        while block_idx < len(chain):
            block = chain[block_idx]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            prev_block = block
            block_idx += 1
            
        return True
    
    
    
    #Flask based web pack
app  = Flask(__name__)

#instance object of blockchain
blockchain = Blockchain()


#mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.poW(prev_proof)
    prev_hash = blockchain.hash(prev_block) 
    block = blockchain.create_block(proof , prev_hash)
    response = {'message':"Woooh! Did you see that?",
                'index' :block['index'],
                'timestamps' : block['timestamp'],
                'proof' : block['proof'],
                'prev_hash' : block['prev_hash']
                }
    return jsonify(response),200 


#to display full blockchain
@app.route('/get_chain' , methods = ['GET'])

def get_chain():
    response = {'chian':blockchain.chain,
                'length' : len(blockchain.chain)
            }
    return jsonify(response),200


@app.route('/is_valid' , methods = ['GET'])
def is_valid():
    isvalid = blockchain.isValid(blockchain.chain)
    if isvalid:
        response = {"message":"Blockhain is valid"}
    else:
        response = {'message': "Blockchain is not valid"}
        
    return jsonify(response) , 200



    




#lets run out of here
    
app.run(host = '0.0.0.0' , port = 5001)




    
    
            
                
        
        
        
    
    
    
            
            
            
            
    
    
        
        
        
        