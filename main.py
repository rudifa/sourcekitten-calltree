#! python3


# if __name__ == '__main__':
#     import argparse
#     import sys

#     parser = argparse.ArgumentParser()
#     parser.add_argument('--file', help='file path to read')
#     args = parser.parse_args()

#     if args.file:
#         with open(args.file, 'r') as f:
#             input_text = f.read().splitlines()
#     else:
#         sys.stderr.write("expecting input on stdin...\n")
#         input_text = input().splitlines()

#     # now you can process input_text as an array
#     print(input_text)

import sys
import argparse
import select

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='input file path to read')
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as f:
            input_text = f.read()
    else:
        timeout = 1
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if ready:
            input_text = sys.stdin.read()
        else:
            sys.stderr.write(
                """No input received within 1 second.
Please pipe the input to sdtdin or use the `--file <inputfile>` option.
\n""")
            sys.exit()

    # now you can process input_text as an array
    print(len(input_text))
    print(input_text)
