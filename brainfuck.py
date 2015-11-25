#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Brainfuck is an esoteric programming language noted for its extreme minimalism.
The language consists of only eight simple commands and an instruction pointer.
It is designed to challenge and amuse programmers,
and was not made to be suitable for practical use.
It was created in 1993 by Urban Müller.

Copyright (c) 2015 QoQo
License: MIT (see README.rst for details)

"""

from enum import Enum

########################################################################
# Exception  ###########################################################
########################################################################


# All brainfuck exceptions should also be derived from this class.
class BrainfuckError(Exception):
    pass


# Raised when the parser encounters a syntax error.
class BrainfuckSyntaxError(BrainfuckError):
    pass


# Raised when an runtime error is detected
class BrainfuckRuntimeError(BrainfuckError):
    pass


########################################################################
# Context  #############################################################
########################################################################

class Context(object):
    __slots__ = ['__in', '__out', '__pc', '__cur', '__memory']
        
    def __init__(self, **kwargs):
        self.__pc, self.__cur, self.__memory = 0, 0, [0]
            
        """ """
        self.__in = kwargs.get('input', lambda: ord(input().strip()))
            
        """ """
        self.__out = kwargs.get('output', lambda value: print(value, end=''))
        
    @property
    def pc(self):
        return self.__pc
        
    @pc.setter
    def pc(self, value):
        self.__pc = value
        
    @property
    def cur(self):
        return self.__cur
        
    @cur.setter
    def cur(self, value):
        self.__cur = value
        
    @property
    def memory(self):
        return self.__memory
        
    def load(self):
        return self.__in()
        
    def store(self, value):
        self.__out(value)


########################################################################
# Brainfuck  ###########################################################
########################################################################

class Brainfuck(object):

    ########################################################################
    # Symbol  ##############################################################
    ########################################################################

    class Symbol(Enum):
        LSHIFT = '<'
        RSHIFT = '>'
        PLUS = '+'
        MINUS = '-'
        DOT = '.'
        COMMA = ','
        LBRACKET = '['
        RBRACKET = ']'

        @classmethod
        def symbols(cls):

            """ Get a symbol list for brainfuck. """
            return ['<', '>', '+', '-', '.', ',', '[', ']']

    ########################################################################
    # Command  #############################################################
    ########################################################################

    class Command(object):

        def __init__(self, token, bracemap=None):

            """ Creating the brainfuck commands. """
            self.__token, self.__bracemap = token, bracemap

            if token == Brainfuck.Symbol.LSHIFT:
                self.__eval = self.__lshift
            elif token == Brainfuck.Symbol.RSHIFT:
                self.__eval = self.__rshift
            elif token == Brainfuck.Symbol.PLUS:
                self.__eval = self.__plus
            elif token == Brainfuck.Symbol.MINUS:
                self.__eval = self.__minus
            elif token == Brainfuck.Symbol.DOT:
                self.__eval = self.__dot
            elif token == Brainfuck.Symbol.COMMA:
                self.__eval = self.__comma
            elif token == Brainfuck.Symbol.LBRACKET:
                self.__eval = self.__lbracket
            elif token == Brainfuck.Symbol.RBRACKET:
                self.__eval = self.__rbracket

        def __lshift(self, context):
            # increment the data pointer
            # (to point to the next cell to the right)
            context.cur -= 1
            if context.cur < 0:
                raise BrainfuckRuntimeError('Subscript out of range.')

        def __rshift(self, context):
            # increment the data pointer
            # (to point to the next cell to the right).
            context.cur += 1
            if context.cur == len(context.memory):
                context.memory.append(0)

        def __plus(self, context):
            # increment (increase by one) the byte at the data pointer.
            cur, memory = context.cur, context.memory
            memory[cur] = memory[cur] + 1 if memory[cur] < 255 else 0

        def __minus(self, context):
            # decrement (decrease by one) the byte at the data pointer.
            cur, memory = context.cur, context.memory
            memory[cur] = memory[cur] - 1 if memory[cur] > 0 else 255

        def __dot(self, context):
            # output the byte at the data pointer.
            context.store(chr(context.memory[context.cur]))

        def __comma(self, context):
            # accept one byte of input,
            # storing its value in the byte at the data pointer.
            context.memory[context.cur] = context.load()

        def __lbracket(self, context):
            if context.memory[context.cur] == 0:
                context.pc = self.__bracemap[context.pc]

        def __rbracket(self, context):
            if context.memory[context.cur] != 0:
                context.pc = self.__bracemap[context.pc]

        def __call__(self, context):
            self.__eval(context)

    ########################################################################
    # Interpreter  #########################################################
    ########################################################################

    def __init__(self, code):
        self.__code = code
        self.__commands, self.__bracemap = self.__class__.pause(code)

    def __len__(self):
        return len(self.__commands)

    @property
    def code(self):
        return self.__code

    def execute(self, **kwargs):
        context = kwargs.get('context', Context())
        while context.pc < len(self):
            token, bracemap = self.__commands[context.pc], self.__bracemap
            command = self.__class__.Command(token, bracemap)
            command(context)
            context.pc += 1

    @classmethod
    def pause(cls, code):

        """ Parse the input string. """
        commands = []
        bracestack, bracemap = [], {}
        command_lists = filter(lambda c: c in cls.Symbol.symbols(), code)
        for index, symbol in enumerate(command_lists):
            token = cls.Symbol(symbol)
            if token == cls.Symbol.LBRACKET:
                bracestack.append(index)
            if token == cls.Symbol.RBRACKET:
                if not bracestack:
                    raise BrainfuckSyntaxError("syntax error, unexpected ']'")
                start = bracestack.pop()
                bracemap[start] = index
                bracemap[index] = start
            commands.append(token)

        if bracestack:
            raise BrainfuckSyntaxError("syntax error, unexpected '['")
        return (commands, bracemap)
