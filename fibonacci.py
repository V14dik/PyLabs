import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
logger = logging.getLogger(__name__)

M = {0: 0, 1: 1}
n = 0


def fib(n):
    if n in M:
        return M[n]
    M[n] = fib(n - 1) + fib(n - 2)
    return M[n]


def main():
    while type:
        n = input("ведите номер числа Фибоначи:")
        try:
            n = int(n)
        except ValueError:
            logging.warning("Введите число")
        else:
            break
    fib(n)
    logging.warning(M[n - 1])


if __name__ == "__main__":
    main()
