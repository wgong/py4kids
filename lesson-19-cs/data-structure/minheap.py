"""

MinHeap implementation from scratch in Python

Educational purposes: 
Understand heap operations without using built-in libraries like `heapq`

see https://claude.ai/chat/fd741cd4-35fb-41dc-852b-c32975bd7d74


By default, Python’s heapq implements a min-heap. To create a max-heap, you can simply invert the values (store negative numbers).

Example: Below example, convert a list into a max-heap by storing negative numbers and then retrieve the largest element:

```python
import heapq  
nums = [10, 20, 15, 30, 40]  

# Convert into a max-heap by inverting values  
max_heap = [-n for n in nums]  
heapq.heapify(max_heap)  

# Access largest element (invert sign again)  
print("Largest element:", -max_heap[0])

Output:
Largest element: 40

see more examples at https://www.geeksforgeeks.org/python/heap-queue-or-heapq-in-python/

"""




class MinHeap:
    def __init__(self, initial_list=None, allow_duplicates=True):
        """
        Initialize MinHeap with optional initial list and duplicate policy
        
        Args:
            initial_list: List to convert into heap
            allow_duplicates: If False, prevents duplicate elements
        """
        self.allow_duplicates = allow_duplicates
        self.heap = []
        self.elements_set = set() if not allow_duplicates else None
        
        if initial_list is not None:
            if not allow_duplicates:
                # Remove duplicates while preserving order
                seen = set()
                unique_items = []
                for item in initial_list:
                    if item not in seen:
                        unique_items.append(item)
                        seen.add(item)
                self.heap = unique_items
                self.elements_set = seen.copy()
            else:
                self.heap = initial_list.copy()
            
            self.heapify()
    
    def _parent_index(self, i):
        """Get parent index"""
        return (i - 1) // 2
    
    def _left_child_index(self, i):
        """Get left child index"""
        return 2 * i + 1
    
    def _right_child_index(self, i):
        """Get right child index"""
        return 2 * i + 2
    
    def _has_parent(self, i):
        """Check if node has parent"""
        return self._parent_index(i) >= 0
    
    def _has_left_child(self, i):
        """Check if node has left child"""
        return self._left_child_index(i) < len(self.heap)
    
    def _has_right_child(self, i):
        """Check if node has right child"""
        return self._right_child_index(i) < len(self.heap)
    
    def _parent(self, i):
        """Get parent value"""
        return self.heap[self._parent_index(i)]
    
    def _left_child(self, i):
        """Get left child value"""
        return self.heap[self._left_child_index(i)]
    
    def _right_child(self, i):
        """Get right child value"""
        return self.heap[self._right_child_index(i)]
    
    def _swap(self, i, j):
        """Swap elements at indices i and j"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def _bubble_up(self, index):
        """
        Bubble up element at index to maintain heap property
        Used after insertion
        """
        while (self._has_parent(index) and 
               self._parent(index) > self.heap[index]):
            parent_idx = self._parent_index(index)
            self._swap(index, parent_idx)
            index = parent_idx
    
    def _bubble_down(self, index):
        """
        Bubble down element at index to maintain heap property
        Used after extraction
        """
        while self._has_left_child(index):
            # Find smallest child
            smaller_child_idx = self._left_child_index(index)
            
            if (self._has_right_child(index) and 
                self._right_child(index) < self._left_child(index)):
                smaller_child_idx = self._right_child_index(index)
            
            # If current element is smaller than smallest child, we're done
            if self.heap[index] < self.heap[smaller_child_idx]:
                break
            
            # Otherwise, swap with smaller child and continue
            self._swap(index, smaller_child_idx)
            index = smaller_child_idx
    
    def heapify(self):
        """
        Convert current list into a valid min-heap from scratch
        Uses bottom-up approach - start from last non-leaf node
        Time complexity: O(n)
        """
        if len(self.heap) <= 1:
            return
        
        # Start from last non-leaf node and bubble down
        start_idx = self._parent_index(len(self.heap) - 1)
        
        for i in range(start_idx, -1, -1):
            self._bubble_down(i)
        
        print(f"Heapified: {self.heap}")
    
    def push(self, val):
        """
        Add element to heap (manual implementation of heappush)
        Time complexity: O(log n)
        """
        # Check for duplicates if not allowed
        if not self.allow_duplicates:
            if val in self.elements_set:
                print(f"Duplicate {val} not allowed!")
                return False
            self.elements_set.add(val)
        
        # Add to end of heap
        self.heap.append(val)
        
        # Bubble up to maintain heap property
        self._bubble_up(len(self.heap) - 1)
        
        print(f"Pushed {val}: {self.heap}")
        return True
    
    def pop(self):
        """
        Remove and return smallest element (manual implementation of heappop)
        Time complexity: O(log n)
        """
        if len(self.heap) == 0:
            print("Cannot pop from empty heap")
            return None
        
        if len(self.heap) == 1:
            val = self.heap.pop()
            if not self.allow_duplicates:
                self.elements_set.remove(val)
            print(f"Popped {val}: {self.heap}")
            return val
        
        # Store min value
        min_val = self.heap[0]
        
        # Move last element to root
        self.heap[0] = self.heap.pop()
        
        # Update set if needed
        if not self.allow_duplicates:
            self.elements_set.remove(min_val)
        
        # Bubble down to maintain heap property
        self._bubble_down(0)
        
        print(f"Popped {min_val}: {self.heap}")
        return min_val
    
    def peek(self):
        """
        Access smallest element without removing it
        Time complexity: O(1)
        """
        if len(self.heap) == 0:
            return None
        return self.heap[0]
    
    def heappushpop(self, val):
        """
        Push new element and pop smallest in single step (manual implementation)
        More efficient than separate push() and pop()
        Time complexity: O(log n)
        """
        # Check for duplicates if not allowed
        if not self.allow_duplicates and val in self.elements_set:
            print(f"Duplicate {val} detected in pushpop, only popping")
            return self.pop()
        
        if len(self.heap) == 0:
            if not self.allow_duplicates:
                self.elements_set.add(val)
            print(f"Empty heap, pushpop just returns {val}")
            return val
        
        # If new value is smaller than root, just return it
        if val < self.heap[0]:
            print(f"Pushpop {val} (immediately returned as it's smallest): {self.heap}")
            return val
        
        # Otherwise, replace root with new value and bubble down
        result = self.heap[0]
        self.heap[0] = val
        
        # Update set if needed
        if not self.allow_duplicates:
            self.elements_set.remove(result)
            self.elements_set.add(val)
        
        self._bubble_down(0)
        
        print(f"Pushpop {val} (returned {result}): {self.heap}")
        return result
    
    def heapreplace(self, val):
        """
        Pop smallest and push new element in one step (manual implementation)
        More efficient than separate pop() and push()
        Time complexity: O(log n)
        """
        if len(self.heap) == 0:
            if not self.allow_duplicates:
                if val in self.elements_set:
                    print(f"Cannot replace in empty heap with duplicate {val}")
                    return None
                self.elements_set.add(val)
            self.heap.append(val)
            print(f"Empty heap, replace just adds {val}")
            return None
        
        # Check for duplicates if not allowed
        if not self.allow_duplicates and val in self.elements_set:
            print(f"Duplicate {val} detected in replace, operation cancelled")
            return None
        
        # Replace root with new value
        result = self.heap[0]
        self.heap[0] = val
        
        # Update set if needed
        if not self.allow_duplicates:
            self.elements_set.remove(result)
            self.elements_set.add(val)
        
        # Bubble down to maintain heap property
        self._bubble_down(0)
        
        print(f"Replace {result} with {val}: {self.heap}")
        return result
    
    def size(self):
        """Return number of elements in heap"""
        return len(self.heap)
    
    def is_empty(self):
        """Check if heap is empty"""
        return len(self.heap) == 0
    
    def contains(self, val):
        """
        Check if element exists in heap
        O(1) if duplicates not allowed, O(n) otherwise
        """
        if not self.allow_duplicates:
            return val in self.elements_set
        return val in self.heap
    
    def get_heap_list(self):
        """Return copy of heap array"""
        return self.heap.copy()
    
    def clear(self):
        """Clear all elements from heap"""
        self.heap.clear()
        if not self.allow_duplicates:
            self.elements_set.clear()
    
    def show_tree(self, sep="#"):
        """
        Visualize this heap as a complete binary tree
        
        Args:
            sep: Separator between left and right children (default: "#")
        """
        self.show_heap_as_complete_binary_tree(self.heap, sep)
    
    @staticmethod
    def show_heap_as_complete_binary_tree(heap, sep="#"):
        """
        Static method to visualize any heap array as a complete binary tree
        Can be called on any list/array representing a heap
        
        Usage:
            MinHeap.show_heap_as_complete_binary_tree([1, 3, 2, 4, 5, 6])
            # or
            my_heap.show_tree()
        """
        import math

        if not heap:
            print("Empty heap")
            return
        
        n = len(heap)
        height = int(math.log2(n)) + 1 if n > 0 else 0
        
        print(f"\nHeap as Complete Binary Tree (size={n}, height={height}):")
        print("=" * 50)
        
        level = 0
        index = 0
        
        while index < n:
            nodes_in_level = min(2**level, n - index)
            spaces_before = " " * (4 * (2**(height - level - 1) - 1))
            spaces_between = " " * (4 * (2**(height - level) - 1))
            
            print(spaces_before, end="")
            for i in range(nodes_in_level):
                if i > 0:
                    # Add separator between siblings (left and right children of same parent)
                    if i % 2 == 1:  # Right child (odd index in level)
                        print(f"   {sep} ", end="")
                    else:  # Left child of different parent
                        print(spaces_between, end="")
                print(f"{heap[index + i]:3}", end="")
            print()
            
            index += nodes_in_level
            level += 1
        
        print(f"\nArray representation: {heap}")




def demonstrate_heap_operations(allow_duplicates=True):
    """Demonstrate all heap operations implemented from scratch"""
    print("=== MinHeap Implementation From Scratch ===\n")
    
    # Test with duplicates allowed
    print("--- Testing with duplicates allowed ---")
    initial_data = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7, 3, 1]
    print(f"Initial data: {initial_data}")
    
    heap1 = MinHeap(initial_data, allow_duplicates=allow_duplicates)
    heap1.show_tree()
    
    print(f"\nPeek: {heap1.peek()}")
    
    # Test push
    heap1.push(0)
    heap1.show_tree()
    
    # Test pop
    print(f"\nPopping 3 elements:")
    for _ in range(3):
        heap1.pop()
    heap1.show_tree()
    
    # Test heappushpop
    print(f"\nTesting heappushpop(5):")
    result = heap1.heappushpop(5)
    heap1.show_tree()
    
    # Test heapreplace
    print(f"\nTesting heapreplace(12):")
    result = heap1.heapreplace(12)
    heap1.show_tree()
    
    # Test with duplicates NOT allowed
    print(f"\n{'='*60}")
    print("--- Testing with duplicates NOT allowed ---")
    
    heap2 = MinHeap(initial_data, allow_duplicates=False)
    heap2.show_tree()
    
    print(f"\nTrying to push duplicate:")
    heap2.push(3)  # Should fail
    
    print(f"\nTrying to push new element:")
    heap2.push(0)  # Should succeed
    heap2.show_tree()
    
    print(f"\nTesting heappushpop with duplicate:")
    result = heap2.heappushpop(1)  # 1 already exists
    
    print(f"\nTesting heapreplace with duplicate:")
    result = heap2.heapreplace(2)  # 2 already exists


def demonstrate_heapify_process(allow_duplicates=True):
    """Show step-by-step heapify process"""
    print(f"\n{'='*60}")
    print("=== Understanding Heapify Process ===\n")
    
    data = [9, 5, 6, 2, 3, 7, 1, 4, 8]
    print(f"Original array: {data}")
    
    # Show the tree before heapify
    print(f"\nBefore heapify (not a valid heap):")
    MinHeap.show_heap_as_complete_binary_tree(data, sep="<>")
    
    # Manual step-by-step heapify explanation
    print(f"\nHeapify process:")
    print(f"1. Start from last non-leaf node (index {(len(data)-1-1)//2})")
    print(f"2. For each node, bubble down to maintain min-heap property")
    print(f"3. Continue until we reach the root")
    
    heap = MinHeap(data, allow_duplicates)
    print(f"\nAfter heapify (using different separator):")
    heap.show_tree(sep="||")
    
    print(f"\nTime complexity analysis:")
    print(f"- Heapify: O(n) - more efficient than n insertions")
    print(f"- Individual operations: O(log n)")
    print(f"- Space complexity: O(1) additional space")


    
def print_summary():
    print(f"\n{'='*60}")
    print("=== Educational Summary ===")
    print("Key concepts implemented from scratch:")
    print("1. Heapify: Bottom-up approach, O(n) time")
    print("2. Push: Add to end, bubble up, O(log n) time")
    print("3. Pop: Replace root with last, bubble down, O(log n) time")
    print("4. Peek: Direct access to root, O(1) time")
    print("5. Pushpop: Optimized push+pop, O(log n) time")
    print("6. Replace: Optimized pop+push, O(log n) time")
    print("7. Duplicate handling: Optional O(1) detection with set")
    

if __name__ == "__main__":
    allow_duplicates=False

    demonstrate_heap_operations(allow_duplicates)
    demonstrate_heapify_process(allow_duplicates)
    
    print_summary()