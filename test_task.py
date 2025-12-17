import unittest
import numpy as np

from task import Task


class TestTask(unittest.TestCase):
    def test_solve_linear_system(self):
        task = Task()
        task.work()

        # Vérifie que A @ x ≈ b
        Ax = task.a @ task.x
        np.testing.assert_allclose(Ax, task.b)

    def test_serialization_deserialization(self):
        a = Task()
        a.work()

        txt = a.to_json()
        b = Task.from_json(txt)

        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
