from lb_dev.commands.copyright.check_for_license_file.check_for_license import check_for_license

def main():
    result = check_for_license('.')
    exit(result)

if __name__ == "__main__":
    main()
    