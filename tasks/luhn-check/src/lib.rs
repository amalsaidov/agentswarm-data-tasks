//! Luhn checksum validation for a string of ASCII digits and spaces.

/// Validate `input` with the Luhn checksum.
///
/// The input may contain only ASCII digits `0`-`9` and ASCII spaces
/// (`U+0020`); spaces are ignored anywhere. Any other character (letters,
/// punctuation, tabs, newlines, non-breaking spaces, non-ASCII digits) makes
/// the result `false`. After removing spaces, fewer than two digits is
/// `false`. Otherwise the Luhn checksum is applied from the rightmost digit:
/// every second digit (second-from-right, fourth-from-right, ...) is doubled,
/// subtracting 9 when the doubled value exceeds 9; the function returns `true`
/// exactly when the digit sum is divisible by 10. Any length works without
/// panic or overflow.
pub fn luhn_valid(input: &str) -> bool {
    let mut digits: Vec<u32> = Vec::new();
    for ch in input.chars() {
        match ch {
            ' ' => continue,
            '0'..='9' => digits.push(ch as u32 - '0' as u32),
            _ => return false,
        }
    }
    if digits.len() < 2 {
        return false;
    }
    let mut sum: u64 = 0;
    for (index, &digit) in digits.iter().rev().enumerate() {
        let mut value = digit;
        if index % 2 == 1 {
            value *= 2;
            if value > 9 {
                value -= 9;
            }
        }
        sum += u64::from(value);
    }
    sum % 10 == 0
}
