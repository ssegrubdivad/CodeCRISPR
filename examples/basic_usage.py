"""
Basic usage example for CodeCRISPR
"""

import os
from CodeCRISPR import CodeCRISPR

# Create a sample file
sample_code = '''
def hello_world():
    """Say hello"""
    print("Hello, World!")

def calculate_sum(a, b):
    """Calculate sum of two numbers"""
    return a + b

def main():
    """Main function"""
    hello_world()
    result = calculate_sum(5, 3)
    print(f"Sum: {result}")
'''

# Write sample file
with open('example.py', 'w') as f:
    f.write(sample_code)

# Use CodeCRISPR to inspect and modify
editor = CodeCRISPR('example.py')

# Inspect the file
print("Functions found:")
for name, info in editor.reference_map.items():
    print(f"  {name}: lines {info['start']}-{info['end']}")

# Modify the hello_world function
new_code = '''def hello_world():
    """Say hello with style"""
    print("Hello CodeCRISPR World!")'''

editor.replace_method('hello_world', new_code)
editor.save()

print("\nFunction updated successfully!")
