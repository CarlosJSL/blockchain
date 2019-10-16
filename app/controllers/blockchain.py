from app import app
import json
from app.models.blockchain import Blockchain

@app.route("/") 
def index():
    return "Hello world"

@app.route("/transactions/create", methods=['POST']) 
def createTransactions():
    return 'Transactions route'

@app.route("/transactions/mempool", methods=['GET']) 
def getMemPool():
    return 'Mempool route'

@app.route("/mine", methods=['GET']) 
def mine():
    return 'Mine route'

@app.route("/chain", methods=['GET']) 
def getChain():
    return Blockchain.printChain()
  
@app.route("/nodes/register", methods=['POST']) 
def registerNode():
    return 'Nodes register route'
  
@app.route("/nodes/resolve", methods=['GET']) 
def resolveNodes():
    return 'Nodes resolve route'