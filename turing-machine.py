#!/usr/bin/python

import sys

tape = list(sys.argv[1])

# set up initial, accept, and reject states
q0 = 0
qA = 'A'
qR = 'R'

# Set up delta function
delta = {}
delta[(0, '0')] = (1, '0', 'R')
delta[(0, 'b')] = ('A', 'b', 'R')
delta[(1, '0')] = (0, '0', 'R')


class TuringMachine:
  def __init__(self, q0, qA, qR, delta):
    self.q0 = q0
    self.qA = qA
    self.qR = qR
    self.delta = delta

  def inputTape(self, tape):
    tape = list(tape)

    end_tape, end_index, end_state = self.__processTape(tape, 0, self.q0)
    self.__printConfiguration(end_tape, end_index, end_state)
    if (end_state == self.qA):
      print 'ACCEPTED'
    elif (end_state == self.qR):
      print 'REJECTED'
    return

  def __printConfiguration(self, tape, index, state):
    configuration = tape[:index] + ['(q', str(state), ')'] + tape[index:]
    print ''.join(configuration)


  def __processTape(self, tape, index, state):
    self.__printConfiguration(tape, index, state)

    if (not (state, tape[index]) in self.delta):
      return tape, index, self.qR

    transition = self.delta[(state, tape[index])]

    new_state, new_symbol, head_move = transition
    new_index = self.__moveHead(tape, new_symbol, head_move, index)

    if (new_state == self.qA or new_state == self.qR):
      return (tape, new_index, new_state)

    return self.__processTape(tape, new_index, new_state)



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
 

tm = TuringMachine(q0, qA, qR, delta)
tm.inputTape(tape)

