# you can add imports but you should not rely on libraries that are not already provided in "requirements.txt #
from collections import deque
import numpy as np

class TextbookStack(object):
    """ A class that tracks the """
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
        self.orientations[:position] = np.abs(self.orientations[:position] - 1)[::-1]

    def check_ordered(self):
        for idx, front_matter in enumerate(self.orientations):
            if (idx != self.order[idx]) or (front_matter != 1):
                return False

        return True

    def copy(self):
        return TextbookStack(self.order, self.orientations)
    
    def __eq__(self, other):
        assert isinstance(other, TextbookStack), "equality comparison can only ba made with other __TextbookStacks__"
        return all(self.order == other.order) and all(self.orientations == other.orientations)

    def __str__(self):
        return f"TextbookStack:\n\torder: {self.order}\n\torientations:{self.orientations}"


def apply_sequence(stack, sequence):
    new_stack = stack.copy()
    for flip in sequence:
        new_stack.flip_stack(flip)
    return new_stack

def breadth_first_search(stack):
    flip_sequence = []
    # --- v ADD YOUR CODE HERE v --- #
    visited = set()
    visited.add((tuple(stack.order), tuple(stack.orientations)))
    search_queue = deque()
    length = stack.num_books+1
    for i in range(1,length):
        new_stack = stack.copy()
        new_stack.flip_stack(i)
        search_queue.append([[i],new_stack])
    while search_queue:
        flip_list = search_queue.popleft()
        curr_stack = flip_list[1]
        curr_flip_sequence = flip_list[0]
        #print("curr flip seq: ", curr_flip_sequence)
        #print("curr book stack: " + str(curr_stack))
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
                search_queue.append([new_flip_sequence,new_stack])
        
    return flip_sequence
    # ---------------------------- #


def depth_first_search(stack):
    flip_sequence = []
    
    # --- v ADD YOUR CODE HERE v --- #
    visited = set()
    visited.add((tuple(stack.order), tuple(stack.orientations)))
    search_stack = []
    length = stack.num_books+1
    for i in range(1,length):
        new_stack = stack.copy()
        new_stack.flip_stack(i)
        search_stack.append([[i],new_stack])
    while search_stack:
        flip_list = search_stack.pop()
        curr_stack = flip_list[1]
        curr_flip_sequence = flip_list[0]
        #print("curr flip seq: ", curr_flip_sequence)
        #print("curr book stack: " + str(curr_stack))
        visited.add((tuple(curr_stack.order), tuple(curr_stack.orientations)))
        if curr_stack.check_ordered():
            flip_sequence = curr_flip_sequence
            break
        for i in range(1,length):
            new_stack = curr_stack.copy()
            new_stack.flip_stack(i)
            visited_check = (tuple(new_stack.order), tuple(new_stack.orientations))
            if visited_check not in visited:
                new_flip_sequence = curr_flip_sequence.copy()
                new_flip_sequence.append(i)
                search_stack.append([new_flip_sequence,new_stack])
        
    return flip_sequence
    # ---------------------------- #



# test = TextbookStack(initial_order=[3, 2, 1, 0], initial_orientations=[0, 0, 0, 0])
# output_sequence = depth_first_search(test)
# print(output_sequence) # Should give you [4]


# new_stack = apply_sequence(test, output_sequence)
# stack_ordered = new_stack.check_ordered()
# print(stack_ordered) # Should give you True

# test4 = TextbookStack(initial_order=[2, 0, 1], initial_orientations=[1, 0, 1])
# output4 = depth_first_search(test4)
# print(output4)  # e.g. [2, 3] (may vary depending on BFS/DFS order)
# print(apply_sequence(test4, output4).check_ordered())  # True

# test5 = TextbookStack(initial_order=[1, 3, 0, 2], initial_orientations=[0, 1, 0, 1])
# output5 = depth_first_search(test5)
# print(output5)  # sequence of flips, may vary
# print(apply_sequence(test5, output5).check_ordered())  # True