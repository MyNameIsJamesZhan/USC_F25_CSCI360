# you can add imports but you should not rely on libraries that are not already provided in "requirements.txt #
from collections import deque 
from queue import PriorityQueue
from heapq import heappush, heappop

import numpy as np


class TextbookStack(object):
    """A class that tracks the"""

    def __init__(self, initial_order, initial_orientations):
        assert len(initial_order) == len(initial_orientations)
        self.num_books = len(initial_order)

        for i, a in enumerate(initial_orientations):
            assert i in initial_order
            assert a == 1 or a == 0

        self.order = np.array(initial_order)
        self.orientations = np.array(initial_orientations)

    def flip_stack(self, position):
        assert position <= self.num_books

        self.order[:position] = self.order[:position][::-1]
        self.orientations[:position] = np.abs(self.orientations[:position] - 1)[
            ::-1
        ]

    def check_ordered(self):
        for idx, front_matter in enumerate(self.orientations):
            if (idx != self.order[idx]) or (front_matter != 1):
                return False

        return True

    def copy(self):
        return TextbookStack(self.order, self.orientations)

    def __eq__(self, other):
        assert isinstance(
            other, TextbookStack
        ), "equality comparison can only ba made with other __TextbookStacks__"
        return all(self.order == other.order) and all(
            self.orientations == other.orientations
        )

    def __str__(self):
        return f"TextbookStack:\n\torder: {self.order}\n\torientations:{self.orientations}"


def apply_sequence(stack, sequence):
    new_stack = stack.copy()
    for flip in sequence:
        new_stack.flip_stack(flip)
    return new_stack


def a_star_search(stack):
    flip_sequence = []
    # --- v ADD YOUR CODE HERE v --- #
    visited = set()
    visited.add((tuple(stack.order), tuple(stack.orientations)))
    search_queue = PriorityQueue()
    length = stack.num_books+1
    for i in range(1,length):
        new_stack = stack.copy()
        new_stack.flip_stack(i)
        h = calculate_heuristic(new_stack)
        g = 1  # Cost of one flip
        f = g + h
        search_queue.put((f, [[i],new_stack]))
    while not search_queue.empty():
        flip_list = search_queue.get()[1]
        curr_stack = flip_list[1]
        curr_flip_sequence = flip_list[0]
        visited.add((tuple(curr_stack.order), tuple(curr_stack.orientations)))
        if curr_stack.check_ordered():
            flip_sequence = curr_flip_sequence
            break
        for i in range(1, length):
            new_stack = curr_stack.copy()
            new_stack.flip_stack(i)
            visited_check = (tuple(new_stack.order), tuple(new_stack.orientations))
            if visited_check not in visited:
                new_flip_sequence = curr_flip_sequence.copy()
                new_flip_sequence.append(i)
                h = calculate_heuristic(new_stack)
                g = len(new_flip_sequence)  # Cost is number of flips
                f = g + h
                search_queue.put((f, [new_flip_sequence,new_stack]))
        
    return flip_sequence
def calculate_heuristic(stack):
    # Calculate heuristic value based on pairs of books
    h = 0
    for i in range(stack.num_books-1):
        j = i+1
        # Check adjacency
        if abs(stack.order[i] - stack.order[j]) == 1:
            if abs(i - j) != 1:
                h += 1
        
        # Check orientations differ
        if stack.orientations[i] != stack.orientations[j]:
            h += 1
            
        # Check wrong order when both up
        if stack.orientations[i] == 1 and stack.orientations[j] == 1 and stack.order[i] - stack.order[j] == 1:
            if stack.order[i] > stack.order[j]:
                h += 1
                
        # Check wrong order when both down
        if stack.orientations[i] == 0 and stack.orientations[j] == 0 and stack.order[j] - stack.order[i] == 1:
            if stack.order[i] < stack.order[j]:
                h += 1
                    
    return h
def weighted_a_star_search(stack, epsilon=None, N=1):
    # Weighted A* is extra credit

    flip_sequence = []
    # --- v ADD YOUR CODE HERE v --- #

    return flip_sequence

    # ---------------------------- #


if __name__ == "__main__":
    test = TextbookStack(initial_order=[3, 2, 1, 0], initial_orientations=[0, 0, 0, 0])
    output_sequence = a_star_search(test)
    correct_sequence = int(output_sequence == [4])

    new_stack = apply_sequence(test, output_sequence)
    stack_ordered = new_stack.check_ordered()

    print(f"Stack is {'' if stack_ordered else 'not '}ordered")
    print(f"Comparing output to expected traces  - \t{'PASSED' if correct_sequence else 'FAILED'}")
    