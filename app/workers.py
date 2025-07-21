from collections.abc import Callable
from functools import partial
from typing import Any

from PySide6.QtCore import QObject, QThread, Signal

_refs: list[tuple["WorkerThread", QThread]] = []
_t_count: int = 1


class WorkerThread(QObject):
    dataReady = Signal(object)
    excReceived = Signal(Exception)
    runFinished = Signal()

    def __init__(self, func: Callable[[], Any]):
        super().__init__()
        self.func = func

    def run(self):
        try:
            result = self.func()
            self.dataReady.emit(result)
        except Exception as exc:
            self.excReceived.emit(exc)
        finally:
            self.runFinished.emit()


def _get_func_name(func: Callable | None) -> str | None:
    if func is None:
        return None

    if isinstance(func, partial):
        func_name = func.func.__name__
    else:
        try:
            func_name = func.__name__
        except AttributeError:
            func_name = str(func)

    return func_name


def make_worker_thread(
    func: Callable[[], Any],
    data_func: Callable[[object], Any] | None = None,
    exc_callback: Callable[[Exception], Any] | None = None,
) -> tuple[WorkerThread, QThread]:
    global _t_count

    worker = WorkerThread(func)
    thread = QThread()

    worker.moveToThread(thread)

    if data_func is not None:
        worker.dataReady.connect(data_func)

    if exc_callback is not None:
        worker.excReceived.connect(exc_callback)

    thread.started.connect(worker.run)
    worker.runFinished.connect(thread.quit)

    func_name = _get_func_name(func)

    thread.setObjectName(f"thread-{_t_count}:func[{func_name}]")
    thread.start()

    refs = (worker, thread)
    _refs.append(refs)

    _t_count += 1
    return refs
