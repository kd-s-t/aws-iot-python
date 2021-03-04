from time import sleep
import controllers.main as en

n = en.Main()
n.subscribe()

while True:
    sleep(5)
