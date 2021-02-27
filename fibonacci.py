import logging
import sys


logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
logger = logging.getLogger(__name__)



def fib(n):
    if n==1: return 0
    if n == 2: return 1
    return fib(n - 1) + fib(n - 2)



def main():
    while type:
        n = input("ведите номер числа Фибоначи:")
        try:
            n = int(n)
        except ValueError:
            logging.warning("Введите число")
        else:
            break
    logging.info(fib(n))


if __name__ == "__main__":
    main()
