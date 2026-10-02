import hashlib
import subprocess

def unsafe_eval(user_input):
    return eval(user_input)

def unsafe_command(user_input):
    subprocess.run(user_input, shell=True)

def weak_hash(value):
    return hashlib.md5(value.encode()).hexdigest()

print("Sample application")
