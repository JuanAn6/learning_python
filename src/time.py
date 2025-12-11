import time
import sys

# Timestamp actual (segundos desde 1970)
now = int(time.time())

# Máximo valor posible de un int de 32 bits
max_int = 2147483647

# Diferencia entre el máximo valor y el tiempo actual
diff = max_int - now

# Conversiones de tiempo
years = diff / (60 * 60 * 24 * 365.25)
days = diff / (60 * 60 * 24)
months = years * 12

print()
print(f".....Current timestamp : {now}")
print(f".....Max int:            {max_int}")
print(f".....Difference:         {diff} seconds")
print(f".....Approximate:        {years:.2f} years")
print(f".....Approximate:        {days:.2f} days")
print(f".....Approximate:        {months:.2f} months")
