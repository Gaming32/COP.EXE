from cop_exe import global_vars


def co_sleep(time: float):
    already = 0
    while already < time:
        yield
        already += global_vars.delta
