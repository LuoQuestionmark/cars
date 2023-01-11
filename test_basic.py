from storage import Storage

if __name__ == '__main__':
    s = Storage(width=7, height=3)
    s.add(3, 1)
    f, args = s.available_options().pop()

    print(s)

    f(*args)

    print(s)