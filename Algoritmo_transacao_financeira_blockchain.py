# Um exemplo básico de algoritmo de transação financeira usando a tecnologia Blockchain:
# (Nelson Nishiwaki)
# 1. Verificar a identidade do remetente e do destinatário da transação.
# 2. Verificar se o remetente tem saldo suficiente para realizar a transação.
# 3. Criar uma transação e incluir as informações necessárias, como o endereço do remetente, o endereço do destinatário e o valor a ser transferido.
# 4. A transação é transmitida para a rede Blockchain e enviada a todos os nós na rede.
# 5. Os nós na rede validam a transação e a adicionam a um bloco.
# 6. Uma vez que a maioria dos nós na rede tenha validado a transação, ela é confirmada e adicionada ao registro público (o Blockchain).
# 7. O saldo do remetente é atualizado para refletir a transação.
# 8. O destinatário é notificado de que a transação foi concluída.

import hashlib
import json
import time

class Blockchain:
    
    def _init_(self):
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=1, previous_hash='0')
        
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof*2 - previous_proof*2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof*2 - previous_proof*2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
        })
    
    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['sender'] == address:
                    balance -= transaction['amount']
                elif transaction['receiver'] == address:
                    balance += transaction['amount']
        return balance

blockchain = Blockchain()
blockchain.add_transaction('Alice', 'Bob', 1)
blockchain.add_transaction('Bob', 'Charlie', 2)
blockchain.add_transaction('Charlie', 'Alice', 3)
previous_block = blockchain.get_previous_block()
previous_proof = previous_block['proof']
proof = blockchain.proof_of_work(previous_proof)
previous_hash = blockchain.hash(previous_block)
block = blockchain.create_block(proof, previous_hash)

print(blockchain.chain)
print(blockchain.get_balance('Alice'))
print(blockchain.get_balance('Bob'))
print(blockchain.get_balance('Charlie'))
