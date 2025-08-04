import functools
import time


def run_n_times(n: int):
    def my_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            for i in range(n):
                print(
                    f"Calling {func.__name__}"
                    f"{i+1} time: {func(*args, **kwargs)}")
            end = time.time()
            print(f"Total runtime: {end - start:.2f} sec")
        return wrapper
    return my_decorator


@run_n_times(5)
def my_func(delay: int):
    time.sleep(delay)
    return f"Hello from {my_func.__name__}"


if __name__ == "__main__":
    my_func(1)