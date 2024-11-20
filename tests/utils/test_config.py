from dataclasses import dataclass
from typing import Dict, Any
import yaml
from pathlib import Path

@dataclass
class TestConfig:
    timeout: int = 10
    retry_count: int = 3
    performance_thresholds: Dict[str, float] = None
    browser_config: Dict[str, Any] = None
    
    @classmethod
    def load_from_yaml(cls, config_path: Path) -> 'TestConfig':
        with config_path.open() as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)
    
    def save_to_yaml(self, config_path: Path):
        with config_path.open('w') as f:
            yaml.dump(self.__dict__, f) 