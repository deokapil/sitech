import datetime
import time


def generate_id_by_timestamp() -> str:
    """This function generates timestamp based id to be used as common id across the run of monitor
        :return: string common id for particular run.
    """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime("%m-%d-%Y-%H-%M-%S")
    identity = f"sit-{st}"
    return identity
