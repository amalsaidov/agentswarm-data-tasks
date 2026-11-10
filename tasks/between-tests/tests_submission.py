"""Behavioral tests for ``is_between(value, lower, upper)``.

The contract (see ``SPEC.md``): ``is_between`` is an inclusive integer range
check. It accepts exactly three built-in ``int`` arguments and returns the
exact ``bool`` ``True`` when ``lower <= value <= upper`` and ``False``
otherwise. Bounds are inclusive and equal bounds are valid. If any argument is
not an exact ``int`` (``bool``, ``int`` subclasses, ``float``, ``str``,
``None`` and containers all count as invalid) a ``TypeError`` is raised, and
this type check happens before the bounds are compared. If ``lower > upper`` a
``ValueError`` is raised.

Every test asserts public behavior only; none inspects the implementation
source or tries to identify a particular faulty variant.
"""

import unittest

from implementation import is_between


class ReturnValueTests(unittest.TestCase):
    """Values strictly inside, on, and outside the range."""

    def test_value_strictly_inside_range_is_true(self):
        self.assertIs(is_between(3, 1, 5), True)

    def test_value_below_range_is_false(self):
        self.assertIs(is_between(0, 1, 5), False)

    def test_value_above_range_is_false(self):
        self.assertIs(is_between(6, 1, 5), False)


class InclusiveBoundaryTests(unittest.TestCase):
    """Both endpoints are part of the range, and equal bounds are valid."""

    def test_lower_bound_is_inclusive(self):
        self.assertIs(is_between(1, 1, 5), True)

    def test_upper_bound_is_inclusive(self):
        self.assertIs(is_between(5, 1, 5), True)

    def test_equal_bounds_accept_the_single_value(self):
        self.assertIs(is_between(2, 2, 2), True)

    def test_equal_bounds_reject_other_values(self):
        self.assertIs(is_between(3, 2, 2), False)


class ResultTypeTests(unittest.TestCase):
    """The result must be an exact ``bool``, not an ``int`` or other truthy
    value."""

    def test_true_result_is_exact_bool(self):
        result = is_between(3, 1, 5)
        self.assertIs(result, True)
        self.assertIs(type(result), bool)

    def test_false_result_is_exact_bool(self):
        result = is_between(9, 1, 5)
        self.assertIs(result, False)
        self.assertIs(type(result), bool)


class ReversedBoundsTests(unittest.TestCase):
    """``lower > upper`` is an error; equal bounds are not."""

    def test_reversed_bounds_raise_value_error(self):
        with self.assertRaises(ValueError):
            is_between(3, 5, 2)

    def test_reversed_bounds_raise_even_when_value_would_be_in_order(self):
        with self.assertRaises(ValueError):
            is_between(4, 5, 2)


class InvalidTypeTests(unittest.TestCase):
    """Non-``int`` arguments raise ``TypeError``; ``bool`` is not an ``int``
    here."""

    def test_bool_value_raises_type_error(self):
        with self.assertRaises(TypeError):
            is_between(True, 0, 5)

    def test_bool_bound_raises_type_error(self):
        with self.assertRaises(TypeError):
            is_between(1, False, 5)

    def test_float_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            is_between(2.0, 1, 5)

    def test_non_numeric_arguments_raise_type_error(self):
        for args in (("3", 1, 5), (3, None, 5), (3, 1, [5])):
            with self.subTest(args=args):
                with self.assertRaises(TypeError):
                    is_between(*args)

    def test_type_is_checked_before_bounds(self):
        # Bounds are reversed *and* an argument has the wrong type: the type
        # error must win, per the contract.
        with self.assertRaises(TypeError):
            is_between(None, 5, 2)


class LargeIntegerTests(unittest.TestCase):
    """Arbitrary-precision integers are supported."""

    def test_arbitrary_precision_integers(self):
        big = 10 ** 50
        self.assertIs(is_between(big, 0, big), True)
        self.assertIs(is_between(big + 1, 0, big), False)


if __name__ == "__main__":
    unittest.main()
