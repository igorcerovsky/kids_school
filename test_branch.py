import math
import cmath

r1 = 1.0 / 256.0
r2 = 1.0
log_ratio = math.log(r2 / r1)
numerator = complex(0, 2 * math.pi)
denominator = complex(log_ratio, 2 * math.pi)
beta = numerator / denominator

def w(z, theta):
    r = abs(z)
    log_z = complex(math.log(r), theta)
    return cmath.exp(beta * log_z)

# Let's check w(-1) from top and bottom
print("Top:", w(-1, math.pi))
print("Bottom:", w(-1, -math.pi))
