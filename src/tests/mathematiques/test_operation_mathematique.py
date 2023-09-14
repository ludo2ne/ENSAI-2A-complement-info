from unittest import TestCase, TextTestRunner, TestLoader

from mathematiques.operation_mathematique import OperationMathematiques


class TestOperationMathematiques(TestCase):
    def test_diviser_cinq_par_nombre_non_nul(self):
        # GIVEN
        nombre = 2

        # WHEN
        resultat = OperationMathematiques().diviser_cinq_par(nombre)

        # THEN
        self.assertEqual(resultat, 2.5)

    def test_diviser_cinq_par_zero(self):
        # GIVEN
        nombre = 0

        # WHEN
        resultat = OperationMathematiques().diviser_cinq_par(nombre)

        # THEN
        self.assertIsNone(resultat)

    def test_diviser_cinq_string(self):
        # GIVEN
        nombre = "a"

        # WHEN / THEN
        with self.assertRaises(TypeError):
            OperationMathematiques().diviser_cinq_par(nombre)


if __name__ == "__main__":
    # Run the tests
    result = TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestOperationMathematiques)
    )
