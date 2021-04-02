def run_function(func, *args, **kwargs):
    global_vars.allow_typing = False
    res = func(*args, **kwargs)
    global_vars.text_box.print('>', end='')
    global_vars.text_box.reset_skipped()
    global_vars.allow_typing = True
    return res


from cop_exe import global_vars
