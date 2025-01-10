"""Tests for mesh.py."""


from mesh import Mesh


def test_mesh() -> None:
    mesh = Mesh()
    mesh.connect()
    mesh.start_listening()
    mesh.disconnect()
