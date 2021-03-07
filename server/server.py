from panel import Panel
from socket_binding import SocketBinding
from matrix_factory import matrix_factory

matrix = matrix_factory(32)
panel = Panel(matrix)
provider = SocketBinding(panel)
