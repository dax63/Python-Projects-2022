import sys

# Input: takes as input a positive integer n
# Output: returns True if n is prime and False otherwise
def is_prime ( n ):
  if (n == 1):
    return False

  limit = int (n ** 0.5) + 1
  div = 2
  while (div < limit):
    if (n % div == 0):
      return False
    div += 1
  return True

# Input: takes as input a string in lower case and the size
#        of the hash table 
# Output: returns the index the string will hash into
def hash_word (s, size):
  hash_idx = 0
  for j in range (len(s)):
    letter = ord (s[j]) - 96
    hash_idx = (hash_idx * 26 + letter) % size
  return hash_idx

# Input: takes as input a string in lower case and the constant
#        for double hashing 
# Output: returns the step size for that string 
def step_size (s, const):
    #step size reduces collisions 
    #finds hash of s using constant instead of len(table)
    step = hash_word(s, const)
    return const - step

# Input: takes as input a string and a hash table 
# Output: no output; the function enters the string in the hash table, 
#         it resolves collisions by double hashing
def insert_word (s, hash_table):
    idx = hash_word(s, len(hash_table))
    if hash_table[idx] == '': #if hash table index is empty 
        hash_table[idx] = s #populate bucket with word
    else:
        ind = 1
        step = step_size(s, 7) #hmmm
        new_index = (idx+ ind * step) % len(hash_table) #hmm
        #we have to check the new hashes with double hashing to find next empty bucket
        while (hash_table[new_index]): 
            new_index = (idx + ind * step) % len(hash_table) # for collisions 
            ind += 1
        hash_table[new_index] = s

# Input: takes as input a string and a hash table 
# Output: returns True if the string is in the hash table 
#         and False otherwise
def find_word (s, hash_table):
    idx = hash_word(s, len(hash_table))
    #we need to make sure original hash is s 
    if hash_table[idx] == s:
        return True
    else:
        ind = 1
        step = step_size(s, 7)
        new_index = (idx + ind * step) % len(hash_table)
        #we need to find empty string 
        while (hash_table[new_index] and hash_table[new_index] != s):
            new_index = (idx + ind * step) % len(hash_table)
            ind += 1
        if hash_table[new_index] == s:
            return True
        else:
            return False 

# Input: string s, a hash table, and a hash_memo 
#        recursively finds if the string is reducible
# Output: if the string is reducible it enters it into the hash memo 
#         and returns True and False otherwise
def reducible_helper(s):
    sslist = []
    for i in range(len(s)):
        sslist.append(s[0:i] + s[i + 1:]) #from first letter to i then from next after i to end
    return sslist

def is_reducible (s, hash_table, hash_memo):
    ticker = False
    if ('a' not in s and 'o' not in s and 'i' not in s):
        return False 
    if (len(s) == 1 and (s == 'a' or s == 'o' or s == 'i')):
        if find_word(s, hash_memo) is False:
            insert_word(s, hash_memo)
        return True
    if find_word(s, hash_memo) is True:
        return True
    else: 
        for sslist in reducible_helper(s):
            if find_word(sslist, hash_table) is False and (sslist != 'i' and sslist != 'o' and sslist != 'a'):
                continue
            elif is_reducible(sslist, hash_table, hash_memo) is True:
                if find_word(s, hash_memo) is False:
                    insert_word(s, hash_memo)
                ticker = True
    
    return ticker
    
# Input: string_list a list of words
# Output: returns a list of words that have the maximum length
def get_longest_words (string_list):
    max_len = 1
    listolongest = []

    for word in string_list:
        if len(word) == max_len: 
            listolongest.append(word)
        elif len(word) > max_len:
            max_len = len(word)
            listolongest.clear()
            listolongest.append(word)
    
    return listolongest

def main():
  # create an empty word_list
  word_list = []

  # read words from words.txt and append to word_list
  #sys.stdin = open('word_list.in.txt', 'r')   #COMMENT OUT THIS LINE
  for line in sys.stdin:
    line = line.strip()
    word_list.append (line)

  # find length of word_list
  lenlist = len(word_list)

  # determine prime number N that is greater than twice
  # the length of the word_list
  next_prime = lenlist * 2 + 1
  while not is_prime(next_prime):
      next_prime += 2

  # create an empty hash_list
  hash_list = []

  # populate the hash_list with N blank strings
  # we use next prime because it is the length of our hash list 
  for i in range(next_prime):
      hash_list.append('')

  # hash each word in word_list into hash_list
  # for collisions use double hashing 
  for word in word_list:
      insert_word(word, hash_list)

  # create an empty hash_memo of size M
  # we do not know a priori how many words will be reducible
  # let us assume it is 10 percent (fairly safe) of the words
  # then M is a prime number that is slightly greater than 
  # 0.2 * size of word_list
  M = int(0.2 * lenlist)
  while not(is_prime(M)):
      M += 1
  
  #hash memo is where we store all the past reducible words because we want to go backwards 
  hash_memo = []
 

  # populate the hash_memo with M blank strings
  for j in range(M):
      hash_memo.append('')

  # create an empty list reducible_words
  reducible_words = []

  # for each word in the word_list recursively determine
  # if it is reducible, if it is, add it to reducible_words
  # as you recursively remove one letter at a time check
  # first if the sub-word exists in the hash_memo. if it does
  # then the word is reducible and you do not have to test
  # any further. add the word to the hash_memo.
  for word in word_list:
      if (is_reducible(word, hash_list, hash_memo)):
          reducible_words.append(word)

  # find the largest reducible words in reducible_words
  largestword = get_longest_words(reducible_words)
  # print the reducible words in alphabetical order
  largestword.sort()

  # one word per line
  for word in largestword:
      print(word)

if __name__ == "__main__":
  main()

'''
To run this program on a Mac do

python3 Reducible.py < words.txt
'''