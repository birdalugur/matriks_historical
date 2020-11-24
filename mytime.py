import pandas as pd


def resample(data: pd.DataFrame, rule: str, func: str) -> pd.DataFrame:
    """
    Verileri 1sn, 5sn, 1dk, 30dk... şeklinde yeniden örnekleyin.

    Args:
        data :
        rule :
        func :
    Return:
        New Dataframe
    """
    return data.resample(rule=rule).apply(func)


def convert_timestamp():
    """
    Unix time olarak gelen verileri pandas timestamp'ine dönüştürün
    """
    pass


