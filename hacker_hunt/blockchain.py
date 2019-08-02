import requests
import time
import hashlib
from utils import consts
from threading import Thread
from settings import TOKEN


auth = {"Authorization": f"Token {TOKEN}"}


def get_last_proof():
    res = requests.get(
        f"{consts['bc_url']}{consts['last_proof']}",
        headers=auth
    )
    return res.json()


def mine(new_proof):
    res = requests.post(
        f"{consts['bc_url']}{consts['mine']}",
        headers=auth,
        json={"proof": f"{new_proof}"}
    )
    return res.json()


def valid_proof(last_proof, proof, difficulty):
    checksum = '0' * difficulty
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # print(guess_hash[:difficulty])
    return guess_hash[:difficulty] == checksum


# get last proof
last_proof_obj = get_last_proof()
last_proof = last_proof_obj['proof']
diff = last_proof_obj['difficulty']
time.sleep(last_proof_obj['cooldown'])


def proof_of_work(start_point):
    print("Mining new block")

    start_time = time.time()
    proof = int(start_point)
    # valid_proof(last_proof, proof, diff) is False
    while valid_proof(last_proof, proof, diff) is False:
        proof += 1

    print(f'POW: {start_point}')
    end_time = time.time()
    print(
        f'Block mined in {round(end_time-start_time, 2)}sec. Nonce: {str(proof)}')

    mine(proof)


if __name__ == "__main__":
    thread1 = Thread(target=proof_of_work(
        444444444444444444444444444444444444))
    thread2 = Thread(target=proof_of_work(
        88888888888888888888888888888888888888888888881))
    thread1.start()
    thread2.start()
    print("thread finished...exiting")
