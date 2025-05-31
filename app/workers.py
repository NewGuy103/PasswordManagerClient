from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, QThread, Signal

_refs: list[tuple['WorkerThread', QThread]] = []


class WorkerThread(QObject):
    dataReady = Signal(object)
    excReceived = Signal(Exception)

    def __init__(self, func: Callable[[], Any]):
        super().__init__()
        self.func = func
    
    def run(self):
        try:
            result = self.func()
            self.dataReady.emit(result)
        except Exception as exc:
            self.excReceived.emit(exc)


def make_worker_thread(
    func: Callable[[], Any], 
    data_func: Callable[[object], Any], 
    exc_callback: Callable[[Exception], Any]
) -> tuple[WorkerThread, QThread]:
    worker = WorkerThread(func)
    thread = QThread()
    
    worker.moveToThread(thread)
    
    worker.dataReady.connect(data_func)
    worker.excReceived.connect(exc_callback)
    
    thread.started.connect(worker.run)
    worker.dataReady.connect(thread.quit)

    worker.excReceived.connect(thread.quit)
    thread.start()

    refs = (worker, thread)
    _refs.append(refs)

    return refs
