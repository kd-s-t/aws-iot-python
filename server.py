from time import sleep
import controllers.Main as en

n = en.Main()
n.subscribe()

while True:
    sleep(5)
