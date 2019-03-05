import sys, getopt
from server_balancing import ServerBalancing


def usage():
    help_text = """ 
    Help usage
    Parameter: 
        --file to file input. Is required
        --output to file output. Default is output.txt 
        --ttask default is 5
        --umax default is 10
    """

    print(help_text)


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hfotu", ["help", "file=", "output=", "ttask=", "umax="]
        )
        print("opts", opts)
    except getopt.GetoptError as e:
        print(str(e))
    file_input = None
    file_output = "output.txt"
    ttaks = 5
    umax = 10

    for o, a in opts:

        if o in ("-f", "--file"):
            print(a)
            file_input = a
        elif o in ("-o", "--output"):
            file_output = a
        elif o in ("-t", "--ttask"):
            ttaks = a
        elif o in ("-u", "--umax"):
            umax = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            raise BaseException(f"Invalid parameter {o}")
    if not isinstance(file_input, str):
        raise BaseException("File input is required")

    server_balancing = ServerBalancing(
        ttask=ttaks, umax=umax, output_file_path=file_output
    )
    server_balancing.execute(file_input)


if __name__ == "__main__":
    main()
