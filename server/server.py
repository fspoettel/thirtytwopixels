from panel import Panel
from socket_binding import SocketBinding
from spotify_binding import SpotifyBinding
from home_assistant_binding import HomeAssistantBinding
from matrix_factory import matrix_factory

matrix = matrix_factory(32)
panel = Panel(matrix)

provider = SocketBinding(panel)
#provider = SpotifyBinding(panel)
#provider = HomeAssistantBinding(panel)
