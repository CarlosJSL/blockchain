from app import app
import json
from flask import request
from app.models.blockchain import Blockchain
blockChain = Blockchain()

@app.route("/") 
def index():
    return "Hello world"

@app.route("/transactions/create", methods=['POST']) 
def createTransactions():
    data = request.get_json()
    return blockChain.createTransaction(data.get('sender', ''), data.get('recipient', ''), data.get('amount', ''))

@app.route("/transactions/mempool", methods=['GET']) 
def getMemPool():
    return blockChain.printMemPool()

@app.route("/mine", methods=['GET']) 
def mine():
    if len(blockChain.getMem) > 0:
        newblock = blockChain.createBlock()
        blockChain.mineProofOfWork(newblock)
        return 'bloco minerado com sucesso'
    else:
        return 'não existem blocos disponiveis'

@app.route("/chain", methods=['GET']) 
def getChain():
    return blockChain.printChain()
  
@app.route("/nodes/register", methods=['POST']) 
def registerNode():
    data = request.get_json()
    blockChain.addNewMiners(data)
    return 'Nodes register route'
  
@app.route("/nodes/resolve", methods=['GET']) 
def resolveNodes():
    return 'Nodes resolve route'