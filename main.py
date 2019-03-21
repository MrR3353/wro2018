import init
import _thread
import var

l = _thread.allocate_lock()
_thread.start_new_thread(var.eva.run, ())
_thread.start_new_thread(var.rob.run, ())
while not l.locked():
    pass



