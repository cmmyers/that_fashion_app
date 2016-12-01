def mse(tester, trainer):
    mses = {}
    for i, row in enumerate(trainer):
        mse = sum([(tester-row)**2])
        mses['i'] = mse
    return mses
