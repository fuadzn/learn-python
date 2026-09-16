def make_upper(function):
    def upper():
        f = function()
        print(f"this from origin value: {f}")
        return f.upper()
    return upper

@make_upper
def helloworld():
    return "hello world"

print(helloworld())