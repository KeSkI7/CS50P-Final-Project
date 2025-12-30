import pytest
import project
import unittest
from unittest.mock import patch
from types import SimpleNamespace

def test_percentages():
    assert project.validate_percentage(25, "CPU") == True
    assert project.validate_percentage(100, "RAM") == True

def test_percentages_invalid():
    with pytest.raises(SystemExit):
        project.validate_percentage(125, "RAM")
    with pytest.raises(SystemExit):
        project.validate_percentage(-3, "hello")

class TestCpu(unittest.TestCase):
    @patch('project.psutil.cpu_percent')
    def test_cpu_warn(self, mock_cpu):
        mock_cpu.return_value = 90.0

        alert, usage = project.check_cpu(80)

        self.assertTrue(alert)
        self.assertEqual(usage, 90.0)

    @patch('project.psutil.cpu_percent')
    def test_cpu_ok(self, mock_cpu):
        mock_cpu.return_value = 70.0

        alert, usage = project.check_cpu(80)

        self.assertFalse(alert)
        self.assertEqual(usage, 70.0)


class TestRam(unittest.TestCase):
    @patch('project.psutil.virtual_memory')
    def test_cpu_warn(self, mock_ram):
        mock_ram.return_value.percent = 90.0

        alert, usage = project.check_ram(80)

        self.assertTrue(alert)
        self.assertEqual(usage, 90.0)

    @patch('project.psutil.virtual_memory')
    def test_cpu_ok(self, mock_ram):
        mock_ram.return_value.percent = 70.0

        alert, usage = project.check_ram(80)

        self.assertFalse(alert)
        self.assertEqual(usage, 70.0)

class TestDiskMath(unittest.TestCase):
    def test_calculate_speed_ok(self):
        start = {"Disk1": SimpleNamespace(read_bytes=0, write_bytes = 0)}
        end = {"Disk1": SimpleNamespace(read_bytes=10485760, write_bytes = 0)}

        result = project.check_disks_speed(start, end, duration=2)
        self.assertEqual(result[0]["name"], "Disk1")
        self.assertEqual(result[0]["read"], 5)
        self.assertEqual(result[0]["write"], 0)