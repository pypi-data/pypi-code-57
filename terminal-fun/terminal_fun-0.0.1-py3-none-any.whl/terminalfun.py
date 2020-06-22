def cowsay():
    try:
        import cowsay
        cowsay.cow("Hello World")
        return True
    
    except:
        return False

if __name__ == '__main__':
    cowsay()