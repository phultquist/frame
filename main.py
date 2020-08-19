import importlib

while True:
    try:
        import run
    except Exception as e:
        print(e)
        if e != 'KeyboardInterrupt':
            importlib.reload(run)