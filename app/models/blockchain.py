import hashlib
import json
from time import time
import copy
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

        block = {
            'index': len(self.chain) + 1,
            'timestamp': int(time()),
            'transactions': self.memPool,
            'merkleRoot': '0'*64,
            'nonce': nonce,
            'previousHash': previousHash or self.generateHash(previousBlockCopy),
        }

        self.memPool = []
        self.chain.append(block)
        return block

    def addNewMiners(self, nodes):
        for node in nodes:
            self.nodes.add(node)
        print(self.nodes)
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
        print(self.memPool)
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
        #ta vindo um b esquisito
        transaction["signature"] = str(self.sign(privKey, transaction))[2:-1]
        self.memPool.append(transaction)
        return "transaçao realizada"

    @staticmethod
    def generateMerkleRoot(transactions):
        if len(hashList) == 1:
            return hashList[0]
        newHashList = [] 
        for i in range(0, len(hashList)-1, 2):
            newHashList.append(hash2(hashList[i], hashList[i+1]))
        if len(hashList) % 2 == 1: # odd, hash last item twice
            newHashList.append(hash2(hashList[-1], hashList[-1]))
        return merkle(newHashList)

    def hash2(a, b):
        a1 = a.decode('hex')
        a11 = a1[::-1]
        b1 = b.decode('hex')[::-1]
        concat = a11+b1
        concat2 = hashlib.sha256(concat).digest()
        print ("hash1:" + concat2.encode('hex'))
        h = hashlib.sha256(concat2).digest()
        print ("hash2:" + h[::-1].encode('hex'))
        print ('')
        return h[::-1].encode('hex')
 
# Teste
# blockchain = Blockchain()

# sender = '19sXoSbfcQD9K66f5hwP5vLwsaRyKLPgXF'
# recipient = '1MxTkeEP2PmHSMze5tUZ1hAV3YTKu2Gh1N'

# Cria 5 blocos, incluindo o Genesis, contendo de 1-4 transações cada, com valores aleatórios, entre os endereços indicados em sender e recipient.
# for x in range(0, 4): 
#     for y in range(0, random.randint(1,4)) : 
#         timestamp = int(time())
#         amount = random.uniform(0.00000001, 100)
#         blockchain.createTransaction(sender, recipient, amount, timestamp, 'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U')
#     blockchain.createBlock()
#     blockchain.mineProofOfWork(blockchain.prevBlock)

# blockchain.printChain()

