import sys

class Link (object):
  def __init__ (self, coeff = 1, exp = 1, next = None):
    self.coeff = coeff
    self.exp = exp
    self.next = next

  def __str__ (self):
    return '(' + str(self.coeff) + ', ' + str(self.exp) + ')'

class LinkedList (object):
  def __init__ (self):
    self.first = None
    
  # keep Links in descending order of exponents
  def insert_in_order (self, coeff, exp):
    new_node = Link(coeff, exp)
    current = self.first
    prev = self.first
    #empty list or greater exponent 
    if current == None or current.exp < new_node.exp:
        self.first = new_node
        new_node.next = current 
        return
        #no need to run through the other statements if we add to beginning of list 
    #traverse list 
    while current != None and new_node.exp <= current.exp:
        prev = current
        current = current.next
    #middle 
    if current != None and new_node.exp <= prev.exp:
        prev.next = new_node
        new_node.next = current
    #end of list 
    if current == None:
        prev.next = new_node
        return

  #combine like terms 
  def clt (self):
        sum_ll = LinkedList()
      # term i and term i + 1 
        current_n = self.first 

        #create i iteration 
        while current_n != None:
            coeff = current_n.coeff
            exp = current_n.exp
            next_n = current_n.next 
            while next_n != None:
                #if they have like exp 
                if current_n.exp == next_n.exp: 
                  coeff += next_n.coeff
                #if they dont have like exp 
                else:
                  current_n = next_n
                  if coeff != 0:
                    sum_ll.insert_in_order(coeff, exp)
                  break
                #tick next node 
                next_n = next_n.next      
            if next_n == None: 
                if coeff != 0:
                    sum_ll.insert_in_order(coeff, exp) 
                break
        return sum_ll

  # add polynomial p to this polynomial and return the sum
  def add (self, p):
      #sum linked list 
    presum_ll = LinkedList()
    current_s = self.first 
    current_p = p.first
    #iterate through our first poly and add each element to send to clt
    while current_s != None:
        presum_ll.insert_in_order(current_s.coeff, current_s.exp)
        current_s = current_s.next
    #iterate through second poly and add each ele to send to clt 
    while current_p != None:
        presum_ll.insert_in_order(current_p.coeff, current_p.exp)
        current_p = current_p.next
    #send to clt 
    postsum_ll = presum_ll.clt()
    #return summed ll 
    return postsum_ll

  # multiply polynomial p to this polynomial and return the product
  def mult (self, p):
    premult_ll = LinkedList() 

    current_s = self.first
    #do a loop in a loop to foil mult 
    while current_s != None: 
        current_p = p.first 
        while current_p != None:
            premult_ll.insert_in_order(current_s.coeff * current_p.coeff, current_s.exp + current_p.exp)
            current_p = current_p.next
        current_s = current_s.next
    postmult_ll = premult_ll.clt()
    return postmult_ll

  # create a string representation of the polynomial
  def __str__ (self):
      current = self.first 
      str_poly = ''
      while current != None: 
          if current.next != None:
              str_poly += str(current) + ' + '
          else:
              str_poly += str(current)
          current = current.next 
      return str_poly


def main():
  # read data from file poly.in from stdin
    #sys.stdin = open('poly.in.txt', 'r')
    num = int(sys.stdin.readline())
  # create polynomial p
    p = LinkedList()
    for i in range(num):
        p_split = sys.stdin.readline().split()
        p.insert_in_order(int(p_split[0]), int(p_split[1]))
    next(sys.stdin)
  # create polynomial q
    q = LinkedList()
    num = int(sys.stdin.readline())
    for i in range(num):
        q_split = sys.stdin.readline().split()
        q.insert_in_order(int(q_split[0]), int(q_split[1]))
  # get sum of p and q and print sum
    print(p.add(q))
  # get product of p and q and print product
    print(p.mult(q))

if __name__ == "__main__":
  main()
