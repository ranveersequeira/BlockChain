#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 20:46:09 2020



@author: ranveersequeira
"""
#Creating CryptoCurrency


import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests 
from uuid import uuid4
from urllib.parse import urlparse
#BUILDING A BLOCKCHAIN

class Blockchain:
    #all components of block
    def __init__(self):
        self.chain = []
        self.transactions = []
        #we'll define this function later.used to create blocks
        self.create_block(proof = 1 , prev_hash = '0')
        self.nodes = set()
        
        
    def create_block(self,proof,prev_hash):
        block = {"index":len(self.chain)+1 ,
                 "timestamp": str(datetime.datetime.now()),
                 "proof" : proof,
                 "prev_hash": prev_hash,
                 "transactions" : self.transactions}
        self.transactions = []
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
    
    
    def add_transactions(self,sender, receiver,amount):
        self.transactions.append({'sender':sender,
                                  'receiver' : receiver,
                                  'amount' : amount})
    
        prev_block = self.get_prev_block()
        return prev_block['index'] + 1
    
    def add_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
        #consensus function
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        for nodes in network:
            response = requests.get('http://{node}/get_chain') 
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length>max_length and self.isValid(chain):
                    max_length = length
                    longest_chain = chain
                
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
    
                    
            
    
    #Flask based web pack
app  = Flask(__name__)

#creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

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


#adding transaction to the block

@app.route('/add_transaction' , methods = ['POST'])

def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver' , 'amount']
    if not all (key in json for key in transaction_keys):
        return "Something Missing",400
    index = blockchain.add_transactions(json['sender'], json['receiver'] , json['amount'])
    response = {'message': f'Added at {index} '
        }    
    return jsonify(response),201


#Decentralize the network/blockchain

#connection new nodes
@app.route('/connect_node' , methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes  = json.get('nodes')
    if nodes is None:
        return "NO Node",400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message' : 'All Nodes are connected',
               'total_nodes' : list(blockchain.nodes)}
    return jsonify(response),201


#replacing the chain with longest chain
@app.route('/replace_chain' , methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    
    if is_chain_replaced:
        response = {"message":"Replaced with the longest chain",
                    'new_chain': blockchain.chain}
    else:
        response = {'message': "No Change in Chain",
                    'actual_chain' : blockchain.chain}
        
        
    return jsonify(response) , 200

    



#lets run out of here
    
app.run(host = '0.0.0.0' , port = 5000)




    
    
            
                
        
        
        
    
    
    
            
            
            
            
    
    
        
        
        
        