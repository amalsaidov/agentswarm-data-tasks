"""Behavioral tests for ``is_leap_year(year)``.

The contract (see ``SPEC.md``): ``is_leap_year`` is a Gregorian leap-year
check. ``year`` must have the exact built-in ``int`` type; ``bool``, ``int``
subclasses, ``float``, ``str``, ``None`` and containers all raise
``TypeError``, and this type check happens *before* the range check. A year
below 1 (``0`` and negatives) raises ``ValueError``. Otherwise the function
returns the exact ``bool`` ``True`` when the year is a Gregorian leap year
(divisible by 4, except century years, which are leap only when divisible by
400) and ``False`` otherwise.

Every test asserts public behavior only; none inspects the implementation
source or tries to identify a particular faulty variant.
"""

import unittest

from implementation import is_leap_year


class LeapYearResultTests(unittest.TestCase):
    """Ordinary leap and common years."""

    def test_year_divisible_by_four_is_leap(self):
        self.assertIs(is_leap_year(2024), True)
        self.assertIs(is_leap_year(4), True)

    def test_year_not_divisible_by_four_is_common(self):
        self.assertIs(is_leap_year(2023), False)

    def test_year_one_is_common(self):
        # 1 is in range (>= 1) and not divisible by 4, so it is a common year.
        self.assertIs(is_leap_year(1), False)


class CenturyRuleTests(unittest.TestCase):
    """Century years are leap only when divisible by 400."""

    def test_century_not_divisible_by_400_is_common(self):
        self.assertIs(is_leap_year(1900), False)
        self.assertIs(is_leap_year(2100), False)

    def test_century_divisible_by_400_is_leap(self):
        self.assertIs(is_leap_year(2000), True)
        self.assertIs(is_leap_year(1600), True)


class ResultTypeTests(unittest.TestCase):
    """The result must be an exact ``bool``, not an ``int`` or other value."""

    def test_true_result_is_exact_bool(self):
        result = is_leap_year(2024)
        self.assertIs(result, True)
        self.assertIs(type(result), bool)

    def test_false_result_is_exact_bool(self):
        result = is_leap_year(2023)
        self.assertIs(result, False)
        self.assertIs(type(result), bool)


class RangeTests(unittest.TestCase):
    """Years below 1 raise ``ValueError``."""

    def test_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            is_leap_year(0)

    def test_negative_year_raises_value_error(self):
        for year in (-1, -4, -400):
            with self.subTest(year=year):
                with self.assertRaises(ValueError):
                    is_leap_year(year)


class InvalidTypeTests(unittest.TestCase):
    """Non-``int`` arguments raise ``TypeError``; ``bool`` is not accepted."""

    def test_bool_raises_type_error(self):
        # bool is an int subclass but is rejected by the exact-type contract.
        for year in (True, False):
            with self.subTest(year=year):
                with self.assertRaises(TypeError):
                    is_leap_year(year)

    def test_float_raises_type_error(self):
        # A whole-valued float is still the wrong type.
        for year in (2024.0, 2023.0):
            with self.subTest(year=year):
                with self.assertRaises(TypeError):
                    is_leap_year(year)

    def test_other_non_int_types_raise_type_error(self):
        for year in ("2024", None, [2024], 2024j):
            with self.subTest(year=year):
                with self.assertRaises(TypeError):
                    is_leap_year(year)

    def test_type_is_checked_before_range(self):
        # The argument is both the wrong type and out of range: the type error
        # must win, per the contract.
        with self.assertRaises(TypeError):
            is_leap_year(-4.0)


class LargeIntegerTests(unittest.TestCase):
    """Arbitrary-precision integers follow the same rules."""

    def test_large_leap_and_common_years(self):
        self.assertIs(is_leap_year(10 ** 18 + 4), True)
        self.assertIs(is_leap_year(10 ** 18 + 1), False)


if __name__ == "__main__":
    unittest.main()
