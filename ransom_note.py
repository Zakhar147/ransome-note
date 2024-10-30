import sys
import time #for time measure
from collections import Counter, defaultdict
from tqdm import tqdm #for loading bar

def Counter_method(message, magazine):
    """
    Method to check if a message can be constructed
    from the magazine's contents using pre-character counting.
    """
    msg_count = Counter(message)
    mag_count = Counter(magazine)
    
    for char, count in msg_count.items():
        if count > mag_count.get(char, 0):#using .get(char,0) for missing KeyError
            return False
    return True

def dict_method(message, magazine):
    """
    Method to check if a message can be constructed
    from the magazine's contents using a dictionary for char counts.
    """
    char_count = defaultdict(int)
    for char in magazine:
        char_count[char] += 1
    
    for char in message:
        if char_count[char] == 0:
            return False
        char_count[char] -= 1

    return True

def set_method(message, magazine):
    """
    Method to check if a message can be constructed
    from the magazine's contents using set and count comparisons.
    It's the most optimal method.
    """
    # using set to filter duplicate characters
    unique_chars = set(message)

    for char in unique_chars:
        """
        if there are not enough instances for at least one symbol type,
        then it is impossible to assemble a message
        """
        if magazine.count(char) < message.count(char):
            return False

    return True

def measure_time(func, *args):
    """
    Measure the execution time of a given function with arguments.
    """
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, end_time - start_time

def process_txt(txt: str):
    """
    Process the input strings by converting them to lowercase
    and removing non-alphanumeric characters.
    """
    return ''.join(c.lower() for c in txt if c.isalnum())

def bench(iters: int, func, *args):
    name = func.__name__
    total_time = 0

    for _ in tqdm(range(iters), desc=f"{name} progress"):
        _, time_taken = measure_time(func, *args)
        total_time += time_taken

    print(f"{name} total time for {iters} "
            f"calls: {total_time:.4f} seconds, "
            f"result: {func(*args)}\n")

def benchmark_mode(message: str, magazine: str, iters: int):
    print('benchmark_mode')
    methods = (Counter_method, dict_method, set_method)
    
    for meth in methods:
        bench(iters, meth, message, magazine)

def main():
    # Handle command-line arguments
    usage = """
    Usage: *python ransom_note.py [message.txt] [magazine.txt] [iters]*

    Arguments:
    - `message.txt`: Path to the text file containing the message.
    - `magazine.txt`: Path to the text file containing the magazine.
    - `iters` (optional): Number of iterations for benchmark mode. If omitted, the program runs in normal mode and returns `True` or `False.
"""
    
    if len(sys.argv) <= 2 or len(sys.argv) > 4:
        return usage
        
    message_file = sys.argv[1] 
    magazine_file = sys.argv[2]
    iters = int(sys.argv[3]) if len(sys.argv) > 3 else None

    # Attempt to read the files and handle potential errors
    try:
        if not message_file.endswith('.txt'):
            raise ValueError(f"Error! {message_file} is not a txt file!")
        if not magazine_file.endswith('.txt'):
            raise ValueError(f"Error! {magazine_file} is not a txt file")    

        with open(message_file, 'r') as msg_file:
            message = msg_file.read()
        with open(magazine_file, 'r') as mag_file:
            magazine = mag_file.read()
    except ValueError as e: 
        return str(e)
    except IOError as e:
        return(f"Error opening files: {str(e)}")

    if not message.strip():
        return("Error! Message is empty.")
    if not magazine.strip():
        return("Error! Magazine is empty.")
    
    processed_message = process_txt(message)
    processed_magazine = process_txt(magazine)

    # if the magazine has fewer 
    # alphanumeric characters than the message
    # which means it is impossible to assemble the message
    if len(processed_message) > len(processed_magazine):
        return False

    if iters is None:
        # Normal mode
        # Using set_method() because it is the fastest
        return set_method(processed_message, processed_magazine) 

    else:
        benchmark_mode(processed_message, processed_magazine, iters)
        return ""

if __name__ == "__main__":
    print(main())

