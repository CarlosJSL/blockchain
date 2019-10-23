import hashlib
import json
from time import time
import copy
import requests
from bitcoin.wallet import CBitcoinSecret
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage
import random

DIFFICULTY = 4 # Quantidade de zeros (em hex) iniciais no hash válido.

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.nodes = set()
        self.createGenesisBlock()

    def createGenesisBlock(self):
        self.createBlock(previousHash='0'*64, nonce=0)
        self.mineProofOfWork(self.prevBlock) 

    def createBlock(self, nonce=0, previousHash=None):
        if (previousHash == None):
            previousBlock = self.chain[-1]
            previousBlockCopy = copy.copy(previousBlock)
            previousBlockCopy.pop("transactions", None)
        mempool = self.hashlist(self.memPool)
        block = {
            'index': len(self.chain) + 1,
            'timestamp': int(time()),
            'transactions': self.memPool,
            'merkleRoot': self.generateMerkleRoot(mempool) if (len(self.memPool) > 0) else '0'*64,
            'nonce': nonce,
            'previousHash': previousHash or self.generateHash(previousBlockCopy),
        }
        self.memPool = []
        self.chain.append(block)
        return block

    @staticmethod
    def hashlist(mempool):
        hash_list = []
        for t in mempool:
            transaction_object = json.dumps(t, sort_keys=True).encode()
            hash_list.append(hashlib.sha256(transaction_object).hexdigest())
        return hash_list

    def addNewMiners(self, nodes):
        for node in nodes:
            self.nodes.add(node)
        return self.nodes
        
    @staticmethod
    def generateHash(data):
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()

    def mineProofOfWork(self, prevBlock):
        nonce = 0
        while self.isValidProof(prevBlock, nonce) is False:
            nonce += 1
        return nonce

    @staticmethod
    def isValidProof(block, nonce):
        block['nonce'] = nonce
        guessHash = Blockchain.getBlockID(block)
        return guessHash[:DIFFICULTY] == '0' * DIFFICULTY 

    @staticmethod
    def getBlockID(block):
        blockCopy = copy.copy(block)
        blockCopy.pop("transactions", None)
        return Blockchain.generateHash(blockCopy)

    def printChain(self):
        return json.dumps(self.chain, indent=2, sort_keys=True)

    @property
    def prevBlock(self):
        return self.chain[-1]
    
    @property
    def getMem(self):
        return self.memPool

    def printMemPool(self):
        return json.dumps(self.memPool, indent=2, sort_keys=True)

    @staticmethod
    def sign(privKey, message):
        secret = CBitcoinSecret(privKey)
        
        msg = BitcoinMessage(json.dumps(message))
        return SignMessage(secret, msg)
        
    @staticmethod
    def verifySignature(address, signature, message):
        msg = BitcoinMessage(message)
        return VerifyMessage(address, msg, signature)

    def createTransaction(self, sender, recipient, amount):
        privKey = 'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U'
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": int(time())  
        }
        #strange b
        transaction["signature"] = str(self.sign(privKey, transaction))[2:-1]
        self.memPool.append(transaction)
        return "transaçao realizada"

    @staticmethod
    def generateMerkleRoot(hashList):
        if len(hashList) == 1:
            return hashList[0]
        newHashList = [] 
        for i in range(0, len(hashList)-1, 2):
            newHashList.append(Blockchain.hash2(hashList[i], hashList[i+1]))
        if len(hashList) % 2 == 1:
            newHashList.append(Blockchain.hash2(hashList[-1], hashList[-1]))
        return Blockchain.generateMerkleRoot(newHashList)

    @staticmethod
    def hash2(a, b):

        a11 = a[::-1]
        b1 = b[::-1]
        concat = a11+b1
        concat2 = hashlib.sha256(str(concat).encode('utf-8')).hexdigest()
        h = hashlib.sha256(str(concat2).encode('utf-8')).hexdigest()
        return h[::-1]

    def isValidChain(self, blockchain):
        for block in blockchain:
            block_hash = self.getBlockID(block)
            if block_hash[:DIFFICULTY] == '0' * DIFFICULTY: 
                return True
            else:
                return False

    def resolveConflicts(self):
        for node in self.nodes:
            response = requests.get(node+'/chain')
            blockchain = response.json()
            if len(blockchain) > len(self.chain):
                if self.isValidChain(blockchain):
                    self.chain = blockchain
        
        return 'conflitos resolvidos'
                