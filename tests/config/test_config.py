from dataclasses import dataclass
from typing import Dict, Any
import yaml
from pathlib import Path

@dataclass
class TestConfig:
    browser_config: Dict[str, Any] = None
    performance_thresholds: Dict[str, float] = None
    test_data: Dict[str, Any] = None
    
    @classmethod
    def load(cls) -> 'TestConfig':
        config_path = Path(__file__).parent / "test_config.yaml"
        with config_path.open() as f:
            return cls(**yaml.safe_load(f))
    
    def save(self):
        config_path = Path(__file__).parent / "test_config.yaml"
        with config_path.open('w') as f:
            yaml.dump(self.__dict__, f) 