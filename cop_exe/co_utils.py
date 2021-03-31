def execute(func, *args, **kwargs):
    def wrapper():
        global_vars.allow_typing = False
        yield from func(*args, **kwargs)
        global_vars.text_box.print('>', end='')
        global_vars.text_box.reset_skipped()
        global_vars.allow_typing = True
    global_vars.coroutines.append(wrapper())


def co_sleep(time: float):
    already = 0
    while already < time:
        yield
        already += global_vars.delta


from cop_exe import global_vars
