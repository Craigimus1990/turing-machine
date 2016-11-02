#!/usr/bin/python

import sys

tape = list(sys.argv[1])

# set up initial, accept, and reject states
q0 = 0
qA = 'A'
qR = 'R'

# Set up delta function
delta = {}
delta[(0, '0')] = (0, '0', 'R')
delta[(0, '1')] = (0, '1', 'R')
delta[(0, 'b')] = (1, 'b', 'L')
delta[(1, '1')] = (2, 'b', 'R')
delta[(2, 'b')] = (3, '1', 'L')
delta[(3, 'b')] = (1, 'b', 'L')
delta[(1, '0')] = (4, 'b', 'R')
delta[(4, 'b')] = (5, '0', 'L')
delta[(5, 'b')] = (1, 'b', 'L')
delta[(1, 'b')] = ('A', '$', 'R')
delta[(6, 'b')] = ('A', '$', 'R')

tm = TuringMachine(q0, qA, qR, delta)
tm.inputTape(tape)


class TuringMachine:
  def __init__(self, q0, qA, qR, delta):
    self.q0 = q0
    self.qA = qA
    self.qR = qR
    self.delta = delta

  def inputTape(self, tape):
	tape = list(tape)
    end_tape, end_index, end_state = self.__processTape(tape, 0, q0)
    configuration = end_tape[:end_index] + ['(q', end_state, ')'] + end_tape[end_index:]
    print ''.join(configuration)
    if (end_state == self.qA):
      print 'ACCEPTED'
    elif (end_state == self.qR):
      print 'REJECTED'
    return


  def __processTape(self, tape, index, state):
    transition = self.delta[(state, tape[index])]

    if (!transition):
      return tape, index, self.qR

    new_state, new_symbol, head_move = transition
    new_index = self.__moveHead(tape, new_symbol, head_move, index)

    if (new_state == self.qA or new_state == self.qR):
      return tape, new_index, new_stae

	self.__processTape(tape, new_index, new_state)



  def __moveHead(self, tape, symbol, move, index):
    if (move.upper() == 'R'):
      tape[index] = symbol
      index += 1

      if (tape.__len__() <= index):
        tape.append('b') # if we run off the input tape append blanks

    elif (move.upper() == 'L'):
      tape[index] = symbol
      index -= 1
      index = max(0, index)

    return index
 
