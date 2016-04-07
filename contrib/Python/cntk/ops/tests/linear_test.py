# Copyright (c) Microsoft. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root 
# for full license information.
# ==============================================================================

"""
Unit tests for linear algebra operations, each operation is tested for 
the forward and the backward pass
"""

import numpy as np
import pytest
from .ops_test_utils import test_helper, C, AA, I, cpu_gpu
from ...graph import *
from ...reader import *
import numpy as np

# Testing inputs
@pytest.mark.parametrize("left_operand, right_operand", [
    ([30], [10]),
    ([[30]], [[10]]),
    ([[1.5,2.1]], [[10,20]]),
    #TODO: enable once all branches are merged to master
    #([5], [[30,40], [1,2]]),
    #Adding two 3x2 inputs of sequence length 1
    #([[30,40], [1,2], [0.1, 0.2]], [[10,20], [3,4], [-0.5, -0.4]]),     
    ])
def test_op_add(left_operand, right_operand, cpu_gpu):    

    #Forward pass test
    
    #we compute the expected output for the forward pass
    # we need two surrounding brackets
    # the first for sequence of 1 element, since we have has_sequence_dimension=False
    # the second for batch of one sample
    expected = [[AA(left_operand) + AA(right_operand)]]

    a = I([left_operand], has_sequence_dimension=False)
    b = I([right_operand], has_sequence_dimension=False)    
    
    left_as_input = a + right_operand    
    test_helper(left_as_input, expected, cpu_gpu, False)
    
    right_as_input = left_operand + b
    test_helper(right_as_input, expected, cpu_gpu, False)
    
    #Backward pass test
    
    #the expected results for the backward pass is all ones
    expected = [[[np.ones_like(x) for x in left_operand]]]
    test_helper(left_as_input, expected, cpu_gpu, clean_up=True, backward_pass = True, input_node = a)    
    test_helper(right_as_input, expected, cpu_gpu, clean_up=True, backward_pass = True, input_node = b)