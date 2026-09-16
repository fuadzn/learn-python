text = """
transaction_id,user\r
1,aaa\r
\r
2,xx\r
3,ccc\r
\r
"""

def process_large_file(text):
    for line in text.split('\r'):
        # Process the line
        processed_line = line.strip().upper()

        if processed_line != "":
            # Yield the processed line
            yield processed_line

# Example usage
for processed_line in process_large_file(text):
    print(processed_line)