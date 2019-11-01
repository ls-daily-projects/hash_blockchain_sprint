import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

from json.decoder import JSONDecodeError

import random


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
    """

    start = timer()

    last_proof_string = str(last_proof).encode()
    last_hex_hash = hashlib.sha256(last_proof_string).hexdigest()

    print("Searching for next proof")

    proof = start
    proof = random.randint(-sys.maxsize, sys.maxsize//2**48)

    while not valid_proof(last_hex_hash, proof):
        proof += random.randint(2**8, 2**16)

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?

    IE:  last_hash: ...AE9123456, new hash 123456888...
    """
    guess = f"{proof}".encode()
    guess_hex_hash = hashlib.sha256(guess).hexdigest()
    last_hash_last_6 = last_hash[-6:]
    guess_hash_first_6 = guess_hex_hash[:6]
    return guess_hash_first_6 == last_hash_last_6


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("blockchain/my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        try:
            data = r.json()
        except JSONDecodeError as error:
            print(error)
        finally:
            if data.get('message') == 'New Block Forged':
                coins_mined += 1
                print("Total coins mined: " + str(coins_mined))
            else:
                print(data.get('message'))
