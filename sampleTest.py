# Arrange-Act-Assert (AAA) Pattern for testing

def test_calculate_discount_standard_user():
  # Arrange
  user_type = "standard"
  purchase_amount = 100

  # Act
  final_amount = calculate_discount(user_type, purchase_amount)

  # Assert
  expected_amount = 90
  assert final_amount == expected_amount, "Standard users should receive a 10% discount."