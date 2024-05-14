import ast

def safe_exec(code_string):
    # (Perform validation and security checks here)
    tree = ast.parse(code_string)  # Parse the code string
    exec(compile(tree, '<string>', 'exec'))  # Compile and execute

user_code = input("Enter your code: ")
safe_exec(user_code)