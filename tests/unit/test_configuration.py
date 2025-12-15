"""
Unit tests for Configuration class.
"""

import pytest
from src.models import Configuration


class TestConfiguration:
    """Test cases for Configuration class."""
    
    def test_create_default_configuration(self):
        """Test creating configuration with default values."""
        config = Configuration()
        
        assert config.annual_goal == 15
        assert config.simultaneous_reading_limit == 3
    
    def test_set_annual_goal(self):
        """Test setting annual reading goal."""
        config = Configuration()
        config.annual_goal = 24
        
        assert config.annual_goal == 24
    
    def test_set_invalid_annual_goal_raises_error(self):
        """Test that negative annual goal raises ValueError."""
        config = Configuration()
        
        with pytest.raises(ValueError, match="Annual target cannot be less than or equal to zero."):
            config.annual_goal = -5
    
    def test_set_simultaneous_reading_limit(self):
        """Test setting simultaneous reading limit."""
        config = Configuration()
        config.simultaneous_reading_limit = 3
        
        assert config.simultaneous_reading_limit == 3
    
    def test_set_invalid_simultaneous_limit_raises_error(self):
        """Test that invalid simultaneous limit raises ValueError."""
        config = Configuration()
        
        with pytest.raises(ValueError, match="simultaneous readings cannot be less than or equal to zero."):
            config.simultaneous_reading_limit = 0
        
        with pytest.raises(ValueError, match="simultaneous readings cannot be less than or equal to zero."):
            config.simultaneous_reading_limit = -1
    
    def test_configuration_to_dict(self):
        """Test configuration serialization."""
        config = Configuration()
        config.annual_goal = 15
        config.simultaneous_reading_limit = 4
        
        data = config._to_dict()
        
        assert data['annual_goal'] == 15
        assert data['simultaneous_reading_limit'] == 4
    
    def test_configuration_from_dict(self):
        """Test configuration deserialization."""
        data = {
            'annual_goal': 20,
            'simultaneous_reading_limit': 2,
            'favorite_genre': "Fiction"
        }
        
        config = Configuration.from_dict(data)
        
        assert config.annual_goal == 20
        assert config.simultaneous_reading_limit == 2
    
    # TODO
    # def test_configuration_from_dict_with_missing_keys(self):
    #     """Test that from_dict handles missing keys with defaults."""
    #     data = {}
        
    #     config = Configuration.from_dict(data)
        
    #     assert config.annual_goal == 0
    #     assert config.simultaneous_reading_limit == 5