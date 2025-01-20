def character_distribution(input_string):
    char_count = {}
    for char in input_string:
        if char.isalpha():
            char = char.lower()
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1
    return char_count

def test_general_case():
  assert character_distribution('Hello, World!') == {'h': 1, 'e': 1, 'l': 3, 'o': 2, 'w': 1, 'r': 1, 'd': 1}

# Test case 2: Empty string (Edge case)
def test_empty_string():
  assert character_distribution('') == {}

# Test case 3: String with no alphabetic characters (Edge case)
def test_no_alphabetic_characters():
  assert character_distribution('12345!@#$%') == {}

# Test case 4: String with all identical alphabetic characters (Edge case)
def test_identical_characters():
  assert character_distribution('aaaaaa') == {'a': 6}

# Test case 5: String with mixed letters and numbers (Logical case)
def test_mixed_letters_numbers():
  assert character_distribution('a1b2c3d4e5f6g7h8i9j0') == {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1, 'i': 1, 'j': 1}

# Test case 6: String with mixed case letters (Logical case)
def test_mixed_case():
  assert character_distribution('AaBbCcDdEe') == {'a': 2, 'b': 2, 'c': 2, 'd': 2, 'e': 2}

# Test case 7: Large input with repetitive pattern (Performance case)
def test_large_input():
    large_input = 'abcde' * 1000
    expected_output = {'a': 1000, 'b': 1000, 'c': 1000, 'd': 1000, 'e': 1000}
    assert character_distribution(large_input) == expected_output

# Test 8: Testing Unicode characters
def test_unicode_characters():
    assert character_distribution('ñÑäÄ') == {'ñ': 2, 'ä': 2}

# Test 9: Whitespace and random punctuation and special characters
def test_whitespace_and_punctuation():
    assert character_distribution(' a !!%#$a a . ') == {'a': 3}
    
if __name__ == "__main__":
    try:
        test_general_case()
        test_empty_string()
        test_no_alphabetic_characters()
        test_identical_characters()
        test_mixed_letters_numbers()
        test_mixed_case()
        test_large_input()
        test_unicode_characters()
        test_whitespace_and_punctuation()
        
        print("All tests passed!")
    except AssertionError as e:
        print("A test failed.")
        