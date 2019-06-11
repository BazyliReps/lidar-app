from gpiozero import MCP3008
from time import sleep
import sys
res = MCP3008(0)

for i in range(1000):
    val = res.value
    print(val)
    sleep(0.5)
