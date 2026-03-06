import re
pattern = r"ab*"
test_strings = ["a", "ab", "abb", "b", "ba", "aa"]
for s in test_strings:
    if re.fullmatch(pattern, s):
        print(f"'{s}' matches")
    else:
        print(f"'{s}' does not match")


#------------------------------------------------------------------------------
import re
pattern = r"ab{2,3}"
test_strings = ["a", "ab", "abb", "abbb", "abbbb", "aa"]
for s in test_strings:
    if re.fullmatch(pattern, s):
        print(f"'{s}' matches")
    else:
        print(f"'{s}' does not match")


#------------------------------------------------------------------------------
pattern = r"[a-z]+_[a-z]+"
text = "hello_world test_case example_test not_this One_two"
matches = re.findall(pattern, text)
print(matches)


#-----------------------------------------------------------------------------
pattern = r"[A-Z][a-z]+"

text = "Hello World This is An Example Test"
matches = re.findall(pattern, text)
print(matches)


#-----------------------------------------------------------------------------
pattern = r"a.*b"
test_strings = ["ab", "acb", "a123b", "a_b", "a", "b"]
for s in test_strings:
    if re.fullmatch(pattern, s):
        print(f"'{s}' matches")


#-----------------------------------------------------------------------------
text = "Hello, world. This is a test."
new_text = re.sub(r"[ ,\.]", ":", text)
print(new_text)


#-----------------------------------------------------------------------------
def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

print(snake_to_camel("hello_world_example"))


#-----------------------------------------------------------------------------
text = "HelloWorldThisIsTest"
parts = re.findall(r'[A-Z][a-z]*', text)
print(parts)


#-----------------------------------------------------------------------------
text = "HelloWorldThisIsTest"
spaced = re.sub(r'([A-Z])', r' \1', text).strip()
print(spaced)


#-----------------------------------------------------------------------------
text = "HelloWorldThisIsTest"
snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
print(snake_case)